from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    professor_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    professor_id: Optional[int] = None

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True