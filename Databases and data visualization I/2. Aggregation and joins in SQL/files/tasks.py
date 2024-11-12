import sqlite3
from datetime import datetime, date

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('practice.db')
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            salary DECIMAL(10,2),
            department_id INTEGER,
            manager_id INTEGER,
            hire_date DATE
        );

        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name VARCHAR(50),
            location VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            project_name VARCHAR(50),
            budget DECIMAL(10,2),
            dept_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS employee_projects (
            emp_id INTEGER,
            project_id INTEGER,
            hours_worked DECIMAL(10,2)
        );
    ''')

    # Sample data
    departments_data = [
        (1, 'Engineering', 'New York'),
        (2, 'Marketing', 'Los Angeles'),
        (3, 'HR', 'Chicago'),
        (4, 'Sales', 'Boston')
    ]

    employees_data = [
        (1, 'John Doe', 85000.00, 1, None, '2020-01-15'),
        (2, 'Jane Smith', 75000.00, 1, 1, '2020-02-01'),
        (3, 'Bob Johnson', 65000.00, 2, 1, '2020-03-15'),
        (4, 'Alice Brown', 72000.00, 2, 3, '2020-04-01'),
        (5, 'Charlie Wilson', 68000.00, 3, 1, '2020-05-15')
    ]

    projects_data = [
        (1, 'Website Redesign', 100000.00, 1),
        (2, 'Mobile App', 150000.00, 1),
        (3, 'Marketing Campaign', 80000.00, 2),
        (4, 'HR System', 120000.00, 3)
    ]

    employee_projects_data = [
        (1, 1, 120.5),
        (1, 2, 80.0),
        (2, 1, 100.0),
        (3, 3, 150.0),
        (4, 3, 120.0),
        (5, 4, 90.0)
    ]

    # Insert sample data
    cursor.executemany('INSERT OR REPLACE INTO departments VALUES (?,?,?)', departments_data)
    cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?,?,?,?,?,?)', employees_data)
    cursor.executemany('INSERT OR REPLACE INTO projects VALUES (?,?,?,?)', projects_data)
    cursor.executemany('INSERT OR REPLACE INTO employee_projects VALUES (?,?,?)', employee_projects_data)

    # Commit changes and close connection
    conn.commit()
    return conn

def run_tasks(conn):
    cursor = conn.cursor()
    
    # Task 1: Basic COUNT and NULL Handling
    print("\nTask 1 - Employee Counts:")
    cursor.execute('''
        SELECT 
            COUNT(*) as total_employees,
            COUNT(salary) as employees_with_salary
        FROM employees
    ''')
    print(cursor.fetchall())

    # Task 2: Simple Arithmetic and ROUND
    print("\nTask 2 - Monthly Salaries:")
    cursor.execute('''
        SELECT 
            name,
            ROUND(salary/12.0, 2) as monthly_salary
        FROM employees
    ''')
    print(cursor.fetchall())

    # Task 3: Basic JOIN and GROUP BY
    print("\nTask 3 - Employees per Department:")
    cursor.execute('''
        SELECT 
            d.dept_name,
            COUNT(e.emp_id) as employee_count
        FROM departments d
        LEFT JOIN employees e ON d.dept_id = e.department_id
        GROUP BY d.dept_name
    ''')
    print(cursor.fetchall())

    # Task 4: Multiple JOINs with NULL Handling
    print("\nTask 4 - Project Employee Hours:")
    cursor.execute('''
        SELECT 
            p.project_name,
            COALESCE(SUM(ep.hours_worked), 0) as total_hours
        FROM projects p
        LEFT JOIN employee_projects ep ON p.project_id = ep.project_id
        GROUP BY p.project_name
    ''')
    print(cursor.fetchall())

    # Task 5: Self Join with Aggregation
    print("\nTask 5 - Manager Reports:")
    cursor.execute('''
        SELECT 
            e1.name as employee,
            e2.name as manager,
            COUNT(e3.emp_id) as direct_reports
        FROM employees e1
        LEFT JOIN employees e2 ON e1.manager_id = e2.emp_id
        LEFT JOIN employees e3 ON e2.emp_id = e3.manager_id
        GROUP BY e1.emp_id
    ''')
    print(cursor.fetchall())

    # Additional tasks can be added as needed
    
def main():
    conn = create_database()
    run_tasks(conn)
    conn.close()

if __name__ == "__main__":
    main()