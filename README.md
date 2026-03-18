# SLM Serving Gateway

## Description
This project provides a highly concurrent, production-ready gateway for serving Small Language Models (SLMs). It acts as an intelligent proxy that bridges local requests to a remote heavy-compute node offering inference capabilities, ensuring that traffic is securely routed, strictly rate-limited, and properly monitored.

## Architecture
The system utilizes a hybrid deployment model:
1. **Remote Inference Node (Heavy Compute):** A Google Colab T4 instance running a quantized model (`Qwen2.5-1.5B-Instruct-AWQ`) using the `vLLM` engine. This engine exposes an OpenAI-compatible API over a secure Ngrok tunnel.
2. **Local Gateway Node (Routing & Orchestration):** A local Docker Compose stack functioning as the traffic controller. It processes incoming requests, enforces concurrency protections, and forwards validated traffic over the tunnel asynchronously.

## Tech Stack
* **Proxy and Load Balancing:** Nginx
* **API Framework:** FastAPI, Uvicorn
* **HTTP Client:** HTTPX (Async)
* **Inference Engine:** vLLM (with AutoAWQ)
* **Validation:** Pydantic
* **Observability:** Structlog (JSON structured logging)
* **Containerization:** Docker, Docker Compose

## Quick Start
1. **Prepare the Remote Node:**
   - Launch your Google Colab instance equipped with a T4 GPU.
   - Start the vLLM server and establish an Ngrok tunnel.
   - Copy your generated Ngrok Forwarding URL.

2. **Configure Local Environment:**
   - Clone this repository.
   - Create a `.env` file in the root directory and add your tunnel URL:
     ```env
     VLLM_URL=https://your-ngrok-url.ngrok-free.app
     ```

3. **Deploy the Gateway:**
   - From the repository root, start the Docker containers:
     ```bash
     docker compose -f docker/docker-compose.yml up -d --build
     ```

4. **Verify Deployment:**
   - Check system health: `curl http://localhost/health`
   - Test inference via the proxy:
     ```bash
     curl -X POST http://localhost/v1/chat/completions \
       -H "Content-Type: application/json" \
       -d '{"messages":[{"role": "user", "content": "Hello!"}]}'
     ```

## Project Structure
```text
slm-serving-challenge1/
├── app/                        # FastAPI Wrapper (Core app)
│   ├── main.py                 # FastAPI entry point & lifespan events
│   ├── api/                    # HTTP Layer (Routes & Middleware)
│   │   ├── dependencies.py     # Async HTTP client and logger factories
│   │   └── v1/                 # API Version v1
│   │       ├── router.py       # Main router inclusion
│   │       └── endpoints/      # Controllers (chat.py, health.py)
│   ├── schemas/                # Pydantic API Contracts
│   └── core/                   # Application configuration (config.py)
├── colab/                      # Remote node scripts
│   └── SLM_serving.ipynb       # Colab notebook for vLLM & Ngrok
├── docker/                     # Infrastructure as Code
│   ├── Dockerfile              # Multi-stage Python build
│   └── docker-compose.yml      # Orchestration for Nginx and FastAPI
├── docs/                       # Project Documentation
│   └── RUNBOOK.md              # Avoidance Table and Operations Manual
│   └──screenshots/             # Screenshots of proof
├── nginx/                      # Reverse Proxy configuration
│   └── nginx.conf              # Rate limiting, timeouts, & proxy pass
├── pyproject.toml              # Project dependencies configuration (uv)
├── requirements.txt            # Python dependencies lists
├── test.py                     # Local single request test script
└── rate_limit_test.py          # Local concurrency stress test script
```
