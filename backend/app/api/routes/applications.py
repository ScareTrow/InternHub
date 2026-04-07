from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.application import EmployerApplicationRead, StudentApplicationRead
from app.services import application as application_service
from app.services.serializers import (
    serialize_employer_application,
    serialize_student_application,
)


router = APIRouter()


@router.get("/me", response_model=list[StudentApplicationRead])
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STUDENT)),
) -> list[StudentApplicationRead]:
    applications = application_service.list_student_applications(db, current_user)
    return [serialize_student_application(application) for application in applications]


@router.get("/employer", response_model=list[EmployerApplicationRead])
def list_employer_applications(
    vacancy_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYER)),
) -> list[EmployerApplicationRead]:
    applications = application_service.list_employer_applications(db, current_user, vacancy_id)
    return [serialize_employer_application(application) for application in applications]
