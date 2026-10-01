from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# Create Department
# =========================

class DepartmentCreate(BaseModel):

    department_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = None


# =========================
# Complete Update
# =========================

class DepartmentUpdate(BaseModel):

    department_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = None

    is_active: bool


# =========================
# Partial Update
# =========================

class DepartmentPatch(BaseModel):

    department_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None


# =========================
# Response
# =========================

class DepartmentResponse(BaseModel):

    department_id: int
    department_name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True