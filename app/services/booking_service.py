from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.booking import booking_repository
from app.repositories.exam import exam_repository
from app.repositories.user import user_repository
from app.schemas.booking import BookingCreate, BookingUpdate, Booking
from app.models.user import UserRole
from datetime import datetime

class BookingService:
    def create_booking(self, db: Session, booking_in: BookingCreate) -> Booking:
        # Verifica se lo studente esiste ed è effettivamente uno studente
        student = user_repository.get(db, id=booking_in.student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail="Studente non trovato",
            )
        if student.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=400,
                detail="L'utente non è uno studente",
            )
        
        # Verifica se l'esame esiste
        exam = exam_repository.get(db, id=booking_in.exam_id)
        if not exam:
            raise HTTPException(
                status_code=404,
                detail="Esame non trovato",
            )
        
        # Verifica se l'esame è attivo
        if not exam.is_active:
            raise HTTPException(
                status_code=400,
                detail="L'esame non è attivo",
            )
        
        # Verifica se l'esame è nel futuro
        if exam.date < datetime.now():
            raise HTTPException(
                status_code=400,
                detail="L'esame è già passato",
            )
        
        # Verifica se lo studente è già iscritto all'esame
        existing_booking = booking_repository.get_by_student_and_exam(
            db, student_id=booking_in.student_id, exam_id=booking_in.exam_id
        )
        if existing_booking:
            raise HTTPException(
                status_code=400,
                detail="Lo studente è già iscritto all'esame",
            )
        
        # Verifica se c'è ancora posto disponibile
        current_bookings = booking_repository.count_by_exam_id(db, exam_id=booking_in.exam_id)
        if current_bookings >= exam.max_students:
            raise HTTPException(
                status_code=400,
                detail="Non ci sono più posti disponibili per questo esame",
            )
        
        return booking_repository.create(db, obj_in=booking_in)
    
    def get_booking(self, db: Session, booking_id: int) -> Booking:
        booking = booking_repository.get(db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return booking
    
    def get_bookings(self, db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
        return booking_repository.get_multi(db, skip=skip, limit=limit)
    
    def get_bookings_by_student(self, db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        # Verifica se lo studente esiste
        student = user_repository.get(db, id=student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail="Studente non trovato",
            )
        
        return booking_repository.get_by_student_id(db, student_id=student_id, skip=skip, limit=limit)
    
    def get_bookings_by_exam(self, db: Session, exam_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        # Verifica se l'esame esiste
        exam = exam_repository.get(db, id=exam_id)
        if not exam:
            raise HTTPException(
                status_code=404,
                detail="Esame non trovato",
            )
        
        return booking_repository.get_by_exam_id(db, exam_id=exam_id, skip=skip, limit=limit)
    
    def count_bookings_by_exam(self, db: Session, exam_id: int) -> int:
        # Verifica se l'esame esiste
        exam = exam_repository.get(db, id=exam_id)
        if not exam:
            raise HTTPException(
                status_code=404,
                detail="Esame non trovato",
            )
        
        return booking_repository.count_by_exam_id(db, exam_id=exam_id)
    
    def update_booking(self, db: Session, booking_id: int, booking_in: BookingUpdate) -> Booking:
        booking = booking_repository.get(db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        
        return booking_repository.update(db, db_obj=booking, obj_in=booking_in)
    
    def delete_booking(self, db: Session, booking_id: int) -> Booking:
        booking = booking_repository.get(db, id=booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return booking_repository.remove(db, id=booking_id)
    
    def cancel_booking(self, db: Session, student_id: int, exam_id: int) -> None:
        booking = booking_repository.get_by_student_and_exam(db, student_id=student_id, exam_id=exam_id)
        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Prenotazione non trovata",
            )
        
        booking_repository.remove(db, id=booking.id)

booking_service = BookingService()