#!/usr/bin/env python3
"""
Create a simple test PDF for testing the document parsing service
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path

def create_test_pdf():
    """Create a simple PDF with mammography report content"""
    
    # PDF content
    content = [
        "MAMMOGRAPHY REPORT",
        "",
        "Patient Information:",
        "Name: Jane Smith",
        "DOB: 01/15/1975",
        "Patient ID: 12345",
        "",
        "Exam Information:",
        "Date: 2024-01-15",
        "Indication: Routine screening mammography",
        "Technique: Digital mammography, bilateral CC and MLO views",
        "",
        "Clinical History:",
        "Patient presents for routine screening mammography.",
        "No breast symptoms or concerns.",
        "",
        "Findings:",
        "BREAST COMPOSITION: The breasts are heterogeneously dense,",
        "which may obscure small masses.",
        "",
        "RIGHT BREAST: No suspicious masses, architectural distortion,",
        "or suspicious calcifications identified.",
        "",
        "LEFT BREAST: No suspicious masses, architectural distortion,",
        "or suspicious calcifications identified.",
        "",
        "Assessment:",
        "BI-RADS Category 2: Benign findings",
        "",
        "Recommendation:",
        "Routine screening mammography in 12 months.",
        "",
        "Radiologist: Dr. Smith",
        "Date: 2024-01-15"
    ]
    
    # Create PDF
    filename = "test_mammography_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Add content
    y_position = height - 50
    for line in content:
        if y_position < 50:  # Start new page if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
        
        c.drawString(50, y_position, line)
        y_position -= 20
    
    c.save()
    
    print(f"✅ Created test PDF: {filename}")
    return filename

if __name__ == "__main__":
    create_test_pdf()
