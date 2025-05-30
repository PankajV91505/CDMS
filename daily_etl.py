import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
import json
import os

def run_etl():
    print("ETL Process Started...")
    
    try:
        # Step 1: Database Connection with validation
        db_file = 'customer_db_1.sqlite'
        if not os.path.exists(db_file):
            raise FileNotFoundError(f"Database file {db_file} not found")
        
        engine = create_engine(f'sqlite:///{db_file}')
        
        with engine.connect() as conn:
            # Step 2: Enhanced data loading with schema validation
            tables = {}
            required_tables = ['customers', 'orders', 'support_tickets']
            
            for table in required_tables:
                try:
                    tables[table] = pd.read_sql(f'SELECT * FROM {table}', conn)
                    print(f"Loaded {table} with {len(tables[table])} records")
                    
                    # Validate critical columns exist
                    if table == 'customers' and 'registration_date' not in tables[table].columns:
                        print("Warning: 'registration_date' not found in customers table")
                except Exception as e:
                    print(f"Failed to load {table}: {str(e)}")
                    tables[table] = pd.DataFrame()

            customers, orders, support_tickets = tables['customers'], tables['orders'], tables['support_tickets']
            
            # Step 3: Fixed duplicate handling with fallback date column
            if not customers.empty:
                # Use registration_date if last_activity_date doesn't exist
                date_col = 'last_activity_date' if 'last_activity_date' in customers.columns else 'registration_date'
                
                if date_col not in customers.columns:
                    print("No suitable date column found in customers. Dropping duplicates without sorting.")
                    customers = customers.drop_duplicates(subset=['email', 'phone'], keep='first')
                else:
                    customers = (
                        customers.sort_values(date_col, ascending=False)
                        .drop_duplicates(subset=['email', 'phone'], keep='first')
                    )
            else:
                print("Customers table is empty - skipping processing")

            # Step 4: Calculate total_amount if missing but quantity & unit_price exist
            if not orders.empty:
                if 'total_amount' not in orders.columns:
                    if all(col in orders.columns for col in ['quantity', 'unit_price']):
                        orders['total_amount'] = orders['quantity'] * orders['unit_price']
                        print("Calculated 'total_amount' from 'quantity' and 'unit_price'")
                    else:
                        print("Cannot calculate 'total_amount' (missing 'quantity' or 'unit_price')")
                if 'total_amount' not in orders.columns:
                    print("'total_amount' missing, skipping CLV calculation")
            
            # Step 5: Time-weighted CLV with empty data check
            if not orders.empty and 'total_amount' in orders.columns and 'order_date' in orders.columns:
                orders['order_date'] = pd.to_datetime(orders['order_date'])
                orders['weight'] = np.exp(-(pd.Timestamp.now() - orders['order_date']).dt.days / 30)
                clv_df = orders.groupby('customer_id').apply(
                    lambda x: (x['total_amount'] * x['weight']).sum()
                ).reset_index(name='CLV')
            else:
                print("Orders data missing or incomplete - skipping CLV calculation")
                clv_df = pd.DataFrame(columns=['customer_id', 'CLV'])

            # Step 6: Quantile-based RFM with validation
            rfm = pd.DataFrame()
            if not orders.empty and all(col in orders.columns for col in ['order_date', 'order_id', 'total_amount', 'customer_id']):
                today = pd.Timestamp.now()
                rfm = orders.groupby('customer_id').agg({
                    'order_date': lambda x: (today - x.max()).days,
                    'order_id': 'count',
                    'total_amount': 'sum'
                }).rename(columns={
                    'order_date': 'Recency',
                    'order_id': 'Frequency',
                    'total_amount': 'Monetary'
                })

                # Fix: Ensure index named customer_id for reset_index
                rfm.index.name = 'customer_id'
                
                for col in rfm.columns:
                    try:
                        rfm[f'{col}_Score'] = pd.qcut(rfm[col], 5, labels=[1, 2, 3, 4, 5])
                    except Exception as e:
                        print(f"Could not calculate {col}_Score: {str(e)}")
                        rfm[f'{col}_Score'] = 3  # Default middle value
                
                rfm['RFM_Score'] = rfm[[f'{c}_Score' for c in ['Recency', 'Frequency', 'Monetary']]].mean(axis=1)
            else:
                print("Orders data missing required columns - skipping RFM calculation")
                rfm = pd.DataFrame()


            if not customers.empty:
                customers = (
                    customers.merge(clv_df, on='customer_id', how='left')
                    .merge(rfm.reset_index(), on='customer_id', how='left')
                    .merge(support_stats, on='customer_id', how='left')
                )
                
                # Calculate health score with robust defaults
                customers['health_score'] = (
                    0.4 * customers['RFM_Score'].fillna(1) +
                    0.3 * (customers['CLV'].fillna(0) / max(customers['CLV'].max(), 1) * 5).clip(0, 5) +
                    0.3 * (5 - np.log1p(customers['ticket_count'].fillna(0)))
                ).round(1)
                
                # Step 8: Save results with validation
                try:
                    customers.to_sql('customer_metrics', conn, index=False, if_exists='replace')
                    print(f"Saved customer metrics with {len(customers)} records")
                except Exception as e:
                    print(f"Failed to save metrics: {str(e)}")
            else:
                print("No customer data available - skipping metric generation")

            # Step 9: Enhanced JSON export with error handling
            export_data = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "metrics_calculated": ["CLV", "RFM", "Health_Score"],
                    "record_count": len(customers) if not customers.empty else 0,
                    "warnings": ["Missing last_activity_date - used registration_date"] if 'last_activity_date' not in customers.columns else []
                },
                "data": customers.where(pd.notnull(customers), None).to_dict('records') if not customers.empty else []
            }
            
            try:
                os.makedirs('reports', exist_ok=True)
                json_path = f"reports/customer_metrics_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
                with open(json_path, 'w') as f:
                    json.dump(export_data, f, indent=2)
                print(f"ETL Completed Successfully! Report: {json_path}")
            except Exception as e:
                print(f"Failed to save JSON report: {str(e)}")

    except Exception as e:
        print(f"Critical ETL Failure: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl()
