import math

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.common import PaginationMeta
from app.schemas.vacancy import VacancyCreate, VacancyFilters, VacancyListResponse, VacancyUpdate
from app.services.serializers import serialize_vacancy


VACANCY_LOAD_OPTIONS = (
    joinedload(Vacancy.employer).joinedload(User.employer_profile),
    selectinload(Vacancy.applications),
)


def _apply_filters(statement, filters: VacancyFilters):
    if filters.title:
        statement = statement.where(Vacancy.title.ilike(f"%{filters.title}%"))
    if filters.category:
        statement = statement.where(Vacancy.category.ilike(f"%{filters.category}%"))
    if filters.location:
        statement = statement.where(Vacancy.location.ilike(f"%{filters.location}%"))
    if filters.employment_type:
        statement = statement.where(Vacancy.employment_type == filters.employment_type)
    return statement


def list_vacancies(db: Session, filters: VacancyFilters) -> VacancyListResponse:
    base_statement = _apply_filters(
        select(Vacancy).where(Vacancy.is_active.is_(True)),
        filters,
    )
    total = db.scalar(select(func.count()).select_from(base_statement.subquery())) or 0
    pages = math.ceil(total / filters.page_size) if total else 1

    statement = (
        base_statement.options(*VACANCY_LOAD_OPTIONS)
        .order_by(Vacancy.created_at.desc(), Vacancy.id.desc())
        .offset((filters.page - 1) * filters.page_size)
        .limit(filters.page_size)
    )
    items = db.scalars(statement).unique().all()
    return VacancyListResponse(
        items=[serialize_vacancy(vacancy) for vacancy in items],
        meta=PaginationMeta(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            pages=pages,
        ),
    )


def get_vacancy_or_404(db: Session, vacancy_id: int) -> Vacancy:
    statement = select(Vacancy).options(*VACANCY_LOAD_OPTIONS).where(Vacancy.id == vacancy_id)
    vacancy = db.scalar(statement)
    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found.")
    return vacancy


def create_vacancy(db: Session, employer: User, payload: VacancyCreate) -> Vacancy:
    vacancy = Vacancy(employer_id=employer.id, **payload.model_dump())
    db.add(vacancy)
    db.commit()
    return get_vacancy_or_404(db, vacancy.id)


def update_vacancy(db: Session, employer: User, vacancy_id: int, payload: VacancyUpdate) -> Vacancy:
    vacancy = get_vacancy_or_404(db, vacancy_id)
    if vacancy.employer_id != employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can edit only your own vacancies.",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(vacancy, field, value)

    db.add(vacancy)
    db.commit()
    return get_vacancy_or_404(db, vacancy.id)


def delete_vacancy(db: Session, employer: User, vacancy_id: int) -> None:
    vacancy = get_vacancy_or_404(db, vacancy_id)
    if vacancy.employer_id != employer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own vacancies.",
        )
    db.delete(vacancy)
    db.commit()


def list_employer_vacancies(db: Session, employer: User) -> list[Vacancy]:
    statement = (
        select(Vacancy)
        .options(*VACANCY_LOAD_OPTIONS)
        .where(Vacancy.employer_id == employer.id)
        .order_by(Vacancy.created_at.desc(), Vacancy.id.desc())
    )
    return db.scalars(statement).unique().all()
