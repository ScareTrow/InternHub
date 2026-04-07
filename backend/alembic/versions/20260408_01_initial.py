"""initial schema

Revision ID: 20260408_01
Revises:
Create Date: 2026-04-08 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260408_01"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("student", "employer", name="user_role")
vacancy_type = sa.Enum("internship", "job", name="vacancy_type")
application_status = sa.Enum(
    "submitted",
    "reviewed",
    "interviewing",
    "rejected",
    "accepted",
    name="application_status",
)


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    vacancy_type.create(bind, checkfirst=True)
    application_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "student_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("university", sa.String(length=255), nullable=False),
        sa.Column("major", sa.String(length=255), nullable=True),
        sa.Column("graduation_year", sa.Integer(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "employer_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("company_website", sa.String(length=255), nullable=True),
        sa.Column("company_description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "vacancies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employer_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("employment_type", vacancy_type, nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requirements", sa.Text(), nullable=True),
        sa.Column("salary_min", sa.Integer(), nullable=True),
        sa.Column("salary_max", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["employer_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vacancies_category"), "vacancies", ["category"], unique=False)
    op.create_index(op.f("ix_vacancies_employer_id"), "vacancies", ["employer_id"], unique=False)
    op.create_index(op.f("ix_vacancies_employment_type"), "vacancies", ["employment_type"], unique=False)
    op.create_index(op.f("ix_vacancies_id"), "vacancies", ["id"], unique=False)
    op.create_index(op.f("ix_vacancies_location"), "vacancies", ["location"], unique=False)
    op.create_index(op.f("ix_vacancies_title"), "vacancies", ["title"], unique=False)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("status", application_status, nullable=False, server_default="submitted"),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vacancy_id"], ["vacancies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "vacancy_id", name="uq_student_vacancy"),
    )
    op.create_index(op.f("ix_applications_id"), "applications", ["id"], unique=False)
    op.create_index(op.f("ix_applications_student_id"), "applications", ["student_id"], unique=False)
    op.create_index(op.f("ix_applications_vacancy_id"), "applications", ["vacancy_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_applications_vacancy_id"), table_name="applications")
    op.drop_index(op.f("ix_applications_student_id"), table_name="applications")
    op.drop_index(op.f("ix_applications_id"), table_name="applications")
    op.drop_table("applications")

    op.drop_index(op.f("ix_vacancies_title"), table_name="vacancies")
    op.drop_index(op.f("ix_vacancies_location"), table_name="vacancies")
    op.drop_index(op.f("ix_vacancies_id"), table_name="vacancies")
    op.drop_index(op.f("ix_vacancies_employment_type"), table_name="vacancies")
    op.drop_index(op.f("ix_vacancies_employer_id"), table_name="vacancies")
    op.drop_index(op.f("ix_vacancies_category"), table_name="vacancies")
    op.drop_table("vacancies")

    op.drop_table("employer_profiles")
    op.drop_table("student_profiles")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    application_status.drop(bind, checkfirst=True)
    vacancy_type.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
