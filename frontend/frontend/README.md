# PlanPilot Frontend

React + Vite frontend for the PlanPilot subscription workspace.

## Run

```powershell
cd C:\Users\CHARAN\Downloads\DSEDBD_PROJECT\frontend\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API Routing

During local development, Vite proxies these paths to the FastAPI gateway on `http://127.0.0.1:8000`:

- `/auth/**`
- `/api/**`

The frontend stores the JWT in `localStorage` and sends it with authenticated requests as `Token: <jwt>`.

If you need to override the API base, set:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```
