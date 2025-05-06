from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    student_id: int
    exam_id: int
    confirmed: bool = True

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    confirmed: Optional[bool] = None

class Booking(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True