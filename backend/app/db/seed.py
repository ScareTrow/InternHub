from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.application import Application
from app.models.employer_profile import EmployerProfile
from app.models.enums import UserRole, VacancyType
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.models.vacancy import Vacancy


EMPLOYERS = [
    {
        "email": "talent@skyforge.io",
        "password": "password123",
        "profile": {
            "company_name": "SkyForge Labs",
            "company_website": "https://skyforge.example.com",
            "company_description": "Product studio building AI and analytics tools for education.",
            "location": "Almaty",
        },
    },
    {
        "email": "hr@northstartech.dev",
        "password": "password123",
        "profile": {
            "company_name": "NorthStar Tech",
            "company_website": "https://northstar.example.com",
            "company_description": "Distributed engineering team focused on fintech and student-friendly hiring.",
            "location": "Astana",
        },
    },
]

STUDENTS = [
    {
        "email": "aigerim@student.edu",
        "password": "password123",
        "profile": {
            "full_name": "Aigerim Sadykova",
            "university": "KBTU",
            "major": "Computer Science",
            "graduation_year": 2027,
            "location": "Almaty",
            "skills": "Python, FastAPI, PostgreSQL",
            "bio": "Backend-focused student interested in product engineering internships.",
        },
    },
    {
        "email": "dias@student.edu",
        "password": "password123",
        "profile": {
            "full_name": "Dias Beketov",
            "university": "Nazarbayev University",
            "major": "Software Engineering",
            "graduation_year": 2026,
            "location": "Astana",
            "skills": "React, TypeScript, UI systems",
            "bio": "Frontend student who enjoys shipping polished interfaces.",
        },
    },
    {
        "email": "madina@student.edu",
        "password": "password123",
        "profile": {
            "full_name": "Madina Tulegenova",
            "university": "SDU University",
            "major": "Information Systems",
            "graduation_year": 2028,
            "location": "Shymkent",
            "skills": "Data analysis, SQL, BI",
            "bio": "Looking for analytics and product internships.",
        },
    },
    {
        "email": "arsen@student.edu",
        "password": "password123",
        "profile": {
            "full_name": "Arsen Nurpeisov",
            "university": "Astana IT University",
            "major": "Cybersecurity",
            "graduation_year": 2027,
            "location": "Astana",
            "skills": "Security, networks, Linux",
            "bio": "Interested in cloud security and platform engineering roles.",
        },
    },
]

VACANCIES = [
    {
        "employer_email": "talent@skyforge.io",
        "title": "Backend Engineering Intern",
        "category": "Engineering",
        "location": "Almaty",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Work with the platform team on APIs, data models, and internal tooling.",
        "requirements": "Python basics, SQL fundamentals, interest in backend systems.",
        "salary_min": 120000,
        "salary_max": 180000,
    },
    {
        "employer_email": "talent@skyforge.io",
        "title": "Frontend React Intern",
        "category": "Frontend",
        "location": "Remote",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Help deliver UI features for dashboards and candidate workflows.",
        "requirements": "JavaScript, React fundamentals, good eye for details.",
        "salary_min": 120000,
        "salary_max": 170000,
    },
    {
        "employer_email": "talent@skyforge.io",
        "title": "Product Analytics Intern",
        "category": "Analytics",
        "location": "Almaty",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Support KPI reporting, dashboards, and experimentation analysis.",
        "requirements": "Excel or Sheets, SQL basics, curiosity for product metrics.",
        "salary_min": 110000,
        "salary_max": 160000,
    },
    {
        "employer_email": "talent@skyforge.io",
        "title": "Junior Python Developer",
        "category": "Engineering",
        "location": "Astana",
        "employment_type": VacancyType.JOB,
        "description": "Join the delivery team to maintain API integrations and services.",
        "requirements": "Python, REST APIs, Git, teamwork.",
        "salary_min": 300000,
        "salary_max": 450000,
    },
    {
        "employer_email": "talent@skyforge.io",
        "title": "QA Automation Trainee",
        "category": "QA",
        "location": "Remote",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Build simple automated checks and support release quality processes.",
        "requirements": "Attention to detail, scripting basics, test mindset.",
        "salary_min": 100000,
        "salary_max": 140000,
    },
    {
        "employer_email": "hr@northstartech.dev",
        "title": "DevOps Intern",
        "category": "DevOps",
        "location": "Astana",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Assist with CI/CD, cloud environments, and infrastructure scripts.",
        "requirements": "Linux basics, Git, interest in infrastructure.",
        "salary_min": 130000,
        "salary_max": 190000,
    },
    {
        "employer_email": "hr@northstartech.dev",
        "title": "Junior Data Analyst",
        "category": "Analytics",
        "location": "Remote",
        "employment_type": VacancyType.JOB,
        "description": "Prepare recurring reports and partner with product and operations teams.",
        "requirements": "SQL, spreadsheets, communication skills.",
        "salary_min": 280000,
        "salary_max": 420000,
    },
    {
        "employer_email": "hr@northstartech.dev",
        "title": "Security Operations Intern",
        "category": "Security",
        "location": "Astana",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Work with the security team on monitoring and incident checklists.",
        "requirements": "Networking basics, OS fundamentals, responsible mindset.",
        "salary_min": 125000,
        "salary_max": 175000,
    },
    {
        "employer_email": "hr@northstartech.dev",
        "title": "Junior Full-Stack Developer",
        "category": "Engineering",
        "location": "Almaty",
        "employment_type": VacancyType.JOB,
        "description": "Ship product features across React frontends and Python services.",
        "requirements": "JavaScript or Python, REST, teamwork, curiosity.",
        "salary_min": 350000,
        "salary_max": 520000,
    },
    {
        "employer_email": "hr@northstartech.dev",
        "title": "UX Research Assistant",
        "category": "Design",
        "location": "Remote",
        "employment_type": VacancyType.INTERNSHIP,
        "description": "Support interviews, note synthesis, and prototype feedback loops.",
        "requirements": "Strong communication, empathy, organization.",
        "salary_min": 90000,
        "salary_max": 130000,
    },
]

