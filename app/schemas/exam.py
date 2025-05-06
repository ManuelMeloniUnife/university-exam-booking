from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ExamBase(BaseModel):
    course_id: int
    date: datetime
    location: str
    max_students: int
    description: Optional[str] = None
    is_active: bool = True

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    date: Optional[datetime] = None
    location: Optional[str] = None
    max_students: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Exam(ExamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True