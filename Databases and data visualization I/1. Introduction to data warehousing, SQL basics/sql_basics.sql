-- Example SQL Script with Common Operations

-- Create a sample database
CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

-- Create departments table
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL UNIQUE,
    location VARCHAR(100),
    budget DECIMAL(15,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table with constraints
CREATE TABLE employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Insert sample data
INSERT INTO departments (dept_id, dept_name, location, budget)
VALUES 
    (1, 'HR', 'Building A', 500000.00),
    (2, 'IT', 'Building B', 1000000.00),
    (3, 'Sales', 'Building C', 750000.00);

-- Alter table example
ALTER TABLE employees
ADD COLUMN phone VARCHAR(20);

-- Update data example
UPDATE employees
SET salary = salary * 1.1
WHERE dept_id = 2;

-- Delete example
DELETE FROM employees
WHERE hire_date < '2020-01-01';

-- Create a view
CREATE VIEW employee_details AS
SELECT 
    e.emp_id,
    CONCAT(e.first_name, ' ', e.last_name) as full_name,
    d.dept_name,
    e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

-- Example of complex query using view
SELECT 
    dept_name,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employee_details
GROUP BY dept_name
HAVING avg_salary > 50000;