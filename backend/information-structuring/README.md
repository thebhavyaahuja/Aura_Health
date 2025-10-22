# 🧠 Information Structuring Service

**Purpose:** Transform parsed mammography reports into structured JSON using Google Gemini API

## 🎯 Responsibilities
- Extract structured medical data from mammography report text
- Use Google Gemini API for intelligent text analysis
- Convert unstructured text to standardized JSON format
- Calculate confidence scores for extracted data
- Trigger Feature Engineering Service

## 🛠️ Technology Stack
- **Framework:** FastAPI
- **LLM:** Google Gemini API
- **Database:** SQLite
- **Storage:** Local filesystem
- **Authentication:** API key-based

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API key
- pip

### Installation
```bash
cd backend/information-structuring
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with the following variables:
```bash
# Copy from example
cp env.example .env

# Edit .env file
nano .env
```

**Required Environment Variables:**
```bash
# API Configuration
API_KEY=demo-api-key-123
HOST=0.0.0.0
PORT=8003

# Google Gemini API (REQUIRED)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Database
DATABASE_URL=sqlite:///./structuring.db

# Service URLs
DOCUMENT_PARSING_URL=http://localhost:8002
FEATURE_ENGINEERING_URL=http://localhost:8004
```

### Getting Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### Running the Service
```bash
# Option 1: Using the run script
python3 run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

### Testing
```bash
# Test structuring functionality
python3 test_structuring.py

# End-to-end pipeline test (requires all services and input file)
python3 test_pipeline.py your_document.pdf
python3 test_pipeline.py test.png
python3 test_pipeline.py /path/to/mammography_report.pdf
```

## 📋 API Endpoints

### Authentication
All endpoints require an API key as a query parameter:
```
?api_key=demo-api-key-123
```

### Core Endpoints

#### Structure Document
```http
POST /structuring/structure?api_key=demo-api-key-123
Content-Type: application/json

{
  "document_id": "uuid",
  "extracted_text": "Mammography report text..."
}
```

**Response:**
```json
{
  "structuring_id": "uuid",
  "document_id": "uuid",
  "status": "completed",
  "message": "Document structured successfully"
}
```

#### Get Structuring Result
```http
GET /structuring/result/{structuring_id}?api_key=demo-api-key-123
```

**Response:**
```json
{
  "structuring_id": "uuid",
  "document_id": "uuid",
  "structured_data": {
    "indication": "routine screening",
    "family_history_breast_pathology": "mother had breast cancer",
    "clinical_exam_result": "normal",
    "skin_abnormalities": "none",
    "nipple_abnormalities": "none",
    "gland_density": "heterogeneously dense",
    "calcifications_present": "no",
    "architectural_distortion": "none",
    "retracted_areas": "none",
    "suspicious_lymph_nodes": "no",
    "evaluation_possible": "yes",
    "findings_summary": "No suspicious findings",
    "acr_density_type": "C",
    "birads_score": "2",
    "followup_recommended": "yes",
    "recommendation_text": "Routine screening in 12 months",
    "lmp": "unknown",
    "hormonal_therapy": "unknown",
    "age": "49",
    "children": "2"
  },
  "confidence_score": 0.85,
  "model_used": "gemini",
  "processing_time": 3,
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Result by Document ID
```http
GET /structuring/result/document/{document_id}?api_key=demo-api-key-123
```

### Health Check Endpoints
```http
GET /health/          # Overall health check
GET /health/ready     # Readiness check
GET /health/live      # Liveness check
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
API_KEY=demo-api-key-123                    # API key for authentication
HOST=0.0.0.0                               # Host to bind to
PORT=8003                                  # Port to run on

# Google Gemini API (REQUIRED)
GEMINI_API_KEY=your_api_key_here           # Google Gemini API key
GEMINI_MODEL=gemini-1.5-flash              # Gemini model to use

# Database Settings
DATABASE_URL=sqlite:///./structuring.db    # SQLite database URL

# Storage Settings
STORAGE_DIR=./storage                      # Local storage directory
RESULTS_DIR=./storage/results              # Structured results directory

