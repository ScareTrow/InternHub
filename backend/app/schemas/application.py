from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ApplicationStatus, VacancyType


class ApplicationCreate(BaseModel):
    cover_letter: str | None = Field(default=None, max_length=2000)


class ApplicationVacancySummary(BaseModel):
    id: int
    title: str
    category: str
    location: str
    employment_type: VacancyType
    employer_name: str


class ApplicationStudentSummary(BaseModel):
    id: int
    email: str
    full_name: str
    university: str
    major: str | None = None
    graduation_year: int | None = None


class StudentApplicationRead(BaseModel):
    id: int
    status: ApplicationStatus
    cover_letter: str | None = None
    created_at: datetime
    vacancy: ApplicationVacancySummary


class EmployerApplicationRead(BaseModel):
    id: int
    status: ApplicationStatus
    cover_letter: str | None = None
    created_at: datetime
    vacancy: ApplicationVacancySummary
    student: ApplicationStudentSummary
