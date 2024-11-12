import sqlite3
from datetime import datetime

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('joins_guide.db')
    cursor = conn.cursor()
    
    # Create basic tables
    cursor.executescript('''
        -- Basic tables for join examples
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            amount DECIMAL(10,2)
        );
        
        -- Additional tables for advanced examples
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            manager_id INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name VARCHAR(100),
            category VARCHAR(50)
        );
        
        -- Tables for set operations
        CREATE TABLE IF NOT EXISTS orders_2023 (
            customer_id INTEGER,
            amount DECIMAL(10,2)
        );
        
        CREATE TABLE IF NOT EXISTS orders_2024 (
            customer_id INTEGER,
            amount DECIMAL(10,2)
        );
        
        CREATE TABLE IF NOT EXISTS active_customers (
            customer_id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE IF NOT EXISTS premium_members (
            customer_id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE IF NOT EXISTS all_customers (
            customer_id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE IF NOT EXISTS opted_out_customers (
            customer_id INTEGER PRIMARY KEY
        );
        
        CREATE TABLE IF NOT EXISTS north_sales (
            amount DECIMAL(10,2)
        );
        
        CREATE TABLE IF NOT EXISTS south_sales (
            amount DECIMAL(10,2)
        );
    ''')

    # Sample data insertion
    sample_data = {
        'customers': [
            (1, 'John Doe', 'john@example.com'),
            (2, 'Jane Smith', 'jane@example.com'),
            (3, 'Bob Wilson', 'bob@example.com')
        ],
        'orders': [
            (1, 1, '2024-01-01', 100.00),
            (2, 1, '2024-01-15', 200.00),
            (3, 2, '2024-01-20', 150.00)
        ],
        'employees': [
            (1, 'Alice Manager', None),
            (2, 'Bob Employee', 1),
            (3, 'Charlie Worker', 1),
            (4, 'David Staff', 2)
        ],
        'products': [
            (1, 'Laptop', 'Electronics'),
            (2, 'Phone', 'Electronics'),
            (3, 'Chair', 'Furniture')
        ]
    }

    # Insert sample data
    cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?,?,?)', sample_data['customers'])
    cursor.executemany('INSERT OR REPLACE INTO orders VALUES (?,?,?,?)', sample_data['orders'])
    cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?,?,?)', sample_data['employees'])
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?,?,?)', sample_data['products'])

    # Sample data for set operations
    set_operations_data = {
        'orders_2023': [(1, 500.00), (2, 750.00)],
        'orders_2024': [(2, 800.00), (3, 900.00)],
        'active_customers': [(1,), (2,), (3,)],
        'premium_members': [(1,), (3,)],
        'all_customers': [(1,), (2,), (3,), (4,)],
        'opted_out_customers': [(2,), (4,)],
        'north_sales': [(1000.00,), (1200.00,)],
        'south_sales': [(800.00,), (900.00,)]
    }

    for table, data in set_operations_data.items():
        if table in ['orders_2023', 'orders_2024']:
            cursor.executemany(f'INSERT OR REPLACE INTO {table} VALUES (?,?)', data)
        elif table in ['north_sales', 'south_sales']:
            cursor.executemany(f'INSERT OR REPLACE INTO {table} VALUES (?)', data)
        else:
            cursor.executemany(f'INSERT OR REPLACE INTO {table} VALUES (?)', data)

    conn.commit()
    return conn

def run_example_queries(conn):
    cursor = conn.cursor()
    
    # Dictionary of example queries
    example_queries = {
        'INNER JOIN': '''
            SELECT 
                c.name,
                o.order_id,
                o.amount
            FROM customers c
            INNER JOIN orders o ON c.customer_id = o.customer_id
        ''',
        'LEFT JOIN': '''
            SELECT 
                c.name,
                COUNT(o.order_id) as order_count
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.name
        ''',
        'CROSS JOIN': '''
            SELECT 
                c.name,
                p.product_name
            FROM customers c
            CROSS JOIN products p
            WHERE p.category = 'Electronics'
        ''',
        'SELF JOIN': '''
            SELECT 
                e1.name as employee,
                e2.name as manager
            FROM employees e1
            LEFT JOIN employees e2 ON e1.manager_id = e2.emp_id
        ''',
        'UNION': '''
            SELECT customer_id FROM orders_2023
            UNION
            SELECT customer_id FROM orders_2024
        '''
    }
    
    # Run and print results for each example query
    print("\nRunning example queries:")
    for query_name, query in example_queries.items():
        print(f"\n{query_name} Example:")
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)

def main():
    print("Creating database and sample data...")
    conn = create_database()
    run_example_queries(conn)
    print("\nDatabase 'joins_guide.db' has been created with all sample tables and data.")
    conn.close()

if __name__ == "__main__":
    main()