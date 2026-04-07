# InternHub

InternHub is a full-stack MVP for a student internship/job platform built for a team project. It includes JWT authentication, role-based flows for students and employers, vacancy management, applications, PostgreSQL persistence, Alembic migrations, demo seed data, and a React frontend.

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic, JWT
- Database: PostgreSQL
- Frontend: React, Vite, React Router, Axios
- Infrastructure: Docker Compose

## Features

- Registration and login with `student` and `employer` roles
- JWT auth and protected frontend routes
- Student and employer profile creation during registration
- Vacancy CRUD for employers
- Vacancy listing with filters and pagination
- Vacancy detail page with student applications
- Student dashboard and "My applications"
- Employer dashboard with own vacancies and incoming applications
- Swagger/OpenAPI docs at `/docs`
- Idempotent demo seed data

## Project Structure

```text
InternHub/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 20260408_01_initial.py
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── Dockerfile
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── styles/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── docker-compose.yml
└── README.md
```

## Quick Start With Docker

1. Copy the environment file:

```bash
cp .env.example .env
```

2. Start the project:

```bash
docker compose up --build
```

3. Open the app:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

The backend container runs:

- `alembic upgrade head`
- `python -m app.db.seed`
- `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Default Vite dev URL: `http://localhost:5173`

## API Overview

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Vacancies

- `GET /api/v1/vacancies`
- `GET /api/v1/vacancies/{id}`
- `POST /api/v1/vacancies`
- `PUT /api/v1/vacancies/{id}`
- `DELETE /api/v1/vacancies/{id}`
- `GET /api/v1/vacancies/me/list`
- `POST /api/v1/vacancies/{id}/apply`

### Applications

- `GET /api/v1/applications/me`
- `GET /api/v1/applications/employer`

## Demo Seed Accounts

Password for all seeded users: `password123`

Employers:

- `talent@skyforge.io`
- `hr@northstartech.dev`

Students:

- `aigerim@student.edu`
- `dias@student.edu`
- `madina@student.edu`
- `arsen@student.edu`

## Notes

- Migrations live in [`backend/alembic/versions/20260408_01_initial.py`](backend/alembic/versions/20260408_01_initial.py)
- Seed script lives in [`backend/app/db/seed.py`](backend/app/db/seed.py)
- Frontend API base URL defaults to `/api/v1` and is proxied by Nginx inside Docker
