from typing import List
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.exam import exam_repository
from app.repositories.course import course_repository
from app.schemas.exam import ExamCreate, ExamUpdate, Exam

class ExamService:
    def create_exam(self, db: Session, exam_in: ExamCreate) -> Exam:
        # Verifica se il corso esiste
        course = course_repository.get(db, id=exam_in.course_id)
        if not course:
            raise HTTPException(
                status_code=404,
                detail="Corso non trovato",
            )
        
        # Verifica se la data dell'esame è nel futuro
        if exam_in.date < datetime.now():
            raise HTTPException(
                status_code=400,
                detail="La data dell'esame deve essere nel futuro",
            )
        
        # Verifica che il numero massimo di studenti sia positivo
        if exam_in.max_students <= 0:
            raise HTTPException(
                status_code=400,
                detail="Il numero massimo di studenti deve essere positivo",
            )
        
        return exam_repository.create(db, obj_in=exam_in)
    
    def get_exam(self, db: Session, exam_id: int) -> Exam:
        exam = exam_repository.get(db, id=exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Esame non trovato")
        return exam
    
    def get_exams(self, db: Session, skip: int = 0, limit: int = 100) -> List[Exam]:
        return exam_repository.get_multi(db, skip=skip, limit=limit)
    
    def get_active_exams(self, db: Session, skip: int = 0, limit: int = 100) -> List[Exam]:
        return exam_repository.get_active_exams(db, skip=skip, limit=limit)
    
    def get_exams_by_course(self, db: Session, course_id: int, skip: int = 0, limit: int = 100) -> List[Exam]:
        # Verifica se il corso esiste
        course = course_repository.get(db, id=course_id)
        if not course:
            raise HTTPException(
                status_code=404,
                detail="Corso non trovato",
            )
        
        return exam_repository.get_by_course_id(db, course_id=course_id, skip=skip, limit=limit)
    
    def get_upcoming_exams_by_course(self, db: Session, course_id: int, skip: int = 0, limit: int = 100) -> List[Exam]:
        # Verifica se il corso esiste
        course = course_repository.get(db, id=course_id)
        if not course:
            raise HTTPException(
                status_code=404,
                detail="Corso non trovato",
            )
        
        return exam_repository.get_upcoming_exams_by_course(db, course_id=course_id, skip=skip, limit=limit)
    
    def update_exam(self, db: Session, exam_id: int, exam_in: ExamUpdate) -> Exam:
        exam = exam_repository.get(db, id=exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Esame non trovato")
        
        # Verifica se la data dell'esame è nel futuro (se fornita)
        if exam_in.date and exam_in.date < datetime.now():
            raise HTTPException(
                status_code=400,
                detail="La data dell'esame deve essere nel futuro",
            )
        
        # Verifica che il numero massimo di studenti sia positivo (se fornito)
        if exam_in.max_students is not None and exam_in.max_students <= 0:
            raise HTTPException(
                status_code=400,
                detail="Il numero massimo di studenti deve essere positivo",
            )
        
        return exam_repository.update(db, db_obj=exam, obj_in=exam_in)
    
    def delete_exam(self, db: Session, exam_id: int) -> Exam:
        exam = exam_repository.get(db, id=exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Esame non trovato")
        return exam_repository.remove(db, id=exam_id)

exam_service = ExamService()