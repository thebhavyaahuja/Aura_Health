import os
from rapidocr import get_ocr

# Ensure the model directory exists
model_dir = os.path.expanduser("~/.cache/RapidOCR")
os.makedirs(model_dir, exist_ok=True)

print("Downloading RapidOCR models...")

# Initialize the OCR engine, which will trigger the download
# of the detection, classification, and recognition models.
get_ocr()

print("Model download complete.")
