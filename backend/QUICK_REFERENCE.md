# 🚀 Quick Reference Guide - ODOMOS Backend

## 📌 Super Admin Credentials
```
Email: super@gmail.com
Password: pw
```

## 🔧 Common Commands

### Start/Stop Services
```bash
cd /Users/vishal/Documents/IIIT-H/DSI/biogpt/odomos-dsi/backend

# Start all services
./setup_and_run.sh start

# Stop all services
./setup_and_run.sh stop

# Restart all services
./setup_and_run.sh restart

# Check status
./setup_and_run.sh status

# View logs
./setup_and_run.sh logs
```

### Complete Reset (Clean Everything)
```bash
# This will:
# - Stop all services
# - Clean all databases
# - Optionally clean uploaded files
# - Recreate super admin
# - Restart all services
./reset_and_restart.sh
```

## 🧪 Testing

### Test Risk Prediction
```bash
cd risk-prediction
./venv/bin/python test_prediction_quick.py
```

### Check Prediction Database
```bash
cd risk-prediction
./venv/bin/python check_database.py
```

### Test Authentication
```bash
cd authentication
./venv/bin/python test_auth.py
```

## 🌐 Service Endpoints

| Service | Port | URL |
|---------|------|-----|
| Authentication | 8010 | http://localhost:8010 |
| Document Ingestion | 8001 | http://localhost:8001 |
| Document Parsing | 8002 | http://localhost:8002 |
| Information Structuring | 8003 | http://localhost:8003 |
| Risk Prediction | 8004 | http://localhost:8004 |

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /health` - Health check

### Document Ingestion
- `POST /documents/upload` - Upload document
- `GET /documents` - List documents
- `GET /documents/{id}` - Get document
- `DELETE /documents/{id}` - Delete document

### Risk Prediction
- `POST /predictions/predict` - Generate prediction (auth required)
- `POST /predictions/predict-internal` - Internal prediction (no auth)
- `GET /predictions/document/{document_id}` - Get prediction (auth required)
- `GET /health` - Health check

## 🤖 Model Information

**Model:** `ishro/biogpt-aura` (from HuggingFace)  
**Task:** BI-RADS Classification  
**Classes:** 7 (BI-RADS 0-6)  
**Device:** CPU (GPU if available)

### BI-RADS Risk Levels
- **0:** Needs Assessment
- **1-2:** Low Risk (Negative/Benign)
- **3:** Medium Risk (Probably Benign)
- **4-6:** High Risk (Suspicious/Malignant/Known Malignancy)

## 📁 Database Locations

```
authentication/auth.db              # User accounts, tokens
document-ingestion/database.db      # Uploaded documents
document-parsing/parsing.db         # Parsed documents
information-structuring/structuring.db  # Structured data
risk-prediction/predictions.db      # Predictions and risk scores
```

## 📋 Log Files

```
logs/authentication.log
logs/document-ingestion.log
logs/document-parsing.log
logs/information-structuring.log
logs/risk-prediction.log
```

## 🔍 Quick Health Check

```bash
# Check all services are running
curl http://localhost:8010/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

## 🐛 Troubleshooting

### Service won't start
```bash
# Check if port is in use
lsof -i :8004

# Kill process on port
kill -9 $(lsof -t -i:8004)

# Restart service
./setup_and_run.sh start
```

### Check logs for errors
```bash
tail -f logs/risk-prediction.log
```

### Reset everything
```bash
./reset_and_restart.sh
```

## 📦 Python Virtual Environments

Each service has its own virtual environment:
```
authentication/venv/
document-ingestion/venv/
document-parsing/venv/
information-structuring/venv/
risk-prediction/venv/
```

## ⚙️ Configuration

### Risk Prediction Model
To switch between HuggingFace and local model:

Edit `risk-prediction/.env`:
```env
# Use HuggingFace model (default)
USE_HUGGINGFACE_MODEL=true
HUGGINGFACE_MODEL_REPO=ishro/biogpt-aura

# Or use local model
# USE_HUGGINGFACE_MODEL=false
# LOCAL_MODEL_PATH=/path/to/local/model
```

## 🎯 Typical Workflow

1. **Login** → Get JWT token from authentication service
2. **Upload Document** → Send PDF to document-ingestion
3. **Parse Document** → Extract text from PDF
4. **Structure Data** → Use Gemini to extract structured fields
5. **Generate Prediction** → Get BI-RADS score and risk level
6. **Review Results** → GCF coordinator reviews predictions

## ✅ Current Status

- ✅ All services running
- ✅ HuggingFace model loaded
- ✅ Databases cleaned and ready
- ✅ Super admin created
- ✅ Predictions working correctly

## 📝 Files Created/Modified

### New Files
- `reset_and_restart.sh` - Complete reset script
- `risk-prediction/test_prediction_quick.py` - Quick prediction test
- `risk-prediction/check_database.py` - Database inspection tool
- `RESET_SUMMARY.md` - Detailed summary of fixes
- `QUICK_REFERENCE.md` - This file

### Modified Files
- `risk-prediction/app/config.py` - Fixed model paths, added HuggingFace config
- `authentication/requirements.txt` - Fixed bcrypt version

## 🎉 All Systems Operational!
