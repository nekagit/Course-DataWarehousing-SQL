import sqlite3
from datetime import datetime

def create_database():
    # Connect to SQLite database
    conn = sqlite3.connect('aggregation_guide.db')
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(50),
            job_title VARCHAR(100),
            salary DECIMAL(10,2),
            hire_date DATE
        )
    ''')
    
    # Sample employee data
    employees_data = [
        (1, 'John Doe', 'Engineering', 'Senior Developer', 85000.00, '2020-01-15'),
        (2, 'Jane Smith', 'Engineering', 'Developer', 65000.00, '2021-03-01'),
        (3, 'Bob Wilson', 'Sales', 'Sales Manager', 75000.00, '2019-11-01'),
        (4, 'Alice Brown', 'Sales', 'Sales Representative', 55000.00, '2022-01-15'),
        (5, 'Charlie Davis', 'Marketing', 'Marketing Manager', 70000.00, '2020-06-01'),
        (6, 'Eve Wilson', 'Engineering', 'Developer', 67000.00, '2021-07-15'),
        (7, 'Frank Miller', 'Sales', 'Sales Representative', 52000.00, '2022-03-01'),
        (8, 'Grace Lee', 'Marketing', 'Marketing Specialist', None, '2023-01-15'),
        (9, 'Henry Garcia', 'Engineering', 'Developer', 63000.00, '2021-09-01'),
        (10, 'Ivy Chen', 'Sales', 'Sales Representative', 54000.00, '2022-05-15')
    ]
    
    # Insert sample data
    cursor.executemany('''
        INSERT OR REPLACE INTO employees 
        (id, name, department, job_title, salary, hire_date) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    conn.commit()
    return conn

def demonstrate_aggregations(conn):
    cursor = conn.cursor()
    
    examples = {
        "Basic COUNT Examples": [
            ("Count all employees", 
             "SELECT COUNT(*) FROM employees"),
            ("Count employees with salary (non-NULL)", 
             "SELECT COUNT(salary) FROM employees"),
            ("Count distinct departments", 
             "SELECT COUNT(DISTINCT department) FROM employees")
        ],
        
        "NULL Handling": [
            ("Find NULL salaries", 
             "SELECT name FROM employees WHERE salary IS NULL"),
            ("Replace NULL with 0 using COALESCE", 
             "SELECT name, COALESCE(salary, 0) AS salary FROM employees"),
            ("Compare total count vs non-NULL salary count", 
             """SELECT COUNT(*) as total_count,
                      COUNT(salary) as salary_count 
                FROM employees""")
        ],
        
        "ROUND Functions": [
            ("Round salaries to nearest integer", 
             "SELECT name, ROUND(salary) FROM employees WHERE salary IS NOT NULL"),
            ("Round salaries to 2 decimal places", 
             "SELECT name, ROUND(salary, 2) FROM employees WHERE salary IS NOT NULL")
        ],
        
        "Arithmetic Operations": [
            ("Calculate monthly salaries", 
             """SELECT name, 
                      ROUND(salary/12, 2) as monthly_salary 
                FROM employees 
                WHERE salary IS NOT NULL"""),
            ("Apply 10% raise", 
             """SELECT name, 
                      salary as current_salary,
                      ROUND(salary * 1.1, 2) as salary_with_raise 
                FROM employees 
                WHERE salary IS NOT NULL""")
        ],
        
        "GROUP BY Examples": [
            ("Count employees by department", 
             """SELECT department, 
                      COUNT(*) as employee_count 
                FROM employees 
                GROUP BY department"""),
            ("Department salary statistics", 
             """SELECT department,
                      COUNT(*) as employee_count,
                      ROUND(AVG(salary), 2) as avg_salary,
                      MAX(salary) as max_salary,
                      MIN(salary) as min_salary
                FROM employees
                GROUP BY department"""),
            ("Departments with more than 2 employees", 
             """SELECT department, 
                      COUNT(*) as employee_count
                FROM employees
                GROUP BY department
                HAVING COUNT(*) > 2""")
        ]
    }
    
    # Run and display all examples
    print("\nSQL Aggregation Functions Examples:")
    print("=" * 50)
    
    for category, queries in examples.items():
        print(f"\n{category}")
        print("-" * len(category))
        
        for description, query in queries:
            print(f"\n{description}:")
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Format and display results
            for row in results:
                if len(row) == 1:
                    print(f"Result: {row[0]}")
                else:
                    print(row)

def main():
    print("Creating database with sample data...")
    conn = create_database()
    print("\nDatabase 'aggregation_guide.db' created successfully.")
    
    print("\nDemonstrating SQL aggregation functions...")
    demonstrate_aggregations(conn)
    
    conn.close()
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()