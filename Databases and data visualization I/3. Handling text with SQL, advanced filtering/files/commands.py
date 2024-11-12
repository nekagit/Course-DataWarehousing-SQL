import sqlite3
from datetime import datetime

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('string_manipulation.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    -- Customers table
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT
    );
    
    -- Products table
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL NOT NULL
    );
    
    -- Orders table
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_status TEXT NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    ''')
    
    # Sample data for customers
    customers_data = [
        (1, 'John', 'Doe', 'john.doe@email.com', '123-456-7890'),
        (2, 'Jane', 'Smith', 'jane.smith@email.com', '234-567-8901'),
        (3, 'Bob', 'Johnson', 'bob.j@email.com', '345-678-9012')
    ]
    
    # Sample data for products
    products_data = [
        (1, 'Camera X1000', 599.99),
        (2, 'Wide Angle Lens', 299.99),
        (3, 'Professional Tripod', 149.99),
        (4, 'Memory Card', 49.99)
    ]
    
    # Sample data for orders
    orders_data = [
        (1, 1, 'Pending', '2024-01-01'),
        (2, 2, 'Shipping', '2024-01-02'),
        (3, 3, 'Delivered', '2024-01-03')
    ]
    
    # Insert sample data
    cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?)', customers_data)
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?)', products_data)
    cursor.executemany('INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?)', orders_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

def demonstrate_string_operations():
    conn = sqlite3.connect('string_manipulation.db')
    cursor = conn.cursor()
    
    print("=== String Manipulation Examples ===\n")
    
    # Concatenation example
    print("1. Name Concatenation:")
    cursor.execute('''
        SELECT first_name || ' ' || last_name AS full_name 
        FROM customers
    ''')
    for row in cursor.fetchall():
        print(f"  Full name: {row[0]}")
    
    # Substring position example
    print("\n2. Email @ Position:")
    cursor.execute('''
        SELECT email, instr(email, '@') AS at_position 
        FROM customers
    ''')
    for row in cursor.fetchall():
        print(f"  Email: {row[0]}, @ position: {row[1]}")
    
    # Substring extraction example
    print("\n3. Phone Area Codes:")
    cursor.execute('''
        SELECT phone, substr(phone, 1, 3) AS area_code 
        FROM customers
    ''')
    for row in cursor.fetchall():
        print(f"  Phone: {row[0]}, Area Code: {row[1]}")
    
    # CASE expression example
    print("\n4. Order Status Text:")
    cursor.execute('''
        SELECT order_id,
               CASE order_status
                   WHEN 'Pending' THEN 'Open'
                   WHEN 'Shipping' THEN 'In Progress'
                   WHEN 'Delivered' THEN 'Closed'
                   ELSE 'Unknown'
               END AS order_status_text
        FROM orders
    ''')
    for row in cursor.fetchall():
        print(f"  Order ID: {row[0]}, Status: {row[1]}")
    
    # Product categorization example
    print("\n5. Product Categories:")
    cursor.execute('''
        SELECT product_name,
               CASE
                   WHEN product_name LIKE 'Camera%' THEN 'Camera'
                   WHEN product_name LIKE '%Lens' THEN 'Lens'
                   WHEN product_name LIKE '%Tripod' THEN 'Tripod'
                   ELSE 'Other'
               END AS product_category
        FROM products
    ''')
    for row in cursor.fetchall():
        print(f"  Product: {row[0]}, Category: {row[1]}")
    
    conn.close()

if __name__ == '__main__':
    # Create the database and insert sample data
    create_database()
    
    # Run the demonstration
    demonstrate_string_operations()