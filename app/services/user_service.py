from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate, User
from app.models.user import UserRole

class UserService:
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        # Verifica se l'email è già utilizzata
        db_user = user_repository.get_by_email(db, email=user_in.email)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="L'email è già registrata nel sistema.",
            )
        
        # Verifica se lo student_id è già utilizzato (se fornito)
        if user_in.student_id:
            db_student = user_repository.get_by_student_id(db, student_id=user_in.student_id)
            if db_student:
                raise HTTPException(
                    status_code=400,
                    detail="L'ID studente è già registrato nel sistema.",
                )
        
        return user_repository.create(db, obj_in=user_in)
    
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        user = user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        return user
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return user_repository.get_multi(db, skip=skip, limit=limit)
    
    def update_user(self, db: Session, user_id: int, user_in: UserUpdate) -> User:
        user = user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        
        # Verifica se l'email è già utilizzata da un altro utente
        if user_in.email and user_in.email != user.email:
            db_user = user_repository.get_by_email(db, email=user_in.email)
            if db_user:
                raise HTTPException(
                    status_code=400,
                    detail="L'email è già registrata nel sistema.",
                )
        
        # Verifica se lo student_id è già utilizzato da un altro utente (se fornito)
        if user_in.student_id and user_in.student_id != user.student_id:
            db_student = user_repository.get_by_student_id(db, student_id=user_in.student_id)
            if db_student:
                raise HTTPException(
                    status_code=400,
                    detail="L'ID studente è già registrato nel sistema.",
                )
        
        return user_repository.update(db, db_obj=user, obj_in=user_in)
    
    def delete_user(self, db: Session, user_id: int) -> User:
        user = user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        return user_repository.remove(db, id=user_id)
    
    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        user = user_repository.authenticate(db, email=email, password=password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Email o password non corretti",
            )
        return user

user_service = UserService()