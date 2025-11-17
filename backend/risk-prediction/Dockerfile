FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Preload BioGPT model from HuggingFace during build
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV HF_HOME=/app/.cache/huggingface
ENV HUGGINGFACE_MODEL_REPO=ishro/biogpt-aura
ENV USE_HUGGINGFACE_MODEL=true

# Download model during build time with progress indication
RUN python download_model.py

ENV PYTHONUNBUFFERED=1

EXPOSE 8004

# Use startup script instead of run.py directly
CMD ["python", "startup.py"]
