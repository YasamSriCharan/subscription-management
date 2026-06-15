# PlanPilot Subscription Management

PlanPilot is a React + FastAPI + Spring Boot subscription management app.

## Local Stack

- Frontend: React 19, Vite 8, plain CSS, fetch API
- API gateway: Python FastAPI, Uvicorn, HTTPX
- Core service: Java Spring Boot, Maven, Spring Web MVC, Spring Data JPA, PostgreSQL, JWT
- Database: PostgreSQL for users, plans, subscriptions, and subscription logs

## Ports

- React frontend: `http://localhost:5173`
- FastAPI gateway: `http://localhost:8000`
- Spring Boot core service: `http://localhost:8001`

The frontend calls only the FastAPI gateway. The gateway proxies `/auth/**` and `/api/**` requests to Spring Boot.

## Run Locally

1. Create the PostgreSQL database:

```sql
CREATE DATABASE sub_mth;
```

2. Update credentials in `spring-backend/src/main/resources/application.properties` if needed.

3. Start Spring Boot:

```powershell
cd spring-backend
mvn spring-boot:run
```

4. Start the FastAPI gateway:

```powershell
cd backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

5. Start the React frontend:

```powershell
cd frontend\frontend
npm install
npm run dev
```

## Authentication

JWTs are stored in browser `localStorage` and sent from the frontend using the `Token` header. Spring also accepts `Authorization: Bearer <token>` for compatibility.

## Main Endpoints

- `POST /auth/signup`
- `POST /auth/login`
- `GET /api/dashboard`
- `POST /api/search`
- `POST /api/plans`
- `POST /api/subscriptions`
- `PATCH /api/subscriptions/{subscriptionId}/status`
- `PATCH /api/subscriptions/{subscriptionId}/plan`
