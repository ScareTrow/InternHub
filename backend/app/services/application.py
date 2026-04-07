from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.application import Application
from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.application import ApplicationCreate
from app.services.vacancy import get_vacancy_or_404


APPLICATION_STUDENT_LOAD = (
    joinedload(Application.vacancy)
    .joinedload(Vacancy.employer)
    .joinedload(User.employer_profile),
)
APPLICATION_EMPLOYER_LOAD = (
    joinedload(Application.student).joinedload(User.student_profile),
    joinedload(Application.vacancy)
    .joinedload(Vacancy.employer)
    .joinedload(User.employer_profile),
)


def get_application_or_404(db: Session, application_id: int) -> Application:
    statement = (
        select(Application)
        .options(*APPLICATION_EMPLOYER_LOAD)
        .where(Application.id == application_id)
    )
    application = db.scalar(statement)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )
    return application


def apply_to_vacancy(
    db: Session,
    student: User,
    vacancy_id: int,
    payload: ApplicationCreate,
) -> Application:
    vacancy = get_vacancy_or_404(db, vacancy_id)
    if not vacancy.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vacancy is no longer accepting applications.",
        )

    existing = db.scalar(
        select(Application).where(
            Application.student_id == student.id,
            Application.vacancy_id == vacancy_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this vacancy.",
        )

    application = Application(
        student_id=student.id,
        vacancy_id=vacancy_id,
        cover_letter=payload.cover_letter,
    )
    db.add(application)
    db.commit()
    return get_application_or_404(db, application.id)


def list_student_applications(db: Session, student: User) -> list[Application]:
    statement = (
        select(Application)
        .options(*APPLICATION_STUDENT_LOAD)
        .where(Application.student_id == student.id)
        .order_by(Application.created_at.desc(), Application.id.desc())
    )
    return db.scalars(statement).unique().all()


def list_employer_applications(
    db: Session,
    employer: User,
    vacancy_id: int | None = None,
) -> list[Application]:
    statement = (
        select(Application)
        .join(Application.vacancy)
        .options(*APPLICATION_EMPLOYER_LOAD)
        .where(Vacancy.employer_id == employer.id)
        .order_by(Application.created_at.desc(), Application.id.desc())
    )
    if vacancy_id is not None:
        statement = statement.where(Application.vacancy_id == vacancy_id)
    return db.scalars(statement).unique().all()
