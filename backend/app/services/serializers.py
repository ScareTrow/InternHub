from app.models.application import Application
from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.application import (
    ApplicationStudentSummary,
    ApplicationVacancySummary,
    EmployerApplicationRead,
    StudentApplicationRead,
)
from app.schemas.profile import EmployerProfileRead, StudentProfileRead
from app.schemas.user import CurrentUserRead
from app.schemas.vacancy import EmployerSummary, VacancyRead


def serialize_user(user: User) -> CurrentUserRead:
    student_profile = (
        StudentProfileRead.model_validate(user.student_profile)
        if user.student_profile
        else None
    )
    employer_profile = (
        EmployerProfileRead.model_validate(user.employer_profile)
        if user.employer_profile
        else None
    )
    return CurrentUserRead(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        student_profile=student_profile,
        employer_profile=employer_profile,
    )


def serialize_vacancy(vacancy: Vacancy) -> VacancyRead:
    company_name = (
        vacancy.employer.employer_profile.company_name
        if vacancy.employer and vacancy.employer.employer_profile
        else "Unknown employer"
    )
    company_location = (
        vacancy.employer.employer_profile.location
        if vacancy.employer and vacancy.employer.employer_profile
        else None
    )
    return VacancyRead(
        id=vacancy.id,
        employer_id=vacancy.employer_id,
        title=vacancy.title,
        category=vacancy.category,
        location=vacancy.location,
        employment_type=vacancy.employment_type,
        description=vacancy.description,
        requirements=vacancy.requirements,
        salary_min=vacancy.salary_min,
        salary_max=vacancy.salary_max,
        is_active=vacancy.is_active,
        created_at=vacancy.created_at,
        updated_at=vacancy.updated_at,
        employer=EmployerSummary(
            user_id=vacancy.employer_id,
            company_name=company_name,
            location=company_location,
        ),
        applications_count=len(vacancy.applications),
    )


def serialize_student_application(application: Application) -> StudentApplicationRead:
    vacancy = application.vacancy
    employer_name = (
        vacancy.employer.employer_profile.company_name
        if vacancy.employer and vacancy.employer.employer_profile
        else "Unknown employer"
    )
    return StudentApplicationRead(
        id=application.id,
        status=application.status,
        cover_letter=application.cover_letter,
        created_at=application.created_at,
        vacancy=ApplicationVacancySummary(
            id=vacancy.id,
            title=vacancy.title,
            category=vacancy.category,
            location=vacancy.location,
            employment_type=vacancy.employment_type,
            employer_name=employer_name,
        ),
    )


def serialize_employer_application(application: Application) -> EmployerApplicationRead:
    vacancy = application.vacancy
    student_profile = application.student.student_profile
    employer_name = (
        vacancy.employer.employer_profile.company_name
        if vacancy.employer and vacancy.employer.employer_profile
        else "Unknown employer"
    )
    return EmployerApplicationRead(
        id=application.id,
        status=application.status,
        cover_letter=application.cover_letter,
        created_at=application.created_at,
        vacancy=ApplicationVacancySummary(
            id=vacancy.id,
            title=vacancy.title,
            category=vacancy.category,
            location=vacancy.location,
            employment_type=vacancy.employment_type,
            employer_name=employer_name,
        ),
        student=ApplicationStudentSummary(
            id=application.student.id,
            email=application.student.email,
            full_name=student_profile.full_name if student_profile else application.student.email,
            university=student_profile.university if student_profile else "N/A",
            major=student_profile.major if student_profile else None,
            graduation_year=student_profile.graduation_year if student_profile else None,
        ),
    )
