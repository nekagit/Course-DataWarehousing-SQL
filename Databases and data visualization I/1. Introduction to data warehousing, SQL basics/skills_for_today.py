import sqlite3
import datetime

# Connect to a local SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# 1. Create the users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# 2. Insert data into the users table
cursor.executemany("""
    INSERT INTO users (name, email) VALUES (?, ?);
""", [
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com')
])
conn.commit()

# 3. Retrieve all data from the users table
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("Users:")
for user in users:
    print(user)

# 4. Filter data with a WHERE clause
cursor.execute("SELECT name, email FROM users WHERE name = 'Alice';")
alice = cursor.fetchone()
print("\nAlice's record:")
print(alice)

# 5. Update data in the users table
cursor.execute("""
    UPDATE users
    SET email = 'alice_new@example.com'
    WHERE name = 'Alice';
""")
conn.commit()

# Confirm update
cursor.execute("SELECT name, email FROM users WHERE name = 'Alice';")
updated_alice = cursor.fetchone()
print("\nUpdated Alice's record:")
print(updated_alice)

# 6. Delete data
cursor.execute("DELETE FROM users WHERE name = 'Bob';")
conn.commit()

# 7. Add a new column to an existing table
cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT;")
conn.commit()

# 8. Create a view for easier data access
cursor.execute("""
    CREATE VIEW IF NOT EXISTS user_info AS
    SELECT name, email, phone
    FROM users;
""")
conn.commit()

# 9. Select data from the view
cursor.execute("SELECT * FROM user_info;")
user_info = cursor.fetchall()
print("\nUser Info View:")
for info in user_info:
    print(info)

# 10. Create a table for product information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    );
""")
conn.commit()

# 11. Insert sample products into the products table
cursor.executemany("""
    INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?);
""", [
    ('Laptop', 1200.00, 10),
    ('Smartphone', 800.00, 25),
    ('Tablet', 450.00, 15)
])
conn.commit()

# 12. Basic query to check products
cursor.execute("SELECT * FROM products;")
products = cursor.fetchall()
print("\nProducts:")
for product in products:
    print(product)

# 13. Drop the products table if it is no longer needed
cursor.execute("DROP TABLE IF EXISTS products;")
conn.commit()

# Close the connection
conn.close()
