from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.course import course_repository
from app.repositories.user import user_repository
from app.schemas.course import CourseCreate, CourseUpdate, Course
from app.models.user import UserRole

class CourseService:
    def create_course(self, db: Session, course_in: CourseCreate) -> Course:
        # Verifica se il codice del corso è già utilizzato
        db_course = course_repository.get_by_code(db, code=course_in.code)
        if db_course:
            raise HTTPException(
                status_code=400,
                detail="Il codice del corso è già registrato nel sistema.",
            )
        
        # Verifica se il professore esiste ed è effettivamente un professore
        professor = user_repository.get(db, id=course_in.professor_id)
        if not professor:
            raise HTTPException(
                status_code=404,
                detail="Professore non trovato",
            )
        if professor.role != UserRole.PROFESSOR:
            raise HTTPException(
                status_code=400,
                detail="L'utente assegnato non è un professore",
            )
        
        return course_repository.create(db, obj_in=course_in)
    
    def get_course(self, db: Session, course_id: int) -> Optional[Course]:
        course = course_repository.get(db, id=course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Corso non trovato")
        return course
    
    def get_courses(self, db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return course_repository.get_multi(db, skip=skip, limit=limit)
    
    def get_courses_by_professor(self, db: Session, professor_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        # Verifica se il professore esiste
        professor = user_repository.get(db, id=professor_id)
        if not professor:
            raise HTTPException(
                status_code=404,
                detail="Professore non trovato",
            )
        if professor.role != UserRole.PROFESSOR:
            raise HTTPException(
                status_code=400,
                detail="L'utente assegnato non è un professore",
            )
        
        return course_repository.get_by_professor_id(db, professor_id=professor_id, skip=skip, limit=limit)
    
    def update_course(self, db: Session, course_id: int, course_in: CourseUpdate) -> Course:
        course = course_repository.get(db, id=course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Corso non trovato")
        
        # Verifica se il codice del corso è già utilizzato
        if course_in.code and course_in.code != course.code:
            db_course = course_repository.get_by_code(db, code=course_in.code)
            if db_course:
                raise HTTPException(
                    status_code=400,
                    detail="Il codice del corso è già registrato nel sistema.",
                )
        
        # Verifica se il professore esiste ed è effettivamente un professore
        if course_in.professor_id:
            professor = user_repository.get(db, id=course_in.professor_id)
            if not professor:
                raise HTTPException(
                    status_code=404,
                    detail="Professore non trovato",
                )
            if professor.role != UserRole.PROFESSOR:
                raise HTTPException(
                    status_code=400,
                    detail="L'utente assegnato non è un professore",
                )
        
        return course_repository.update(db, db_obj=course, obj_in=course_in)
    
    def delete_course(self, db: Session, course_id: int) -> Course:
        course = course_repository.get(db, id=course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Corso non trovato")
        return course_repository.remove(db, id=course_id)

course_service = CourseService()