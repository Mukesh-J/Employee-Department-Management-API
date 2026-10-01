from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:root@localhost/day4_employee_db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()