from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import urllib.parse

DB_USER = "root"
DB_PASS = "k@rtikn@ik"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "timetable_db"

# URL-encode password to handle special characters
DB_PASS_ENCODED = urllib.parse.quote_plus(DB_PASS)

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Tables
class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    instructor = relationship("Instructor")
    group = relationship("Group")

# Create tables
Base.metadata.create_all(bind=engine)
