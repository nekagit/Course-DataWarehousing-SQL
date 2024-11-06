# SQL Practice Tasks - From Basic to Advanced

## Sample Tables
-- Employees table
CREATE TABLE employees (
    emp_id INT,
    name VARCHAR(50),
    salary DECIMAL(10,2),
    department_id INT,
    manager_id INT,
    hire_date DATE
);

-- Departments table
CREATE TABLE departments (
    dept_id INT,
    dept_name VARCHAR(50),
    location VARCHAR(50)
);

-- Projects table
CREATE TABLE projects (
    project_id INT,
    project_name VARCHAR(50),
    budget DECIMAL(10,2),
    dept_id INT
);

-- Employee_Projects table
CREATE TABLE employee_projects (
    emp_id INT,
    project_id INT,
    hours_worked DECIMAL(10,2)
);

## Task 1 - Basic COUNT and NULL Handling (Easy)
-- Task: Find the total number of employees and how many employees have a salary value.

## Task 2 - Simple Arithmetic and ROUND (Easy)
-- Task: Calculate the monthly salary (annual salary divided by 12) for each employee, rounded to 2 decimal places.

## Task 3 - Basic JOIN and GROUP BY (Easy-Medium)
-- Task: Show the number of employees in each department, including department name.

## Task 4 - Multiple JOINs with NULL Handling (Medium)
-- Task: Find all projects and their assigned employees. For projects with no employees or employees with no hours logged, show 0.

## Task 5 - Self Join with Aggregation (Medium)
-- Task: For each employee, show their name, their manager's name, and their manager's total number of direct reports.

## Task 6 - Subquery with Set Theory (Medium-Hard)
-- Task: Find all departments that have employees but no active projects.

## Task 7 - Complex Aggregation with Multiple JOINs (Hard)
-- Task: Calculate the percentage of total project budget consumed by each department, considering employee hours worked and their hourly rate (salary/2080).

## Task 8 - Semi Join with Complex Conditions (Hard)
-- Task: Find employees who have worked on all projects in their department.

## Task 9 - Full Join with Conditional Aggregation (Hard)
-- Task: Create a department summary showing total salary budget, total project budget, number of employees, and number of projects, including departments with no employees or projects.

## Task 10 - Advanced Analysis with All Concepts (Very Hard)
-- Task: Find departments where the average employee salary is higher than the department's project budget per employee, and show the salary to budget ratio, but only include departments where all employees are assigned to at least 2 projects.
