import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import json
import os

def connect_db(db_path='customer_db_1.sqlite'):
    conn = sqlite3.connect(db_path)
    return conn

def load_data(conn):
    customers = pd.read_sql('SELECT * FROM customers', conn)
    orders = pd.read_sql('SELECT * FROM orders', conn)
    tickets = pd.read_sql('SELECT * FROM support_tickets', conn)
    reviews = pd.read_sql('SELECT * FROM product_reviews', conn)
    return customers, orders, tickets, reviews

def clean_customers(df_customers):
    df_clean = df_customers.drop_duplicates(subset='email')
    return df_clean

def calculate_clv(df_orders):
    clv = df_orders.groupby('customer_id')['total_amount'].sum().reset_index()
    clv.columns = ['customer_id', 'lifetime_value']
    return clv

def rfm_analysis(df_orders):
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])

    recency_df = df_orders.groupby('customer_id')['order_date'].max().reset_index()
    recency_df['recency'] = (datetime.today() - recency_df['order_date']).dt.days

    frequency_df = df_orders.groupby('customer_id').size().reset_index(name='frequency')
    monetary_df = df_orders.groupby('customer_id')['total_amount'].sum().reset_index(name='monetary')

    rfm = recency_df.merge(frequency_df, on='customer_id')
    rfm = rfm.merge(monetary_df, on='customer_id')

    rfm['r_score'] = safe_qcut(rfm['recency'], 3, labels=[3, 2, 1])
    rfm['f_score'] = safe_qcut(rfm['frequency'], 3, labels=[1, 2, 3])
    rfm['m_score'] = safe_qcut(rfm['monetary'], 3, labels=[1, 2, 3])
    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

    return rfm

def safe_qcut(series, q, labels):
    try:
        return pd.qcut(series, q, labels=labels, duplicates='drop')
    except ValueError:
        return pd.Series([labels[len(labels) // 2]] * len(series), index=series.index)

def assign_health_score(df_customers, df_tickets):
    ticket_counts = df_tickets.groupby('customer_id').size().reset_index(name='ticket_count')
    df = df_customers.merge(ticket_counts, on='customer_id', how='left')
    df['ticket_count'] = df['ticket_count'].fillna(0)

    df['health_score'] = np.where(df['ticket_count'] > 3, 'Low', 'High')
    return df

def save_to_db(conn, df_customers, df_rfm):
    df_customers.to_sql('customers_cleaned', conn, if_exists='replace', index=False)
    df_rfm.to_sql('customer_rfm', conn, if_exists='replace', index=False)
    print("Data saved to database")

def generate_data_quality_report(df_customers, df_orders, df_tickets, df_reviews):
    report = {
        'customers': {
            'missing_values': df_customers.isnull().sum().to_dict(),
            'duplicate_emails': int(df_customers.duplicated(subset='email').sum())
        },
        'orders': {
            'missing_values': df_orders.isnull().sum().to_dict()
        },
        'support_tickets': {
            'missing_values': df_tickets.isnull().sum().to_dict()
        },
        'product_reviews': {
            'missing_values': df_reviews.isnull().sum().to_dict()
        },
        'report_generated_at': datetime.now().isoformat()
    }

    with open('data_quality_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("Data quality report generated")

def run_etl():
    try:
        conn = connect_db()
        customers, orders, tickets, reviews = load_data(conn)
        generate_data_quality_report(customers, orders, tickets, reviews)
        customers_clean = clean_customers(customers)
        clv = calculate_clv(orders)
        customers_clean = customers_clean.merge(clv, on='customer_id', how='left')
        customers_clean['lifetime_value'] = customers_clean['lifetime_value'].fillna(0)
        rfm = rfm_analysis(orders)
        customers_clean = assign_health_score(customers_clean, tickets)
        save_to_db(conn, customers_clean, rfm)
        conn.close()

    except Exception as e:
        print(f"Critical ETL Failure: {str(e)}")
        raise
if __name__ == '__main__':
    run_etl()
