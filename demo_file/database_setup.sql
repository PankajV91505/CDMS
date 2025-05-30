-- Customer Database Setup for Project 3
-- Run this script to create the SQLite database with sample data

-- Create customers table
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    registration_date DATE,
    birth_date DATE,
    city TEXT,
    country TEXT,
    status TEXT
);

-- Create orders table
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status TEXT,
    payment_method TEXT,
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create support_tickets table
CREATE TABLE support_tickets (
    ticket_id TEXT PRIMARY KEY,
    customer_id TEXT,
    created_date DATETIME,
    issue_type TEXT,
    priority TEXT,
    status TEXT,
    resolution_date DATETIME,
    satisfaction_rating INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create product_reviews table
CREATE TABLE product_reviews (
    review_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    order_id TEXT,
    rating INTEGER,
    review_text TEXT,
    review_date DATE,
    helpful_votes INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Insert sample customers data
INSERT INTO customers VALUES
('CUST001', 'John', 'Doe', 'john.doe@email.com', '+1-555-0101', '2023-01-15', '1990-05-12', 'New York', 'USA', 'active'),
('CUST002', 'Jane', 'Smith', 'jane.smith@gmail.com', '+44-20-7946-0958', '2023-02-20', '1985-08-22', 'London', 'UK', 'active'),
('CUST003', 'Bob', 'Wilson', 'bob.wilson@company.com', '+1-416-555-0199', '2023-03-10', '1992-03-15', 'Toronto', 'Canada', 'active'),
('CUST004', 'Alice', 'Brown', 'alice.brown@yahoo.com', '+61-2-9876-5432', '2023-04-05', '1988-11-30', 'Sydney', 'Australia', 'inactive'),
('CUST005', 'Charlie', 'Davis', 'charlie.davis@hotmail.com', '+49-30-12345678', '2023-05-12', '1975-07-18', 'Berlin', 'Germany', 'active'),
('CUST006', 'Diana', 'Miller', 'diana.miller@email.com', '+1-312-555-0142', '2023-06-18', '1993-12-05', 'Chicago', 'USA', 'active'),
('CUST007', 'Frank', 'Taylor', 'frank.taylor@gmail.com', '+44-161-496-0000', '2023-07-22', '1980-04-28', 'Manchester', 'UK', 'active'),
('CUST008', 'Grace', 'Lee', 'grace.lee@email.com', '+1-604-555-0167', '2023-08-08', '1991-09-14', 'Vancouver', 'Canada', 'active'),
('CUST011', 'John', 'Doe', 'john.doe@email.com', '+1-555-0101', '2023-01-15', '1990-05-12', 'New York', 'USA', 'active'),
('CUST009', 'Henry', 'Clark', 'henry.clark@yahoo.com', '+49-40-87654321', '2023-09-14', '1987-02-11', 'Hamburg', 'Germany', 'active'),
('CUST010', 'Ivy', 'Adams', 'ivy.adams@hotmail.com', '+61-3-8765-4321', '2023-10-03', '1972-06-25', 'Melbourne', 'Australia', 'active');

-- Insert sample orders data
INSERT INTO orders VALUES
('ORD001', 'CUST001', '2024-01-15', 179.98, 'completed', 'credit_card', '123 Main St, New York, NY 10001'),
('ORD002', 'CUST002', '2024-01-15', 45.50, 'completed', 'paypal', '456 Oxford St, London W1A 0AA'),
('ORD003', 'CUST003', '2024-01-16', 299.99, 'completed', 'credit_card', '789 King St W, Toronto, ON M5V 1M5'),
('ORD004', 'CUST001', '2024-01-17', 38.97, 'completed', 'credit_card', '123 Main St, New York, NY 10001'),
('ORD005', 'CUST004', '2024-01-18', 199.99, 'completed', 'bank_transfer', '321 George St, Sydney NSW 2000'),
('ORD006', 'CUST005', '2024-01-18', 78.75, 'completed', 'credit_card', '654 Unter den Linden, Berlin 10117'),
('ORD007', 'CUST002', '2024-01-19', 69.98, 'completed', 'paypal', '456 Oxford St, London W1A 0AA'),
('ORD008', 'CUST006', '2024-01-20', 19.99, 'shipped', 'credit_card', '987 Michigan Ave, Chicago, IL 60611'),
('ORD009', 'CUST003', '2024-01-21', 75.00, 'processing', 'credit_card', '789 King St W, Toronto, ON M5V 1M5'),
('ORD010', 'CUST007', '2024-01-22', 51.98, 'completed', 'debit_card', '147 Deansgate, Manchester M1 5DU'),
('ORD011', 'CUST008', '2024-01-23', 45.00, 'cancelled', 'credit_card', '258 Robson St, Vancouver, BC V6B 6B5'),
('ORD012', 'CUST001', '2024-01-24', 120.00, 'completed', 'credit_card', '123 Main St, New York, NY 10001'),
('ORD013', 'CUST009', '2024-01-25', 35.99, 'completed', 'bank_transfer', '369 Reeperbahn, Hamburg 22767'),
('ORD014', 'CUST010', '2024-01-26', 59.98, 'shipped', 'credit_card', '741 Collins St, Melbourne VIC 3000'),
('ORD015', 'CUST004', '2024-01-27', 56.97, 'completed', 'paypal', '321 George St, Sydney NSW 2000');

-- Insert sample support tickets data
INSERT INTO support_tickets VALUES
('TK001', 'CUST001', '2024-01-16 09:30:00', 'product_defect', 'high', 'resolved', '2024-01-16 14:20:00', 4),
('TK002', 'CUST002', '2024-01-17 11:15:00', 'shipping_delay', 'medium', 'resolved', '2024-01-18 10:00:00', 5),
('TK003', 'CUST003', '2024-01-18 14:45:00', 'billing_issue', 'high', 'resolved', '2024-01-19 09:30:00', 3),
('TK004', 'CUST004', '2024-01-20 08:20:00', 'return_request', 'low', 'resolved', '2024-01-22 16:45:00', 4),
('TK005', 'CUST005', '2024-01-21 16:30:00', 'technical_support', 'medium', 'in_progress', NULL, NULL),
('TK006', 'CUST006', '2024-01-23 10:10:00', 'account_access', 'high', 'resolved', '2024-01-23 13:25:00', 5),
('TK007', 'CUST007', '2024-01-24 13:50:00', 'product_inquiry', 'low', 'resolved', '2024-01-25 11:15:00', 4),
('TK008', 'CUST001', '2024-01-25 09:00:00', 'shipping_delay', 'medium', 'open', NULL, NULL),
('TK009', 'CUST008', '2024-01-26 15:20:00', 'billing_issue', 'high', 'in_progress', NULL, NULL),
('TK010', 'CUST009', '2024-01-27 12:35:00', 'return_request', 'medium', 'resolved', '2024-01-28 14:10:00', 3);

-- Insert sample product reviews data
INSERT INTO product_reviews VALUES
('REV001', 'CUST001', 'PROD001', 'ORD001', 5, 'Excellent headphones! Great sound quality and comfortable to wear.', '2024-01-18', 12),
('REV002', 'CUST002', 'PROD002', 'ORD002', 4, 'Good gaming mouse, responsive and ergonomic design.', '2024-01-19', 8),
('REV003', 'CUST003', 'PROD003', 'ORD003', 5, 'Perfect office chair! Very comfortable for long work hours.', '2024-01-20', 15),
('REV004', 'CUST001', 'PROD004', 'ORD004', 3, 'USB cable works fine but feels a bit flimsy.', '2024-01-21', 3),
('REV005', 'CUST004', 'PROD005', 'ORD005', 4, 'Coffee maker makes great coffee, easy to use and clean.', '2024-01-22', 9),
('REV006', 'CUST005', 'PROD006', 'ORD006', 5, 'Love these notebooks! Great paper quality and nice design.', '2024-01-23', 6),
('REV007', 'CUST002', 'PROD007', 'ORD007', 4, 'Desk lamp provides good lighting, adjustable and sturdy.', '2024-01-24', 7),
('REV008', 'CUST006', 'PROD008', 'ORD008', 5, 'Water bottle keeps drinks cold all day, highly recommend!', '2024-01-25', 11),
('REV009', 'CUST007', 'PROD010', 'ORD010', 4, 'Phone case fits perfectly and provides good protection.', '2024-01-26', 5),
('REV010', 'CUST001', 'PROD012', 'ORD012', 5, 'Bluetooth speaker has amazing sound quality for the price!', '2024-01-27', 18),
('REV011', 'CUST009', 'PROD013', 'ORD013', 3, 'Kitchen scale is accurate but the display could be brighter.', '2024-01-28', 4),
('REV012', 'CUST010', 'PROD014', 'ORD014', 4, 'Reading glasses are comfortable and the prescription is perfect.', '2024-01-29', 2),
('REV013', 'CUST004', 'PROD015', 'ORD015', 5, 'Travel mug keeps coffee hot for hours, no leaks!', '2024-01-30', 8);