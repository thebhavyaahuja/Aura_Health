# 📥 Document Ingestion Service

**Purpose:** Handle file uploads and initial document processing for mammography reports

## 🎯 Responsibilities
- Accept PDF, image, and text file uploads
- File validation and security checks
- Store files in local filesystem (with cloud storage support)
- Track processing status and metadata
- Provide document management capabilities

## 🛠️ Technology Stack
- **Framework:** FastAPI
- **File Storage:** Local filesystem (organized by date)
- **Validation:** python-magic, Pillow
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** API key-based
- **File Types:** PDF, DOCX, PNG, JPG, TIFF

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
cd backend/document-ingestion
pip install -r requirements.txt
```

### Running the Service
```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Using Docker
docker build -t document-ingestion .
docker run -p 8000:8000 document-ingestion
```

### Testing
```bash
# Run tests
python run_tests.py

# Test upload functionality
python test_upload.py
```

## 📋 API Endpoints

### Authentication
All endpoints require an API key as a query parameter:
```
?api_key=demo-api-key-123
```

### Core Endpoints

#### Upload Document
```http
POST /documents/upload?api_key=demo-api-key-123
Content-Type: multipart/form-data

Form Data:
- file: [binary file]
- uploader_id: string (required)
- patient_id: string (optional)
- description: string (optional)
```

**Response:**
```json
{
  "upload_id": "uuid",
  "status": "uploaded",
  "file_info": {
    "filename": "report.pdf",
    "size": 1024000,
    "content_type": "application/pdf"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "message": "Document uploaded successfully"
}
```

#### Get Document Status
```http
GET /documents/{document_id}?api_key=demo-api-key-123
```

**Response:**
```json
{
  "upload_id": "uuid",
  "status": "uploaded",
  "file_info": {
    "filename": "report.pdf",
    "size": 1024000,
    "content_type": "application/pdf"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "processing_statuses": [
    {
      "service_name": "document_ingestion",
      "status": "completed",
      "error_message": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### List Documents
```http
GET /documents/?api_key=demo-api-key-123&page=1&limit=10&status=uploaded
```

**Response:**
```json
{
  "documents": [...],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

#### Delete Document
```http
DELETE /documents/{document_id}?api_key=demo-api-key-123
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
PORT=8000                                  # Port to run on

# File Upload Settings
MAX_FILE_SIZE=10485760                     # 10MB max file size
ALLOWED_EXTENSIONS=pdf,docx,png,jpg,tiff   # Allowed file extensions

# Storage Settings
STORAGE_DIR=./storage                      # Local storage directory
UPLOADS_DIR=./storage/uploads              # Upload directory
TEMP_DIR=./storage/temp                    # Temporary files directory

# Database Settings
DATABASE_URL=sqlite:///./database.db       # SQLite database URL
```

### File Storage Structure
```
storage/
├── uploads/
│   ├── 2024/01/15/          # Date-based organization
│   │   └── uuid-filename.pdf
│   └── temp/                # Temporary files
└── database.db              # SQLite database
```

## 🔄 Service Integration

### For Document Parsing Service
The Document Ingestion Service is designed to work with the Document Parsing Service:

1. **Upload Flow:**
   ```
   Client → Document Ingestion → Local Storage → Database
   ```

2. **Processing Flow:**
   ```
   Document Parsing Service → Read from Storage → Process → Update Status
   ```

### Integration Points
- **File Storage:** Documents are stored in organized directories
- **Database:** Metadata is stored in SQLite/PostgreSQL
- **Status Tracking:** Processing statuses are tracked per document
- **API Communication:** RESTful API for service-to-service communication

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/health/

# Test upload
curl -X POST "http://localhost:8000/documents/upload?api_key=demo-api-key-123" \
  -F "file=@test_document.pdf" \
  -F "uploader_id=test_user" \
  -F "patient_id=patient_123"

# Test document listing
curl "http://localhost:8000/documents/?api_key=demo-api-key-123"
```

### Automated Testing
```bash
# Run all tests
python run_tests.py

# Run specific test file
pytest tests/test_main.py -v
```

## 📊 Monitoring & Logging

### Health Checks
- **Database connectivity** check
- **Storage availability** check
- **Service dependencies** check

### Logging
- **Request/Response logging**
- **Error logging with stack traces**
- **File upload/processing events**

### Metrics
- Upload success/failure rates
- File processing times
- Storage usage
- API response times

## 🔒 Security Features

### File Validation
- **Size limits:** 10MB maximum
- **Type validation:** Magic number checking
- **Extension validation:** Whitelist of allowed extensions
- **Content scanning:** Basic malware detection

### Authentication
- **API key-based authentication**
- **Rate limiting** (configurable)
- **Input sanitization**

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t document-ingestion .

# Run container
docker run -d \
  --name document-ingestion \
  -p 8000:8000 \
  -v $(pwd)/storage:/app/storage \
  document-ingestion
```

### Environment Setup
```bash
# Production environment variables
export API_KEY=your-secure-api-key
export MAX_FILE_SIZE=52428800  # 50MB
export DATABASE_URL=postgresql://user:pass@host:port/db
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### OpenAPI Specification
- **JSON:** `http://localhost:8000/openapi.json`

## 🐛 Troubleshooting

### Common Issues

#### 1. Module Import Errors
```bash
# Make sure you're in the correct directory
cd backend/document-ingestion
python run.py
```

#### 2. File Upload Errors
- Check file size (max 10MB)
- Verify file type is allowed
- Ensure API key is correct

#### 3. Database Errors
- Check if database file exists
- Verify write permissions
- Check disk space

#### 4. Storage Errors
- Verify storage directory exists
- Check write permissions
- Ensure sufficient disk space

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## 📈 Performance Considerations

### File Size Limits
- **Default:** 10MB per file
- **Configurable:** Via environment variables
- **Validation:** Both client and server-side

### Storage Optimization
- **Date-based organization** for easy cleanup
- **Unique filenames** to prevent conflicts
- **Temporary file cleanup** (1-hour retention)

### Database Performance
- **Indexed queries** on document ID and status
- **Pagination** for large result sets
- **Connection pooling** for production

## 🔄 Future Enhancements

### Planned Features
- [ ] Cloud storage integration (S3, GCS, Azure)
- [ ] Advanced file validation (virus scanning)
- [ ] Batch upload support
- [ ] File compression
- [ ] Advanced search and filtering
- [ ] Webhook notifications
- [ ] Rate limiting per user
- [ ] File versioning

### Integration Roadmap
- [ ] Document Parsing Service integration
- [ ] Information Structuring Service integration
- [ ] Feature Engineering Service integration
- [ ] Risk Prediction Service integration

## 📞 Support

### Development Status
**Status:** ✅ Implemented and Ready
**Owner:** You
**Priority:** High
**Last Updated:** 2024-01-15

### Getting Help
- Check the API documentation at `/docs`
- Review the test files for usage examples
- Check the logs for error details
- Verify configuration settings
