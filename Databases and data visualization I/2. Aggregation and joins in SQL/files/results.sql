SELECT 
    COUNT(*) as total_employees,
    COUNT(salary) as employees_with_salary
FROM employees;

SELECT 
    name,
    salary as annual_salary,
    ROUND(salary/12, 2) as monthly_salary
FROM employees;

SELECT 
    d.dept_name,
    COUNT(e.emp_id) as employee_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_name;

SELECT 
    p.project_name,
    e.name,
    COALESCE(ep.hours_worked, 0) as hours_worked
FROM projects p
LEFT JOIN employee_projects ep ON p.project_id = ep.project_id
LEFT JOIN employees e ON ep.emp_id = e.emp_id;


SELECT 
    e1.name as employee_name,
    e2.name as manager_name,
    COUNT(e3.emp_id) as manager_direct_reports
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.emp_id
LEFT JOIN employees e3 ON e2.emp_id = e3.manager_id
GROUP BY e1.name, e2.name;

SELECT DISTINCT d.dept_name
FROM departments d
INNER JOIN employees e ON d.dept_id = e.department_id
WHERE d.dept_id NOT IN (
    SELECT dept_id 
    FROM projects 
    WHERE budget > 0
);


WITH employee_costs AS (
    SELECT 
        p.project_id,
        p.dept_id,
        SUM(ep.hours_worked * (e.salary/2080)) as labor_cost
    FROM projects p
    JOIN employee_projects ep ON p.project_id = ep.project_id
    JOIN employees e ON ep.emp_id = e.emp_id
    GROUP BY p.project_id, p.dept_id
)
SELECT 
    d.dept_name,
    ROUND(SUM(ec.labor_cost) * 100.0 / SUM(p.budget), 2) as budget_utilization_percentage
FROM departments d
JOIN projects p ON d.dept_id = p.dept_id
JOIN employee_costs ec ON p.project_id = ec.project_id
GROUP BY d.dept_name;


SELECT e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT p.project_id
    FROM projects p
    WHERE p.dept_id = e.department_id
    AND NOT EXISTS (
        SELECT 1
        FROM employee_projects ep
        WHERE ep.project_id = p.project_id
        AND ep.emp_id = e.emp_id
    )
);


SELECT 
    d.dept_name,
    COUNT(DISTINCT e.emp_id) as employee_count,
    COUNT(DISTINCT p.project_id) as project_count,
    COALESCE(SUM(e.salary), 0) as salary_budget,
    COALESCE(SUM(p.budget), 0) as project_budget
FROM departments d
FULL JOIN employees e ON d.dept_id = e.department_id
FULL JOIN projects p ON d.dept_id = p.dept_id
GROUP BY d.dept_name;


WITH dept_metrics AS (
    SELECT 
        d.dept_id,
        d.dept_name,
        AVG(e.salary) as avg_salary,
        SUM(p.budget) / NULLIF(COUNT(DISTINCT e.emp_id), 0) as budget_per_employee,
        COUNT(DISTINCT e.emp_id) as emp_count
    FROM departments d
    JOIN employees e ON d.dept_id = e.department_id
    LEFT JOIN projects p ON d.dept_id = p.dept_id
    GROUP BY d.dept_id, d.dept_name
),
employee_project_counts AS (
    SELECT 
        e.department_id,
        e.emp_id,
        COUNT(DISTINCT ep.project_id) as project_count
    FROM employees e
    LEFT JOIN employee_projects ep ON e.emp_id = ep.emp_id
    GROUP BY e.department_id, e.emp_id
)
SELECT 
    dm.dept_name,
    ROUND(dm.avg_salary, 2) as avg_salary,
    ROUND(dm.budget_per_employee, 2) as budget_per_employee,
    ROUND(dm.avg_salary / NULLIF(dm.budget_per_employee, 0), 2) as salary_to_budget_ratio
FROM dept_metrics dm
WHERE NOT EXISTS (
    SELECT 1 
    FROM employee_project_counts epc
    WHERE epc.department_id = dm.dept_id
    AND epc.project_count < 2
)
AND dm.avg_salary > dm.budget_per_employee
ORDER BY salary_to_budget_ratio DESC;
