from fastapi import APIRouter, Depends, HTTPException
import os 
import logging
import httpx

from app.api.dependencies import get_logger, get_vllm_client
from app.core.config import settings


VLLM_URL = settings.VLLM_URL

logger = get_logger()

router = APIRouter()

@router.get("/health")
async def health(client: httpx.AsyncClient = Depends(get_vllm_client)):
    try:
        response = await client.get(f"{VLLM_URL}/health")

        if response.status_code == 200:
            return {"status": "ok"}

        raise HTTPException(status_code=503, detail=f"GPU reported error: {response.status_code}")


    except Exception as e:
        logger.warning(f"Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Remote Colab GPU is unreachable or ngrok tunnel down.")


