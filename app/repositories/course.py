from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories.base import BaseRepository

class CourseRepository(BaseRepository[Course, CourseCreate, CourseUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Course]:
        return db.query(Course).filter(Course.code == code).first()
    
    def get_by_professor_id(self, db: Session, *, professor_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        return (
            db.query(Course)
            .filter(Course.professor_id == professor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

course_repository = CourseRepository(Course)