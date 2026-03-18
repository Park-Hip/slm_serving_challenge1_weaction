from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
import logging

from app.api.dependencies import get_logger, get_vllm_client
from app.schemas.chat import ChatCompletionRequest
from app.core.config import settings


VLLM_URL = settings.VLLM_URL

router = APIRouter()

@router.post("/chat/completions")
async def chat_completion(
    request: ChatCompletionRequest,
    client:  httpx.AsyncClient = Depends(get_vllm_client),
    logger: logging.Logger = Depends(get_logger)
):
    try: 
        response = await client.post(f"{VLLM_URL}/v1/chat/completions", json=request.model_dump())
        response.raise_for_status()

        return response.json()
    except Exception as e:
        logger.error(f"Failed to generate response", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to communicate with the Colab GPU.")