from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- database URL format ---
#mysql+pymysql://<username>:<password>@<host>:<part>/<database_name>
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:k%40rtikn%40ik@localhost/timetable_db"

# --- create database engine --- 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# --- create session for database integration ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base class for ORM models ---
Base = declarative_base()

# --- Dependency for FastAPI routs to access DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
