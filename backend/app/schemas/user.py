from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import UserRole
from app.schemas.profile import EmployerProfileRead, StudentProfileRead


class CurrentUserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    student_profile: StudentProfileRead | None = None
    employer_profile: EmployerProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)
