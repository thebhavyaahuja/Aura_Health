"""
Pydantic schemas for Information Structuring Service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class StructureRequest(BaseModel):
    """Request model for document structuring"""
    document_id: str = Field(..., description="Document ID from parsing service")
    extracted_text: str = Field(..., description="Extracted text from parsing service")

class StructureResponse(BaseModel):
    """Response model for structuring request"""
    structuring_id: str
    document_id: str
    status: str
    message: str

class StructuredData(BaseModel):
    """Structured mammography data model"""
    indication: str = Field(default="unknown", description="Reason for mammography")
    family_history_breast_pathology: str = Field(default="unknown", description="Family history of breast issues")
    clinical_exam_result: str = Field(default="unknown", description="Clinical examination results")
    skin_abnormalities: str = Field(default="unknown", description="Skin abnormalities")
    nipple_abnormalities: str = Field(default="unknown", description="Nipple abnormalities")
    gland_density: str = Field(default="unknown", description="Breast gland density")
    calcifications_present: str = Field(default="unknown", description="Presence of calcifications")
    architectural_distortion: str = Field(default="unknown", description="Architectural distortion")
    retracted_areas: str = Field(default="unknown", description="Retracted areas")
    suspicious_lymph_nodes: str = Field(default="unknown", description="Suspicious lymph nodes")
    evaluation_possible: str = Field(default="unknown", description="Whether evaluation is possible")
    findings_summary: str = Field(default="unknown", description="Summary of findings")
    acr_density_type: str = Field(default="unknown", description="ACR density type (A, B, C, D)")
    birads_score: str = Field(default="unknown", description="BI-RADS score (0-6)")
    followup_recommended: str = Field(default="unknown", description="Follow-up recommended")
    recommendation_text: str = Field(default="unknown", description="Recommendation text")
    lmp: str = Field(default="unknown", description="Last menstrual period")
    hormonal_therapy: str = Field(default="unknown", description="Hormonal therapy status")
    age: str = Field(default="unknown", description="Patient age")
    children: str = Field(default="unknown", description="Number of children")

class StructuringResult(BaseModel):
    """Complete structuring result model"""
    structuring_id: str
    document_id: str
    structured_data: StructuredData
    confidence_score: Optional[float]
    model_used: str
    processing_time: Optional[int]
    status: str
    created_at: datetime

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    database: str
    gemini_api: str
