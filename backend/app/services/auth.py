from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_password_hash, verify_password
from app.models.employer_profile import EmployerProfile
from app.models.user import User
from app.models.student_profile import StudentProfile
from app.schemas.auth import RegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = (
        select(User)
        .options(
            selectinload(User.student_profile),
            selectinload(User.employer_profile),
        )
        .where(User.email == email.lower())
    )
    return db.scalar(statement)


def register_user(db: Session, payload: RegisterRequest) -> User:
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    user = User(
        email=payload.email.lower(),
        password_hash=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()

    if payload.student_profile:
        db.add(StudentProfile(user_id=user.id, **payload.student_profile.model_dump()))
    if payload.employer_profile:
        employer_payload = payload.employer_profile.model_dump(mode="json")
        db.add(EmployerProfile(user_id=user.id, **employer_payload))

    db.commit()
    return get_user_by_email(db, user.email)  # type: ignore[return-value]


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
