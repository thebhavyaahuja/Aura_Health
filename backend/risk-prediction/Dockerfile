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

# Download model during build time
RUN python -c "from transformers import AutoTokenizer, BioGptForSequenceClassification; \
    print('Downloading BioGPT model...'); \
    tokenizer = AutoTokenizer.from_pretrained('${HUGGINGFACE_MODEL_REPO:-ishro/biogpt-aura}'); \
    model = BioGptForSequenceClassification.from_pretrained('${HUGGINGFACE_MODEL_REPO:-ishro/biogpt-aura}'); \
    print('Model downloaded and cached successfully!')"

ENV PYTHONUNBUFFERED=1

EXPOSE 8004

# Use startup script instead of run.py directly
CMD ["python", "startup.py"]
