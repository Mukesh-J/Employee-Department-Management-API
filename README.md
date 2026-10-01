# Employee & Department Management API

## 1. Project Overview

The **Employee & Department Management API** is a FastAPI-based REST API developed using **Python, FastAPI, MySQL, SQLAlchemy, and Pydantic**.

This project manages departments and employees with a one-to-many relationship where one department can have multiple employees.

The API provides CRUD operations, pagination, searching, filtering, sorting, soft deletion, department summaries, and employee statistics.

---

## 2. Technologies Used

- Python
- FastAPI
- Uvicorn
- MySQL
- SQLAlchemy
- PyMySQL
- Pydantic
- Swagger UI

---

## 3. Project Features

### Department Management

- Create department
- View departments
- Search departments
- Filter active/inactive departments
- Pagination
- Sorting
- Get department by ID
- Update department using PUT
- Partially update department using PATCH
- Soft delete department
- View employees belonging to a department
- Department employee summary

### Employee Management

- Create employee
- View employees
- Search employee by name or email
- Filter by department
- Filter by designation
- Filter active/inactive employees
- Pagination
- Sorting by name, salary, joining date and creation date
- Get employee by ID
- Update employee using PUT
- Partially update employee using PATCH
- Validate email
- Validate age
- Validate salary
- Validate department
- Prevent duplicate employee email
- Employee statistics

---

## 4. Database Design

The project contains two main tables:

### Departments

| Column | Description |
|---|---|
| department_id | Primary key |
| department_name | Department name |
| description | Department description |
| is_active | Active/inactive status |
| created_at | Creation date/time |
| updated_at | Last update date/time |

### Employees

| Column | Description |
|---|---|
| employee_id | Primary key |
| name | Employee name |
| email | Employee email |
| phone | Employee phone |
| age | Employee age |
| designation | Employee designation |
| salary | Employee salary |
| department_id | Foreign key |
| is_active | Active/inactive status |
| joining_date | Joining date |
| created_at | Creation date/time |
| updated_at | Last update date/time |

### Relationship

One department can have many employees.

```text
Department
    |
    | 1
    |
    |-------------------<
                         |
                    Employees
                         |
                    department_id
```

The `department_id` column in the `employees` table is a foreign key referencing `departments.department_id`.

---

## 5. Project Structure

```text
task4/
│
├── main.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
│
├── schemas/
│   ├── __init__.py
│   ├── department.py
│   └── employee.py
│
├── routes/
│   ├── __init__.py
│   ├── department.py
│   └── employee.py
│
└── services/
    ├── __init__.py
    ├── department.py
    └── employee.py
```

---

## 6. API Endpoints

### Department APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/departments` | Create department |
| GET | `/departments` | Get departments |
| GET | `/departments/{department_id}` | Get department by ID |
| PUT | `/departments/{department_id}` | Full update |
| PATCH | `/departments/{department_id}` | Partial update |
| DELETE | `/departments/{department_id}` | Soft delete |
| GET | `/departments/{department_id}/employees` | Get department employees |
| GET | `/departments/{department_id}/summary` | Department summary |

### Employee APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/employees` | Create employee |
| GET | `/employees` | Get employees |
| GET | `/employees/{employee_id}` | Get employee with department |
| PUT | `/employees/{employee_id}` | Full update |
| PATCH | `/employees/{employee_id}` | Partial update |
| GET | `/employees/statistics` | Employee statistics |

---

## 7. API Validation

The API validates user input before
