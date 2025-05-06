from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate
from app.repositories.base import BaseRepository

class BookingRepository(BaseRepository[Booking, BookingCreate, BookingUpdate]):
    def get_by_student_and_exam(self, db: Session, *, student_id: int, exam_id: int) -> Optional[Booking]:
        return (
            db.query(Booking)
            .filter(Booking.student_id == student_id, Booking.exam_id == exam_id)
            .first()
        )
    
    def get_by_student_id(self, db: Session, *, student_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return (
            db.query(Booking)
            .filter(Booking.student_id == student_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_exam_id(self, db: Session, *, exam_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return (
            db.query(Booking)
            .filter(Booking.exam_id == exam_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_by_exam_id(self, db: Session, *, exam_id: int) -> int:
        return (
            db.query(Booking)
            .filter(Booking.exam_id == exam_id, Booking.confirmed == True)
            .count()
        )

booking_repository = BookingRepository(Booking)