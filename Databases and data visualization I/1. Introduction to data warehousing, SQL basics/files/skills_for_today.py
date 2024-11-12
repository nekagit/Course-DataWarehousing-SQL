import sqlite3
import datetime
import os

# Delete the existing database file if it exists
if os.path.exists("example.db"):
    os.remove("example.db")
    print("Existing database deleted.")

# Create a new connection to a SQLite database
# This will create a new database file if it doesn't exist
print("Creating new database: example.db")
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# =====================================
# 1. TABLE CREATION
# =====================================
# Create the users table with the following columns:
# - id: A unique identifier that auto-increments
# - name: The user's name (required)
# - email: The user's email (required)
# - created_at: Timestamp of when the record was created (automatically set)
print("\nCreating users table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing primary key
        name TEXT NOT NULL,                    -- User's name (required)
        email TEXT NOT NULL,                   -- User's email (required)
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automatically set timestamp
    );
""")
conn.commit()  # Save the changes to the database

# =====================================
# 2. DATA INSERTION
# =====================================
# Insert multiple users at once using executemany
# This is more efficient than multiple single inserts
print("\nInserting sample users...")
cursor.executemany("""
    INSERT INTO users (name, email) VALUES (?, ?);
""", [
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com'),
    ('David', 'david@example.com'),
    ('Eve', 'eve@example.com')
])
conn.commit()

# =====================================
# 3. BASIC SELECT WITH ORDERING
# =====================================
# Retrieve all users, ordered alphabetically by name
print("\nRetrieving all users ordered by name...")
cursor.execute("SELECT * FROM users ORDER BY name ASC;")  # ASC means ascending order
users = cursor.fetchall()  # Get all results
print("Users (ordered by name):")
for user in users:
    print(user)

# =====================================
# 4. FILTERED SELECT WITH ORDERING
# =====================================
# Select users whose names start with 'A', ordered by email in descending order
print("\nRetrieving filtered users...")
cursor.execute("""
    SELECT name, email 
    FROM users 
    WHERE name LIKE 'A%'    -- Filter names starting with 'A'
    ORDER BY email DESC;    -- DESC means descending order
""")
filtered_users = cursor.fetchall()
print("Filtered users (ordered by email descending):")
print(filtered_users)

# =====================================
# 5. UPDATE DATA
# =====================================
# Update Alice's email address and verify the change
print("\nUpdating user data...")
cursor.execute("""
    UPDATE users
    SET email = 'alice_new@example.com'
    WHERE name = 'Alice';
""")
conn.commit()

# Verify the update with ordered results
cursor.execute("""
    SELECT name, email 
    FROM users 
    WHERE name = 'Alice' 
    ORDER BY created_at DESC;
""")
updated_alice = cursor.fetchone()
print("Updated Alice's record:")
print(updated_alice)

# =====================================
# 6. DELETE DATA
# =====================================
# Remove Bob's record from the database
print("\nDeleting user data...")
cursor.execute("DELETE FROM users WHERE name = 'Bob';")
conn.commit()

# =====================================
# 7. ALTER TABLE
# =====================================
# Add a new column to the existing users table
print("\nAdding new column to users table...")
cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT;")
conn.commit()

# =====================================
# 8. CREATE VIEW
# =====================================
# Create a view that provides a simplified way to access user data
# Views are like virtual tables based on a SELECT statement
print("\nCreating user_info view...")
cursor.execute("""
    CREATE VIEW IF NOT EXISTS user_info AS
    SELECT name, email, phone
    FROM users
    ORDER BY name;  -- The view will always return results ordered by name
""")
conn.commit()

# =====================================
# 9. USE VIEW
# =====================================
# Select data from the view we just created
print("\nRetrieving data from view...")
cursor.execute("SELECT * FROM user_info;")
user_info = cursor.fetchall()
print("User Info View (ordered by name):")
for info in user_info:
    print(info)

# =====================================
# 10. CREATE PRODUCTS TABLE
# =====================================
# Create a new table for storing product information
print("\nCreating products table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID
        product_name TEXT NOT NULL,                    -- Product name (required)
        price REAL NOT NULL,                          -- Price (required)
        stock INTEGER NOT NULL                        -- Stock quantity (required)
    );
""")
conn.commit()

# =====================================
# 11. INSERT PRODUCTS
# =====================================
# Insert sample product data
print("\nInserting sample products...")
cursor.executemany("""
    INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?);
""", [
    ('Laptop', 1200.00, 10),
    ('Smartphone', 800.00, 25),
    ('Tablet', 450.00, 15),
    ('Monitor', 300.00, 20),
    ('Keyboard', 50.00, 30)
])
conn.commit()

# =====================================
# 12. COMPLEX ORDERING
# =====================================
# Query products with multiple ORDER BY criteria
print("\nQuerying products with complex ordering...")
cursor.execute("""
    SELECT * FROM products 
    ORDER BY price DESC,    -- First order by price (highest to lowest)
             stock ASC;     -- Then by stock (lowest to highest)
""")
products = cursor.fetchall()
print("Products (ordered by price descending, then stock ascending):")
for product in products:
    print(product)

# =====================================
# 13. CONDITIONAL ORDERING
# =====================================
# Query products with conditional ordering using CASE statement
print("\nQuerying products with conditional ordering...")
cursor.execute("""
    SELECT 
        product_name, 
        price, 
        stock,
        CASE                                    -- Create a computed column
            WHEN stock < 20 THEN 'Low Stock'    -- Less than 20 items
            WHEN stock < 30 THEN 'Medium Stock' -- Less than 30 items
            ELSE 'High Stock'                   -- 30 or more items
        END as stock_status
    FROM products
    ORDER BY stock_status,  -- First order by stock status
             price;         -- Then by price
""")
products_with_status = cursor.fetchall()
print("Products with stock status (ordered by status and price):")
for product in products_with_status:
    print(product)

# =====================================
# 14. CLEANUP
# =====================================
# Drop the products table and close the database connection
print("\nCleaning up...")
cursor.execute("DROP TABLE IF EXISTS products;")
conn.commit()

# Close the database connection
conn.close()
print("\nDatabase connection closed.")

print("\nScript execution completed successfully.")