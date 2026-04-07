from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class StudentProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    university: str = Field(min_length=2, max_length=255)
    major: str | None = Field(default=None, max_length=255)
    graduation_year: int | None = None
    location: str | None = Field(default=None, max_length=255)
    skills: str | None = Field(default=None, max_length=1000)
    bio: str | None = Field(default=None, max_length=2000)

    @field_validator("graduation_year")
    @classmethod
    def validate_graduation_year(cls, value: int | None) -> int | None:
        if value is None:
            return value
        if value < 2000 or value > 2100:
            raise ValueError("Graduation year must be between 2000 and 2100.")
        return value


class StudentProfileRead(StudentProfileCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class EmployerProfileCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    company_website: HttpUrl | None = None
    company_description: str | None = Field(default=None, max_length=2000)
    location: str | None = Field(default=None, max_length=255)


class EmployerProfileRead(BaseModel):
    id: int
    user_id: int
    company_name: str
    company_website: str | None = None
    company_description: str | None = None
    location: str | None = None

    model_config = ConfigDict(from_attributes=True)
