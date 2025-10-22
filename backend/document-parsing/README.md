# 🔍 Document Parsing Service

**Purpose:** Extract text content from mammography reports using OCR and document parsing

## 🎯 Responsibilities
- Use `docling` for OCR and text extraction
- Convert PDFs, scanned images to markdown/text
- Handle different document formats (PDF, DOCX, images)
- Return structured text output
- Process files asynchronously

## 🛠️ Technology Stack
- **Framework:** FastAPI
- **OCR & Parsing:** docling
- **Database:** SQLite
- **Storage:** Local filesystem
- **Authentication:** API key-based

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
cd backend/document-parsing
pip install -r requirements.txt
```

### Running the Service
```bash
# Option 1: Using the run script
python3 run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Testing
```bash
# Test parsing functionality
python3 test_parsing.py

# Test with real PDF
python3 test_with_pdf.py your_document.pdf

# End-to-end test (requires Document Ingestion Service)
python3 test_end_to_end.py
```

## 📋 API Endpoints

### Authentication
All endpoints require an API key as a query parameter:
```
?api_key=demo-api-key-123
```

### Core Endpoints

#### Parse Document
```http
POST /parsing/parse?api_key=demo-api-key-123
Content-Type: application/json

{
  "document_id": "uuid",
  "file_path": "/path/to/document.pdf"
}
```

**Response:**
```json
{
  "parsing_id": "uuid",
  "document_id": "uuid",
  "status": "completed",
  "message": "Document parsed successfully"
}
```

#### Get Parsing Result
```http
GET /parsing/result/{parsing_id}?api_key=demo-api-key-123
```

**Response:**
```json
{
  "parsing_id": "uuid",
  "document_id": "uuid",
  "extracted_text": "# Extracted Text\n\n...",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Result by Document ID
```http
GET /parsing/result/document/{document_id}?api_key=demo-api-key-123
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
PORT=8002                                  # Port to run on

# Storage Settings
STORAGE_DIR=./storage                      # Local storage directory
PARSED_DIR=./storage/parsed                # Parsed files directory
TEMP_DIR=./storage/temp                    # Temporary files directory

# Database Settings
DATABASE_URL=sqlite:///./parsing.db        # SQLite database URL

# Service URLs
DOCUMENT_INGESTION_URL=http://localhost:8000
INFORMATION_STRUCTURING_URL=http://localhost:8003
```

### File Storage Structure
```
storage/
├── parsed/
│   └── document_id.md                     # Parsed text files
└── temp/                                  # Temporary files
```

## 🔄 Service Integration

### Input from Document Ingestion Service
```python
# Document Ingestion Service automatically calls:
POST http://localhost:8002/parsing/parse
{
  "document_id": "uuid",
  "file_path": "/path/to/uploaded/file.pdf"
}
```

### Output to Information Structuring Service
```python
# Document Parsing Service automatically calls:
POST http://localhost:8003/api/v1/structure
{
  "document_id": "uuid",
  "extracted_text": "Parsed mammography report text..."
}
```

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8002/health/

# Test parsing
curl -X POST "http://localhost:8002/parsing/parse?api_key=demo-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "test-123", "file_path": "/path/to/file.pdf"}'

# Test result retrieval
curl "http://localhost:8002/parsing/result/test-123?api_key=demo-api-key-123"
```

### Automated Testing
```bash
# Run all tests
python3 test_parsing.py

# Test with specific file
python3 test_with_pdf.py your_document.pdf
```

## 📊 Supported File Types

- **PDF Files**: Text-based and scanned PDFs
- **Images**: PNG, JPG, TIFF (with OCR)
- **Documents**: DOCX, DOC
- **Text Files**: Plain text (direct reading)

## 🔒 Security Features

- **API Key Authentication**: Simple key-based auth
- **File Validation**: Checks file existence and accessibility
- **Error Handling**: Comprehensive error responses
- **Input Sanitization**: Validates input parameters

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t document-parsing .

# Run container
docker run -d \
  --name document-parsing \
  -p 8002:8002 \
  -v $(pwd)/storage:/app/storage \
  document-parsing
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI:** `http://localhost:8002/docs`
- **ReDoc:** `http://localhost:8002/redoc`

## 🐛 Troubleshooting

### Common Issues

#### 1. Docling Model Download
First-time PDF processing may take time as docling downloads OCR models:
```bash
# Check if docling is processing
ps aux | grep python
# Wait for model download to complete
```

#### 2. File Not Found
```bash
# Ensure file path is correct and accessible
ls -la /path/to/your/document.pdf
```

#### 3. Service Not Responding
```bash
# Check if service is running
curl http://localhost:8002/health/
# Check logs for errors
```

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## 📈 Performance Notes

- **First PDF**: May take 2-3 minutes (model download)
- **Subsequent PDFs**: Usually 10-30 seconds
- **Text Files**: Very fast (< 1 second)
- **Large Images**: May take longer for OCR processing

## 🔄 Development Status
**Status:** ✅ Implemented and Ready
**Owner:** You
**Priority:** High
**Last Updated:** 2024-01-15
