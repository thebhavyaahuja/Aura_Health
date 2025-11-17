#!/usr/bin/env python3
"""
Download and cache HuggingFace model with progress indication
"""
import os
import sys
from transformers import AutoTokenizer, BioGptForSequenceClassification
from tqdm import tqdm

def download_with_progress():
    """Download model with progress bar"""
    model_repo = os.environ.get('HUGGINGFACE_MODEL_REPO', 'ishro/biogpt-aura')
    
    print("\n" + "="*60)
    print(f"📦 Downloading BioGPT Model: {model_repo}")
    print("="*60 + "\n")
    
    try:
        # Download tokenizer
        print("🔤 [1/2] Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_repo,
            trust_remote_code=True
        )
        print("✅ Tokenizer downloaded successfully!\n")
        
        # Download model with progress
        print(f"🧠 [2/2] Downloading model (this may take a few minutes)...")
        print("    Model size: ~347MB (BioGPT)")
        print("    Please wait...\n")
        
        model = BioGptForSequenceClassification.from_pretrained(
            model_repo,
            trust_remote_code=True
        )
        
        print("\n✅ Model downloaded and cached successfully!")
        print(f"📍 Cache location: {os.environ.get('TRANSFORMERS_CACHE', 'default')}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        print("="*60 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    download_with_progress()
