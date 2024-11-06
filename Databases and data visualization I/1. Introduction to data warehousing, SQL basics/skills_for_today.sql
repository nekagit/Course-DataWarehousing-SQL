-- Setting up the database
-- This assumes PostgreSQL is installed and accessible

-- Create a new table to store user data
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data into the users table
INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Carol', 'carol@example.com');

-- Retrieve data from the users table
SELECT * FROM users;

-- Filter data with WHERE clause
SELECT name, email FROM users WHERE name = 'Alice';

-- Update data in the users table
UPDATE users
SET email = 'alice_new@example.com'
WHERE name = 'Alice';

-- Delete data from the users table
DELETE FROM users WHERE name = 'Bob';

-- Add a new column to an existing table
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Create a view for easier data access
CREATE VIEW user_info AS
SELECT name, email, phone
FROM users;

-- Select data from the view
SELECT * FROM user_info;

-- Create a table for product information
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Insert sample products into the products table
INSERT INTO products (product_name, price, stock) VALUES
('Laptop', 1200.00, 10),
('Smartphone', 800.00, 25),
('Tablet', 450.00, 15);

-- Basic query to check products
SELECT * FROM products;

-- Drop the products table if it is no longer needed
DROP TABLE products;

-- End of .sql example
