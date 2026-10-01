from sqlalchemy.orm import Session
from sqlalchemy import (
    asc,
    desc,
    func,
    or_
)

from database.models import Employee, Department


# =========================
# Create Employee
# =========================

def create_employee(
    db: Session,
    data
):

    employee = Employee(
        name=data.name,
        email=data.email,
        phone=data.phone,
        age=data.age,
        designation=data.designation,
        salary=data.salary,
        department_id=data.department_id,
        is_active=data.is_active,
        joining_date=data.joining_date
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# =========================
# Get Employee
# =========================

def get_employee(
    db: Session,
    employee_id: int
):

    return db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()


# =========================
# Get Employees
# =========================

def get_employees(
    db: Session,
    page: int,
    limit: int,
    department_id: int = None,
    designation: str = None,
    is_active: bool = None,
    search: str = None,
    sort_by: str = "created_at",
    sort_order: str = "asc"
):

    query = db.query(Employee)

    # Department filter
    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    # Designation filter
    if designation:
        query = query.filter(
            Employee.designation.ilike(
                f"%{designation}%"
            )
        )

    # Active filter
    if is_active is not None:
        query = query.filter(
            Employee.is_active == is_active
        )

    # Search
    if search:
        query = query.filter(
            or_(
                Employee.name.ilike(
                    f"%{search}%"
                ),
                Employee.email.ilike(
                    f"%{search}%"
                )
            )
        )

    # Sorting
    sort_columns = {
        "name": Employee.name,
        "salary": Employee.salary,
        "joining_date": Employee.joining_date,
        "created_at": Employee.created_at
    }

    column = sort_columns.get(sort_by)

    if sort_order == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))

    # Pagination
    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


# =========================
# Update Employee
# =========================

def update_employee(
    db: Session,
    employee: Employee,
    data
):

    employee.name = data.name
    employee.email = data.email
    employee.phone = data.phone
    employee.age = data.age
    employee.designation = data.designation
    employee.salary = data.salary
    employee.department_id = data.department_id
    employee.joining_date = data.joining_date
    employee.is_active = data.is_active

    db.commit()
    db.refresh(employee)

    return employee


# =========================
# Patch Employee
# =========================

def patch_employee(
    db: Session,
    employee: Employee,
    data
):

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# =========================
# Department Summary
# =========================

def department_summary(
    db: Session,
    department_id: int
):

    department = db.query(Department).filter(
        Department.department_id == department_id
    ).first()

    if not department:
        return None

    total = db.query(
        func.count(Employee.employee_id)
    ).filter(
        Employee.department_id == department_id
    ).scalar()

    active = db.query(
        func.count(Employee.employee_id)
    ).filter(
        Employee.department_id == department_id,
        Employee.is_active == True
    ).scalar()

    inactive = db.query(
        func.count(Employee.employee_id)
    ).filter(
        Employee.department_id == department_id,
        Employee.is_active == False
    ).scalar()

    average_salary = db.query(
        func.avg(Employee.salary)
    ).filter(
        Employee.department_id == department_id
    ).scalar()

    return {
        "department_id": department.department_id,
        "department_name": department.department_name,
        "total_employees": total or 0,
        "active_employees": active or 0,
        "inactive_employees": inactive or 0,
        "average_salary": round(
            average_salary, 2
        ) if average_salary else None
    }


# =========================
# Employee Statistics
# =========================

def employee_statistics(db: Session):

    total = db.query(
        func.count(Employee.employee_id)
    ).scalar()

    active = db.query(
        func.count(Employee.employee_id)
    ).filter(
        Employee.is_active == True
    ).scalar()

    inactive = db.query(
        func.count(Employee.employee_id)
    ).filter(
        Employee.is_active == False
    ).scalar()

    average = db.query(
        func.avg(Employee.salary)
    ).scalar()

    highest = db.query(
        func.max(Employee.salary)
    ).scalar()

    lowest = db.query(
        func.min(Employee.salary)
    ).scalar()

    return {
        "total_employees": total or 0,
        "active_employees": active or 0,
        "inactive_employees": inactive or 0,
        "average_salary": round(
            average, 2
        ) if average else None,
        "highest_salary": highest,
        "lowest_salary": lowest
    }