APPLICATIONS = [
    {
        "student_email": "aigerim@student.edu",
        "vacancy_title": "Backend Engineering Intern",
        "cover_letter": "I want to grow in backend engineering and already build APIs in Python.",
    },
    {
        "student_email": "dias@student.edu",
        "vacancy_title": "Frontend React Intern",
        "cover_letter": "I focus on React UI and would like to contribute to hiring workflows.",
    },
    {
        "student_email": "madina@student.edu",
        "vacancy_title": "Product Analytics Intern",
        "cover_letter": "I enjoy working with metrics and turning data into product insights.",
    },
    {
        "student_email": "arsen@student.edu",
        "vacancy_title": "Security Operations Intern",
        "cover_letter": "Security operations is the area where I want hands-on experience.",
    },
    {
        "student_email": "aigerim@student.edu",
        "vacancy_title": "Junior Full-Stack Developer",
        "cover_letter": "I have backend strength and want to expand into end-to-end delivery.",
    },
]


def ensure_user(db: Session, email: str, password: str, role: UserRole, profile_data: dict) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        return user

    user = User(email=email, password_hash=get_password_hash(password), role=role)
    db.add(user)
    db.flush()

    if role == UserRole.EMPLOYER:
        db.add(EmployerProfile(user_id=user.id, **profile_data))
    else:
        db.add(StudentProfile(user_id=user.id, **profile_data))

    db.commit()
    return user


def ensure_vacancy(db: Session, employer: User, vacancy_data: dict) -> Vacancy:
    vacancy = db.scalar(
        select(Vacancy).where(
            Vacancy.employer_id == employer.id,
            Vacancy.title == vacancy_data["title"],
        )
    )
    if vacancy:
        return vacancy

    vacancy = Vacancy(employer_id=employer.id, **vacancy_data)
    db.add(vacancy)
    db.commit()
    return vacancy


def ensure_application(db: Session, student: User, vacancy: Vacancy, cover_letter: str) -> None:
    existing = db.scalar(
        select(Application).where(
            Application.student_id == student.id,
            Application.vacancy_id == vacancy.id,
        )
    )
    if existing:
        return

    db.add(
        Application(
            student_id=student.id,
            vacancy_id=vacancy.id,
            cover_letter=cover_letter,
        )
    )
    db.commit()


def seed() -> None:
    with SessionLocal() as db:
        for employer_data in EMPLOYERS:
            ensure_user(
                db,
                email=employer_data["email"],
                password=employer_data["password"],
                role=UserRole.EMPLOYER,
                profile_data=employer_data["profile"],
            )

        for student_data in STUDENTS:
            ensure_user(
                db,
                email=student_data["email"],
                password=student_data["password"],
                role=UserRole.STUDENT,
                profile_data=student_data["profile"],
            )

        for vacancy_data in VACANCIES:
            employer = db.scalar(select(User).where(User.email == vacancy_data["employer_email"]))
            if employer is None:
                continue
            ensure_vacancy(
                db,
                employer,
                {
                    key: value
                    for key, value in vacancy_data.items()
                    if key != "employer_email"
                },
            )

        for application_data in APPLICATIONS:
            student = db.scalar(select(User).where(User.email == application_data["student_email"]))
            vacancy = db.scalar(select(Vacancy).where(Vacancy.title == application_data["vacancy_title"]))
            if student and vacancy:
                ensure_application(db, student, vacancy, application_data["cover_letter"])

    print("Seed data applied.")


if __name__ == "__main__":
    seed()