# Service URLs
DOCUMENT_PARSING_URL=http://localhost:8002
FEATURE_ENGINEERING_URL=http://localhost:8004

# Logging
LOG_LEVEL=INFO                             # Logging level
```

### File Storage Structure
```
storage/
└── results/
    └── document_id.json                   # Structured data files
```

## 🔄 Service Integration

### Input from Document Parsing Service
```python
# Document Parsing Service automatically calls:
POST http://localhost:8003/structuring/structure
{
  "document_id": "uuid",
  "extracted_text": "Parsed mammography report text..."
}
```

### Output to Feature Engineering Service
```python
# Information Structuring Service automatically calls:
POST http://localhost:8004/api/v1/features
{
  "document_id": "uuid",
  "structured_data": {
    "indication": "routine screening",
    "birads_score": "2",
    # ... all other fields
  }
}
```

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8003/health/

# Test structuring
curl -X POST "http://localhost:8003/structuring/structure?api_key=demo-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "test-123", "extracted_text": "Mammography report text..."}'

# Test result retrieval
curl "http://localhost:8003/structuring/result/test-123?api_key=demo-api-key-123"
```

### Automated Testing
```bash
# Run structuring service tests
python3 test_structuring.py

# Run complete pipeline test with your file
python3 test_pipeline.py your_document.pdf
```

## 📊 Structured Data Schema

The service extracts the following fields from mammography reports:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `indication` | Reason for mammography | "routine screening", "follow-up" |
| `family_history_breast_pathology` | Family history | "mother had breast cancer" |
| `clinical_exam_result` | Clinical examination | "normal", "abnormal" |
| `skin_abnormalities` | Skin issues | "none", "dimpling" |
| `nipple_abnormalities` | Nipple issues | "none", "retraction" |
| `gland_density` | Breast density description | "heterogeneously dense" |
| `calcifications_present` | Calcifications | "yes", "no", "unknown" |
| `architectural_distortion` | Distortion | "none", "present" |
| `retracted_areas` | Retracted areas | "none", "present" |
| `suspicious_lymph_nodes` | Lymph nodes | "yes", "no", "unknown" |
| `evaluation_possible` | Evaluation possible | "yes", "no", "unknown" |
| `findings_summary` | Summary of findings | "No suspicious findings" |
| `acr_density_type` | ACR density category | "A", "B", "C", "D" |
| `birads_score` | BI-RADS score | "0", "1", "2", "3", "4", "5", "6" |
| `followup_recommended` | Follow-up needed | "yes", "no", "unknown" |
| `recommendation_text` | Recommendations | "Routine screening in 12 months" |
| `lmp` | Last menstrual period | "01/15/2024" |
| `hormonal_therapy` | Hormonal therapy | "yes", "no", "unknown" |
| `age` | Patient age | "49" |
| `children` | Number of children | "2" |

## 🔒 Security Features

- **API Key Authentication**: Simple key-based auth
- **Input Validation**: Validates input parameters
- **Error Handling**: Comprehensive error responses
- **Rate Limiting**: Built into Gemini API

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t information-structuring .

# Run container
docker run -d \
  --name information-structuring \
  -p 8003:8003 \
  -e GEMINI_API_KEY=your_api_key \
  -v $(pwd)/storage:/app/storage \
  information-structuring
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI:** `http://localhost:8003/docs`
- **ReDoc:** `http://localhost:8003/redoc`

## 🐛 Troubleshooting

### Common Issues

#### 1. Gemini API Key Not Configured
```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Add to .env file
echo "GEMINI_API_KEY=your_key_here" >> .env
```

#### 2. API Rate Limits
```bash
# Check Gemini API usage
# Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
```

#### 3. Service Not Responding
```bash
# Check if service is running
curl http://localhost:8003/health/

# Check logs for errors
```

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## 📈 Performance Notes

- **Gemini API Response**: Usually 2-5 seconds
- **Confidence Scoring**: Based on field completeness
- **Processing Time**: Typically 3-10 seconds total
- **Rate Limits**: 15 requests per minute (free tier)

## 🔄 Development Status
**Status:** ✅ Implemented and Ready
**Owner:** You
**Priority:** High
**Last Updated:** 2024-01-15