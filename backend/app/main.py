from __future__ import annotations

import os
from collections.abc import Mapping

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware


CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL", "http://127.0.0.1:8001").rstrip("/")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("GATEWAY_TIMEOUT_SECONDS", "20"))

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}

app = FastAPI(
    title="PlanPilot API Gateway",
    description="Gateway for the React client. It forwards auth and subscription requests to the Spring core service.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def filter_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }


async def proxy_request(request: Request, downstream_path: str) -> Response:
    target_url = f"{CORE_SERVICE_URL}{downstream_path}"
    body = await request.body()

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        try:
            upstream_response = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=body,
                headers=filter_headers(request.headers),
            )
        except httpx.RequestError as exc:
            return Response(
                content=f'{{"detail":"Core service is unavailable: {exc.request.url}"}}',
                status_code=503,
                media_type="application/json",
            )

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=filter_headers(upstream_response.headers),
        media_type=upstream_response.headers.get("content-type"),
    )


@app.get("/")
def root() -> dict[str, object]:
    return {
        "message": "PlanPilot gateway is running.",
        "coreService": CORE_SERVICE_URL,
        "proxiedPrefixes": ["/auth", "/api"],
    }


@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy_auth(path: str, request: Request) -> Response:
    return await proxy_request(request, f"/auth/{path}")


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy_api(path: str, request: Request) -> Response:
    return await proxy_request(request, f"/api/{path}")
