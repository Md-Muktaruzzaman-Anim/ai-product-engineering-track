from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import List

# Dynamic module lookup within the same directory context
db_module = __import__("08_Working_with_Databases", fromlist=["engine", "Base", "get_db"])
models_module = __import__("08_models", fromlist=["Course", "User"])

engine = db_module.engine
Base = db_module.Base
get_db = db_module.get_db

Course = models_module.Course
User = models_module.User

# Automatically build tables in PostgreSQL if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI Application
app = FastAPI(title="Course Management API")

# --- Course Schemas ---
class CourseCreate(BaseModel):
    course_name: str = Field(..., min_length=2)
    instructor: str = Field(..., min_length=2)
    duration: float = Field(..., ge=0.5)
    website: str

class CourseResponse(BaseModel):
    id: int
    course_name: str
    instructor: str
    duration: float
    website: str

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# ----------------- COURSE ROUTES -----------------
@app.post("/courses_post/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course_data.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/courses/", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} was not found"
        )
    return course

# ----------------- USER ROUTES -----------------
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
