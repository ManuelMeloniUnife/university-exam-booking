from fastapi import APIRouter
from app.api.endpoints import auth, users, courses, exams, bookings

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])