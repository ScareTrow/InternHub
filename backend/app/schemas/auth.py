from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.enums import UserRole
from app.schemas.profile import EmployerProfileCreate, StudentProfileCreate


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    student_profile: StudentProfileCreate | None = None
    employer_profile: EmployerProfileCreate | None = None

    @model_validator(mode="after")
    def validate_profile_payload(self) -> "RegisterRequest":
        if self.role == UserRole.STUDENT and not self.student_profile:
            raise ValueError("Student registration requires student_profile.")
        if self.role == UserRole.EMPLOYER and not self.employer_profile:
            raise ValueError("Employer registration requires employer_profile.")
        if self.role == UserRole.STUDENT:
            self.employer_profile = None
        if self.role == UserRole.EMPLOYER:
            self.student_profile = None
        return self


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
