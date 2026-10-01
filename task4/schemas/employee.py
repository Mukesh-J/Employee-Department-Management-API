from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime


# =========================
# Department Nested Response
# =========================

class DepartmentNested(BaseModel):
    department_id: int
    department_name: str

    class Config:
        from_attributes = True


# =========================
# Create Employee
# =========================

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    age: int = Field(..., ge=18, le=100)
    designation: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)
    department_id: int = Field(..., gt=0)
    joining_date: date
    is_active: bool = True


# =========================
# Complete Update
# =========================

class EmployeeUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    age: int = Field(..., ge=18, le=100)
    designation: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)
    department_id: int = Field(..., gt=0)
    joining_date: date
    is_active: bool


# =========================
# Partial Update
# =========================

class EmployeePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=100)
    designation: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    department_id: Optional[int] = Field(None, gt=0)
    joining_date: Optional[date] = None
    is_active: Optional[bool] = None


# =========================
# Normal Employee Response
# =========================

class EmployeeResponse(BaseModel):
    employee_id: int
    name: str
    email: str
    phone: Optional[str]
    age: int
    designation: str
    salary: float
    department_id: int
    is_active: bool
    joining_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# Employee + Department
# =========================

class EmployeeWithDepartment(BaseModel):
    employee_id: int
    name: str
    email: str
    phone: Optional[str]
    age: int
    designation: str
    salary: float

    department: DepartmentNested

    is_active: bool
    joining_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# Department Summary
# =========================

class DepartmentSummary(BaseModel):
    department_id: int
    department_name: str
    total_employees: int
    active_employees: int
    inactive_employees: int
    average_salary: Optional[float]


# =========================
# Employee Statistics
# =========================

class EmployeeStatistics(BaseModel):
    total_employees: int
    active_employees: int
    inactive_employees: int
    average_salary: Optional[float]
    highest_salary: Optional[float]
    lowest_salary: Optional[float]