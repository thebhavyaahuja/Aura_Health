# HuggingFace Model Setup

## 1. Train and Push Model

```bash
cd backend/model-training

# Install deps
pip install -r requirements.txt

# Login to HuggingFace
huggingface-cli login
# Get token from: https://huggingface.co/settings/tokens

# Train model
python biogpt.py
# When asked "push to HuggingFace?" → type: yes
```

Model will be pushed to: `ishro/biogpt-aura`

## 2. Use Model in Risk-Prediction Service

The service auto-downloads the model from HuggingFace.

```bash
cd backend/risk-prediction

# Test model download works
python test_model_download.py

# Start service (downloads model on first run)
python run.py
```

## Config

**File**: `backend/risk-prediction/.env`

```bash
# Use HuggingFace (default)
USE_HUGGINGFACE_MODEL=true
HUGGINGFACE_MODEL_REPO=ishro/biogpt-aura

# OR use local model
USE_HUGGINGFACE_MODEL=false
LOCAL_MODEL_PATH=/path/to/model
```

## Update Model

```bash
# 1. Retrain and push
cd backend/model-training
python biogpt.py  # answer 'yes' to push

# 2. Clear cache and restart service
rm -rf ~/.cache/huggingface/hub/models--ishro--biogpt-aura
cd ../risk-prediction
python run.py
```

Done.
