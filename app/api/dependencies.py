import structlog
from typing import AsyncGenerator
import httpx

vllm_client: httpx.AsyncClient | None = None

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger("api_gateway")

async def get_vllm_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    if vllm_client is None:
        raise RuntimeError("vLLM Client is not initialized. Check lifespan in main.py")
    
    logger.info("Starting vLLM request...")

    yield vllm_client

    logger.info("Finished vLLM request.")

def get_logger() -> structlog.stdlib.BoundLogger:
    return logger
