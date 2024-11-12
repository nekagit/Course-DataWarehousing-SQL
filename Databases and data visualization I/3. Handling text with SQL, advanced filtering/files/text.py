import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('text_manipulation_demo.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS orders;
        
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        );
        
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            description TEXT,
            product_code TEXT,
            tags TEXT,
            in_stock INTEGER
        );
        
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_status TEXT,
            ship_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );
    ''')
    
    # Insert sample data
    sample_customers = [
        ('John', 'Doe', 'john.DOE@example.com', '5551234567', '  123 Main St  '),
        ('Jane', 'Smith', 'jane.SMITH@example.com', '5559876543', '  456 Oak Ave  '),
        ('Bob', 'Johnson', 'bob.JOHNSON@example.com', '5554567890', '  789 Pine Rd  ')
    ]
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, address)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_customers)
    
    sample_products = [
        ('Digital Camera Pro', 'High-end digital camera with 4K recording', 'CAM', 'camera,electronics,pro', 10),
        ('Wide Angle Lens', 'Professional wide angle lens', 'LENS', 'lens,camera,accessories', 5),
        ('Carbon Fiber Tripod', 'Lightweight tripod for stability', 'TRI', 'tripod,accessories', 0)
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_name, description, product_code, tags, in_stock)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_products)
    
    sample_orders = [
        (1, 'Pending', 'FedEx'),
        (2, 'Shipping', 'USPS'),
        (3, 'Delivered', 'FedEx')
    ]
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, order_status, ship_method)
        VALUES (?, ?, ?)
    ''', sample_orders)
    
    # Commit changes
    conn.commit()
    return conn

def demonstrate_text_manipulation(conn):
    cursor = conn.cursor()
    
    print("\n=== Text Manipulation Examples ===\n")
    
    # 1. Concatenating Text Columns
    print("Full Names using CONCAT:")
    cursor.execute('''
        SELECT first_name || ' ' || last_name AS full_name
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 2. Extracting Substrings
    print("\nFirst 5 characters of email:")
    cursor.execute('''
        SELECT SUBSTR(email, 1, 5) AS first_5_chars
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 3. Converting Text Case
    print("\nUppercase first names:")
    cursor.execute('''
        SELECT UPPER(first_name) AS uppercase_first_name
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 4. Trimming Whitespace
    print("\nTrimmed addresses:")
    cursor.execute('''
        SELECT TRIM(address) AS trimmed_address
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 5. Replacing Text
    print("\nExtracting usernames from emails:")
    cursor.execute('''
        SELECT REPLACE(email, '@example.com', '') AS username
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 6. Using CASE Expression
    print("\nOrder status with friendly names:")
    cursor.execute('''
        SELECT order_id,
               CASE order_status
                   WHEN 'Pending' THEN 'Open'
                   WHEN 'Shipping' THEN 'In Progress'
                   WHEN 'Delivered' THEN 'Closed'
                   ELSE 'Unknown'
               END AS order_status_text
        FROM orders;
    ''')
    print(cursor.fetchall())
    
    # 7. Product Categorization
    print("\nProduct categories based on name:")
    cursor.execute('''
        SELECT product_name,
               CASE 
                   WHEN product_name LIKE '%Camera%' THEN 'Camera'
                   WHEN product_name LIKE '%Lens%' THEN 'Lens'
                   WHEN product_name LIKE '%Tripod%' THEN 'Tripod'
                   ELSE 'Other'
               END AS product_category
        FROM products;
    ''')
    print(cursor.fetchall())
    
    # 8. Formatting Phone Numbers
    print("\nFormatted phone numbers:")
    cursor.execute('''
        SELECT phone,
               '(' || SUBSTR(phone, 1, 3) || ') ' ||
               SUBSTR(phone, 4, 3) || '-' ||
               SUBSTR(phone, 7) AS formatted_phone
        FROM customers;
    ''')
    print(cursor.fetchall())
    
    # 9. Proper Case Names
    print("\nProper case names:")
    cursor.execute('''
        SELECT UPPER(SUBSTR(first_name, 1, 1)) || 
               LOWER(SUBSTR(first_name, 2)) AS proper_first_name,
               UPPER(SUBSTR(last_name, 1, 1)) || 
               LOWER(SUBSTR(last_name, 2)) AS proper_last_name
        FROM customers;
    ''')
    print(cursor.fetchall())

def main():
    # Create database and insert sample data
    conn = create_database()
    
    try:
        # Demonstrate text manipulation examples
        demonstrate_text_manipulation(conn)
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()