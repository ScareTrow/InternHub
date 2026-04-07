from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.models.enums import VacancyType
from app.schemas.common import PaginationMeta


class VacancyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    category: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=255)
    employment_type: VacancyType
    description: str = Field(min_length=20, max_length=4000)
    requirements: str | None = Field(default=None, max_length=4000)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    is_active: bool = True

    @model_validator(mode="after")
    def validate_salary_range(self) -> "VacancyCreate":
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min must be less than or equal to salary_max.")
        return self


class VacancyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    category: str | None = Field(default=None, min_length=2, max_length=120)
    location: str | None = Field(default=None, min_length=2, max_length=255)
    employment_type: VacancyType | None = None
    description: str | None = Field(default=None, min_length=20, max_length=4000)
    requirements: str | None = Field(default=None, max_length=4000)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_salary_range(self) -> "VacancyUpdate":
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValueError("salary_min must be less than or equal to salary_max.")
        return self


class VacancyFilters(BaseModel):
    title: str | None = None
    category: str | None = None
    location: str | None = None
    employment_type: VacancyType | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)


class EmployerSummary(BaseModel):
    user_id: int
    company_name: str
    location: str | None = None


class VacancyRead(BaseModel):
    id: int
    employer_id: int
    title: str
    category: str
    location: str
    employment_type: VacancyType
    description: str
    requirements: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    employer: EmployerSummary
    applications_count: int = 0


class VacancyListResponse(BaseModel):
    items: list[VacancyRead]
    meta: PaginationMeta
