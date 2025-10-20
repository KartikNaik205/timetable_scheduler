from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from .models import SessionLocal, Instructor, Room, Group, Course
from .database import get_db
from .scheduler import generate_weekly_timetable, time_slots

app = FastAPI(title="Timetable Scheduler API")

# -------------------------------
# CORS (Frontend Access)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Root + Timetable Routes
# -------------------------------
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}


@app.get("/generate_timetable")
def get_timetable(db: Session = Depends(get_db)):
    """Generate a full week’s timetable in JSON format."""
    try:
        timetable = generate_weekly_timetable()
        formatted_timetable = {
            day: [{"time": t, "subject": s} for t, s in zip(time_slots, subjects)]
            for day, subjects in timetable.items()
        }
        return {"timetable": formatted_timetable}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Pydantic Schemas
# -------------------------------
class InstructorCreate(BaseModel):
    name: str


class RoomCreate(BaseModel):
    name: str


class GroupCreate(BaseModel):
    name: str


class CourseCreate(BaseModel):
    code: str
    title: str
    hours_per_week: int
    instructor_id: int
    group_id: int


# -------------------------------
# CRUD: Instructor
# -------------------------------
@app.post("/instructors/", response_model=dict)
def create_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = Instructor(name=instructor.name)
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return {"id": db_instructor.id, "name": db_instructor.name}


@app.get("/instructors/", response_model=List[dict])
def read_instructors(db: Session = Depends(get_db)):
    return [{"id": i.id, "name": i.name} for i in db.query(Instructor).all()]


@app.put("/instructors/{instructor_id}", response_model=dict)
def update_instructor(instructor_id: int, instructor: InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not db_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db_instructor.name = instructor.name
    db.commit()
    db.refresh(db_instructor)
    return {"id": db_instructor.id, "name": db_instructor.name}


@app.delete("/instructors/{instructor_id}", response_model=dict)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not db_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db.delete(db_instructor)
    db.commit()
    return {"message": "Instructor deleted successfully"}


# -------------------------------
# CRUD: Room
# -------------------------------
@app.post("/rooms/", response_model=dict)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return {"id": db_room.id, "name": db_room.name}


@app.get("/rooms/", response_model=List[dict])
def read_rooms(db: Session = Depends(get_db)):
    return [{"id": r.id, "name": r.name} for r in db.query(Room).all()]


@app.put("/rooms/{room_id}", response_model=dict)
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db_room.name = room.name
    db.commit()
    db.refresh(db_room)
    return {"id": db_room.id, "name": db_room.name}


@app.delete("/rooms/{room_id}", response_model=dict)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted successfully"}


# -------------------------------
# CRUD: Group
# -------------------------------
@app.post("/groups/", response_model=dict)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return {"id": db_group.id, "name": db_group.name}


@app.get("/groups/", response_model=List[dict])
def read_groups(db: Session = Depends(get_db)):
    return [{"id": g.id, "name": g.name} for g in db.query(Group).all()]


@app.put("/groups/{group_id}", response_model=dict)
def update_group(group_id: int, group: GroupCreate, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_group.name = group.name
    db.commit()
    db.refresh(db_group)
    return {"id": db_group.id, "name": db_group.name}


@app.delete("/groups/{group_id}", response_model=dict)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(db_group)
    db.commit()
    return {"message": "Group deleted successfully"}


# -------------------------------
# CRUD: Course
# -------------------------------
@app.post("/courses/", response_model=dict)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        code=course.code,
        title=course.title,
        hours_per_week=course.hours_per_week,
        instructor_id=course.instructor_id,
        group_id=course.group_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return {
        "id": db_course.id,
        "code": db_course.code,
        "title": db_course.title,
        "hours_per_week": db_course.hours_per_week,
        "instructor_id": db_course.instructor_id,
        "group_id": db_course.group_id
    }


@app.get("/courses/", response_model=List[dict])
def read_courses(db: Session = Depends(get_db)):
    return [
        {
            "id": c.id,
            "code": c.code,
            "title": c.title,
            "hours_per_week": c.hours_per_week,
            "instructor_id": c.instructor_id,
            "group_id": c.group_id
        }
        for c in db.query(Course).all()
    ]


@app.put("/courses/{course_id}", response_model=dict)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course.code = course.code
    db_course.title = course.title
    db_course.hours_per_week = course.hours_per_week
    db_course.instructor_id = course.instructor_id
    db_course.group_id = course.group_id
    db.commit()
    db.refresh(db_course)
    return {"message": "Course updated successfully"}


@app.delete("/courses/{course_id}", response_model=dict)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}
