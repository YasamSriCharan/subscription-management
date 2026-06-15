# FastAPI Gateway

The FastAPI app is the API gateway for the React frontend.

It runs on `http://localhost:8000` and proxies requests to the Spring Boot core service at `http://localhost:8001`.

## Run

```powershell
cd C:\Users\CHARAN\Downloads\DSEDBD_PROJECT\backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

## Configuration

Optional environment variables:

- `CORE_SERVICE_URL`: downstream Spring service URL. Default: `http://127.0.0.1:8001`
- `GATEWAY_TIMEOUT_SECONDS`: downstream request timeout. Default: `20`

## Proxied Routes

- `/auth/**` -> Spring `/auth/**`
- `/api/**` -> Spring `/api/**`

The gateway preserves request bodies, query parameters, and headers, including the custom `Token` JWT header used by the frontend.
