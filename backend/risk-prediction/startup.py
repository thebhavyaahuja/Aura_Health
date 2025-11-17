#!/usr/bin/env python3
"""
Startup script for risk-prediction service
Ensures model is loaded before starting the server
"""
import os
import sys
import logging
from transformers import AutoTokenizer, BioGptForSequenceClassification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preload_model():
    """Preload the BioGPT model to ensure it's ready"""
    try:
        model_repo = os.getenv("HUGGINGFACE_MODEL_REPO", "ishro/biogpt-aura")
        logger.info(f"🔄 Loading BioGPT model from {model_repo}...")
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_repo)
        model = BioGptForSequenceClassification.from_pretrained(model_repo)
        
        logger.info("✅ Model loaded successfully!")
        logger.info(f"   Model config: {model.config.num_labels} classes")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to preload model: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting risk-prediction service...")
    
    # Preload model
    if preload_model():
        logger.info("✅ Model preloaded, starting server...")
        # Start the actual service
        os.system("python run.py")
    else:
        logger.error("❌ Model preload failed, but starting server anyway...")
        os.system("python run.py")
