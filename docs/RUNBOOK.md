# SLM Serving Gateway: Production RUNBOOK


| # | Mistake (The Pitfall) | Production Mitigation / Solution |
| :--- | :--- | :--- |
| **1** | **Download model inside Dockerfile** |  |
| **2** | **Expose vLLM port directly** | **Avoided:** The vLLM port (8000) is hidden behind an Nginx Reverse Proxy. Direct exposure allows malicious actors to bypass rate-limiting, spike memory, and crash the GPU. |
| **3** | **No `--max-model-len`** | **Avoided:** We explicitly set `--max-model-len 2048` during vLLM boot. Without this, vLLM attempts to allocate memory for the model's maximum theoretical context window, instantly causing an Out-Of-Memory (OOM) crash on a 15GB T4 GPU. |
| **4** | **No quantization on weak GPU** | **Avoided:** We strictly utilize `AWQ` quantization (`Qwen2.5-1.5B-Instruct-AWQ`). Attempting to load native FP16/FP32 weights on a single T4 will either fail or leave zero memory for the KV cache (crashing on the first request). |
| **5** | **Health check doesn't verify model loaded** | **Avoided:** Our FastAPI `/health` endpoint actively pings the remote vLLM server (`response = await client.get("/health")`). If the model crashes, Docker properly marks the local gateway as `Unhealthy`. |
| **6** | **Sync endpoint blocks threads** | **Avoided:** We use `httpx.AsyncClient` alongside FastAPI's `async def` routes. Using standard `requests.post` would block the ASGI worker, entirely preventing us from hitting our 100 CCU concurrency requirement. |
| **7** | `--gpu-memory-utilization` **defaults to 0.9** | **Avoided:** We tune the memory utilization factor. T4 GPUs often have background Colab processes. Trusting the default 90% allocation often results in immediate startup crashes (`Free memory ... is less than desired GPU memory`). |
| **8** | **No timeout + no `max_tokens` cap** | **Avoided:** We enforce strict timeouts (`proxy_read_timeout 120s` in Nginx, `timeout=60` in tests) and apply `max_tokens` limits. Without these bounds, a single complex generation can hang the server permanently. |

---

## 🚀 Quick Start Guide

### 1. Remote inference (Google Colab)
1. Start the Colab Notebook.
2. Launch the vLLM Server on the T4 GPU.
3. Start the Ngrok Tunnel to expose port 8000.
4. Copy the generated `https://...ngrok-free.app` URL.

### 2. Local Gateway Setup
1. Open the `.env` file and replace `VLLM_URL` with the new Ngrok address:
   ```env
   VLLM_URL=https://your-ngrok-url.ngrok-free.app
   ```
2. Build and launch the containerized gateway (FastAPI + Nginx):
   ```bash
   docker compose -f docker/docker-compose.yml up -d --build
   ```

### 3. Monitoring & Observability
- **Check System Health:**
  ```bash
  curl http://localhost/health
  # Should return 200 OK: {"status": "ok"}
  ```
- **View JSON Access Logs (MLOps Ready):**
  ```bash
  docker compose -f docker/docker-compose.yml logs -f nginx
  ```
- **Interact with the API:**
  Visit `http://localhost/docs` in your browser to use the interactive Swagger UI.
