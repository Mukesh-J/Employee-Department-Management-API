from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Department

from schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    DepartmentPatch
)

from schemas.employee import (
    EmployeeWithDepartment,
    DepartmentSummary
)

from services import department as department_service
from services import employee as employee_service


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# =========================
# POST /departments
# =========================

@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=201
)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    department = department_service.create_department(
        db,
        data.department_name,
        data.description
    )

    if not department:
        raise HTTPException(
            status_code=409,
            detail="Department already exists"
        )

    return department


# =========================
# GET /departments
# =========================

@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def get_departments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = None,
    is_active: bool = None,
    sort_by: str = "department_id",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):

    valid_sort_fields = [
        "department_id",
        "department_name",
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

    return department_service.get_departments(
        db,
        page,
        limit,
        search,
        is_active,
        sort_by,
        sort_order
    )


# =========================
# GET /departments/{id}
# =========================

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    if department_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid department ID"
        )

    department = department_service.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# =========================
# PUT /departments/{id}
# =========================

@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    department = department_service.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    duplicate = db.query(Department).filter(
        Department.department_name == data.department_name,
        Department.department_id != department_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Department name already exists"
        )

    return department_service.update_department(
        db,
        department,
        data
    )


# =========================
# PATCH /departments/{id}
# =========================

@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse
)
def patch_department(
    department_id: int,
    data: DepartmentPatch,
    db: Session = Depends(get_db)
):

    department = department_service.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    if data.department_name:

        duplicate = db.query(Department).filter(
            Department.department_name == data.department_name,
            Department.department_id != department_id
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Department name already exists"
            )

    return department_service.patch_department(
        db,
        department,
        data
    )


# =========================
# DELETE /departments/{id}
# =========================

@router.delete(
    "/{department_id}",
    response_model=DepartmentResponse
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    department = department_service.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department_service.delete_department(
        db,
        department
    )


# =========================
# Department Employees
# =========================

@router.get(
    "/{department_id}/employees",
    response_model=list[EmployeeWithDepartment]
)
def department_employees(
    department_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = None,
    is_active: bool = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):

    department = department_service.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

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
        None,
        is_active,
        search,
        sort_by,
        sort_order
    )


# =========================
# Department Summary
# =========================

@router.get(
    "/{department_id}/summary",
    response_model=DepartmentSummary
)
def department_summary(
    department_id: int,
    db: Session = Depends(get_db)
):

    result = employee_service.department_summary(
        db,
        department_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return result