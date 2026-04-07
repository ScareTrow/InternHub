from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.enums import UserRole, VacancyType
from app.models.user import User
from app.schemas.application import ApplicationCreate, StudentApplicationRead
from app.schemas.vacancy import VacancyCreate, VacancyFilters, VacancyListResponse, VacancyRead, VacancyUpdate
from app.services import application as application_service
from app.services import vacancy as vacancy_service
from app.services.serializers import serialize_student_application, serialize_vacancy


router = APIRouter()


@router.get("/", response_model=VacancyListResponse)
def list_vacancies(
    title: str | None = Query(default=None),
    category: str | None = Query(default=None),
    location: str | None = Query(default=None),
    employment_type: VacancyType | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> VacancyListResponse:
    filters = VacancyFilters(
        title=title,
        category=category,
        location=location,
        employment_type=employment_type,
        page=page,
        page_size=page_size,
    )
    return vacancy_service.list_vacancies(db, filters)


@router.get("/me/list", response_model=list[VacancyRead])
def list_my_vacancies(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYER)),
) -> list[VacancyRead]:
    vacancies = vacancy_service.list_employer_vacancies(db, current_user)
    return [serialize_vacancy(vacancy) for vacancy in vacancies]


@router.post("/", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
def create_vacancy(
    payload: VacancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYER)),
) -> VacancyRead:
    vacancy = vacancy_service.create_vacancy(db, current_user, payload)
    return serialize_vacancy(vacancy)


@router.get("/{vacancy_id}", response_model=VacancyRead)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)) -> VacancyRead:
    vacancy = vacancy_service.get_vacancy_or_404(db, vacancy_id)
    return serialize_vacancy(vacancy)


@router.put("/{vacancy_id}", response_model=VacancyRead)
def update_vacancy(
    vacancy_id: int,
    payload: VacancyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYER)),
) -> VacancyRead:
    vacancy = vacancy_service.update_vacancy(db, current_user, vacancy_id, payload)
    return serialize_vacancy(vacancy)


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYER)),
) -> Response:
    vacancy_service.delete_vacancy(db, current_user, vacancy_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{vacancy_id}/apply", response_model=StudentApplicationRead, status_code=status.HTTP_201_CREATED)
def apply_to_vacancy(
    vacancy_id: int,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STUDENT)),
) -> StudentApplicationRead:
    application = application_service.apply_to_vacancy(db, current_user, vacancy_id, payload)
    return serialize_student_application(application)
