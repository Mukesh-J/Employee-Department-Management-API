from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


# =========================
# Department Model
# =========================

class Department(Base):

    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # One Department -> Many Employees
    employees = relationship(
        "Employee",
        back_populates="department"
    )


# =========================
# Employee Model
# =========================

class Employee(Base):

    __tablename__ = "employees"

    employee_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    designation = Column(
        String(100),
        nullable=False
    )

    salary = Column(
        Float,
        nullable=False
    )

    # Foreign Key
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    joining_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Many Employees -> One Department
    department = relationship(
        "Department",
        back_populates="employees"
    )