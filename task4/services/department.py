from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database.models import Department


# =========================
# Create Department
# =========================

def create_department(
    db: Session,
    department_name: str,
    description: str
):

    existing = db.query(Department).filter(
        Department.department_name == department_name
    ).first()

    if existing:
        return None

    department = Department(
        department_name=department_name,
        description=description,
        is_active=True
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


# =========================
# Get Department
# =========================

def get_department(
    db: Session,
    department_id: int
):

    return db.query(Department).filter(
        Department.department_id == department_id
    ).first()


# =========================
# Get Departments
# =========================

def get_departments(
    db: Session,
    page: int,
    limit: int,
    search: str = None,
    is_active: bool = None,
    sort_by: str = "department_id",
    sort_order: str = "asc"
):

    query = db.query(Department)

    # Search
    if search:
        query = query.filter(
            Department.department_name.ilike(
                f"%{search}%"
            )
        )

    # Active filter
    if is_active is not None:
        query = query.filter(
            Department.is_active == is_active
        )

    # Sorting
    sort_columns = {
        "department_id": Department.department_id,
        "department_name": Department.department_name,
        "created_at": Department.created_at
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
# Update Department
# =========================

def update_department(
    db: Session,
    department: Department,
    data
):

    department.department_name = data.department_name
    department.description = data.description
    department.is_active = data.is_active

    db.commit()
    db.refresh(department)

    return department


# =========================
# Patch Department
# =========================

def patch_department(
    db: Session,
    department: Department,
    data
):

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


# =========================
# Soft Delete
# =========================

def delete_department(
    db: Session,
    department: Department
):

    department.is_active = False

    db.commit()
    db.refresh(department)

    return department