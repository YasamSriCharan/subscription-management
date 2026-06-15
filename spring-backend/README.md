# Spring Backend

This is the Spring Boot + PostgreSQL core service for PlanPilot subscription management.

The service runs on `http://localhost:8001`. The React frontend should not call it directly during local development; requests go through the FastAPI gateway on `http://localhost:8000`.

## Import into Spring Tools

1. Open `Spring Tool Suite`.
2. Choose `File -> Import -> Existing Maven Projects`.
3. Select the folder:

```text
C:\Users\CHARAN\Downloads\DSEDBD_PROJECT\spring-backend
```

4. Let STS download Maven dependencies.
5. Open `src/main/resources/application.properties`.
6. Update the PostgreSQL username/password if needed.
7. Run `SubscriptionManagementApplication.java` as a Spring Boot app.

## PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE sub_mth;
```

Default app config:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/sub_mth
spring.datasource.username=postgres
spring.datasource.password=postgres
```

## Run From Terminal

```powershell
cd C:\Users\CHARAN\Downloads\DSEDBD_PROJECT\spring-backend
mvn spring-boot:run
```

## API Endpoints

- `POST /auth/signup`
- `POST /auth/login`
- `GET /api/dashboard`
- `POST /api/search`
- `POST /api/plans`
- `POST /api/subscriptions`
- `PATCH /api/subscriptions/{subscriptionId}/status`
- `PATCH /api/subscriptions/{subscriptionId}/plan`

Authenticated requests accept either `Token: <jwt>` or `Authorization: Bearer <jwt>`.

## Optional H2 Fallback

If you want to run without PostgreSQL temporarily in STS, set the active profile to:

```text
h2
```

That uses `application-h2.properties` and keeps the backend on port `8001`.
