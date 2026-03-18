from fastapi import FastAPI
import logging
import httpx
import os
from contextlib import asynccontextmanager

from app.api import dependencies
from app.api.v1.router import api_router
from app.core.config import settings
from app.api.v1.endpoints import health

VLLM_URL = settings.VLLM_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    dependencies.vllm_client = httpx.AsyncClient(
        base_url=VLLM_URL,
        timeout=120,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )

    yield 

    await dependencies.vllm_client.aclose()

app = FastAPI(lifespan=lifespan)
app.include_router(health.router, tags=["Health"])
app.include_router(api_router, prefix="/v1")