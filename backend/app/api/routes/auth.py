from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import RegisterRequest, Token
from app.schemas.user import CurrentUserRead
from app.services import auth as auth_service
from app.services.serializers import serialize_user


router = APIRouter()


@router.post("/register", response_model=CurrentUserRead, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> CurrentUserRead:
    user = auth_service.register_user(db, payload)
    return serialize_user(user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=CurrentUserRead)
def get_me(current_user: User = Depends(get_current_user)) -> CurrentUserRead:
    return serialize_user(current_user)
