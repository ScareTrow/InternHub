from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "student"
    EMPLOYER = "employer"


class VacancyType(StrEnum):
    INTERNSHIP = "internship"
    JOB = "job"


class ApplicationStatus(StrEnum):
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"
    INTERVIEWING = "interviewing"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
