FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim 

# Install curl for the Docker healthcheck, then clean up in the same layer.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -m -r aiuser

COPY --from=builder --chown=aiuser:aiuser /opt/venv /opt/venv

WORKDIR /app
COPY --chown=aiuser:aiuser ./app ./app

USER aiuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
