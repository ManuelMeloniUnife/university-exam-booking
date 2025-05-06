from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.exam import Exam
from app.schemas.exam import ExamCreate, ExamUpdate
from app.repositories.base import BaseRepository

class ExamRepository(BaseRepository[Exam, ExamCreate, ExamUpdate]):
    def get_by_course_id(self, db: Session, *, course_id: int, skip: int = 0, limit: int = 100) -> List[Exam]:
        return (
            db.query(Exam)
            .filter(Exam.course_id == course_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_active_exams(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Exam]:
        return (
            db.query(Exam)
            .filter(Exam.is_active == True, Exam.date >= datetime.now())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_upcoming_exams_by_course(self, db: Session, *, course_id: int, skip: int = 0, limit: int = 100) -> List[Exam]:
        return (
            db.query(Exam)
            .filter(Exam.course_id == course_id, Exam.is_active == True, Exam.date >= datetime.now())
            .offset(skip)
            .limit(limit)
            .all()
        )

exam_repository = ExamRepository(Exam)