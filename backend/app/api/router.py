from fastapi import APIRouter

from app.api.routes import applications, auth, vacancies


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["vacancies"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
