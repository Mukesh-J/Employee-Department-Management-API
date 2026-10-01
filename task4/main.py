from fastapi import FastAPI

from database.connection import Base, engine

from database import models

from routes.department import router as department_router
from routes.employee import router as employee_router


# Create database tables
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Employee & Department Management API",
    description="Day 4 FastAPI + MySQL + SQLAlchemy Project",
    version="1.0.0"
)


# Include routers
app.include_router(
    department_router
)

app.include_router(
    employee_router
)


@app.get("/")
def home():

    return {
        "message": "Employee & Department Management API is running"
    }