from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Employee, Department

from schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    EmployeePatch,
    EmployeeWithDepartment,
    EmployeeStatistics
)

from services import employee as employee_service


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# =========================
# POST /employees
# =========================

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    # Check department
    department = db.query(Department).filter(
        Department.department_id == data.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Check duplicate email
    existing = db.query(Employee).filter(
        Employee.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )

    return employee_service.create_employee(
        db,
        data
    )


# =========================
# GET /employees
# =========================

@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    department_id: int = Query(None, gt=0),
    designation: str = None,
    is_active: bool = None,
    search: str = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):

    valid_sort_fields = [
        "name",
        "salary",
        "joining_date",
        "created_at"
    ]

    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sorting field"
        )

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sorting order"
        )

    return employee_service.get_employees(
        db,
        page,
        limit,
        department_id,
        designation,
        is_active,
        search,
        sort_by,
        sort_order
    )


# =========================
# GET /employees/statistics
# =========================

@router.get(
    "/statistics",
    response_model=EmployeeStatistics
)
def employee_statistics(
    db: Session = Depends(get_db)
):

    return employee_service.employee_statistics(
        db
    )


# =========================
# GET /employees/{id}
# =========================

@router.get(
    "/{employee_id}",
    response_model=EmployeeWithDepartment
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid employee ID"
        )

    employee = employee_service.get_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# =========================
# PUT /employees/{id}
# =========================

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    employee = employee_service.get_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check department
    department = db.query(Department).filter(
        Department.department_id == data.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Check duplicate email
    duplicate = db.query(Employee).filter(
        Employee.email == data.email,
        Employee.employee_id != employee_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )

    return employee_service.update_employee(
        db,
        employee,
        data
    )


# =========================
# PATCH /employees/{id}
# =========================

@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def patch_employee(
    employee_id: int,
    data: EmployeePatch,
    db: Session = Depends(get_db)
):

    employee = employee_service.get_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check department only if provided
    if data.department_id is not None:

        department = db.query(Department).filter(
            Department.department_id == data.department_id
        ).first()

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    # Check email only if provided
    if data.email is not None:

        duplicate = db.query(Employee).filter(
            Employee.email == data.email,
            Employee.employee_id != employee_id
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Employee email already exists"
            )

    return employee_service.patch_employee(
        db,
        employee,
        data
    )