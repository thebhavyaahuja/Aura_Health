#!/usr/bin/env python3
"""
Download and cache HuggingFace model with progress indication
"""
import os
import sys

# Force unbuffered output for Docker
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

from transformers import AutoTokenizer, BioGptForSequenceClassification

def download_with_progress():
    """Download model with progress bar"""
    model_repo = os.environ.get('HUGGINGFACE_MODEL_REPO', 'ishro/biogpt-aura')
    
    print("\n" + "="*60, flush=True)
    print(f"📦 Downloading BioGPT Model: {model_repo}", flush=True)
    print("="*60 + "\n", flush=True)
    
    try:
        # Download tokenizer
        print("🔤 [1/2] Downloading tokenizer...", flush=True)
        print("    This includes: config, vocab, and special tokens", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(
            model_repo,
            trust_remote_code=True
        )
        print("    ✅ Tokenizer downloaded successfully!\n", flush=True)
        
        # Download model with progress
        print(f"🧠 [2/2] Downloading model weights...", flush=True)
        print("    Model: BioGPT (~347MB)", flush=True)
        print("    This may take 2-5 minutes depending on connection...", flush=True)
        
        model = BioGptForSequenceClassification.from_pretrained(
            model_repo,
            trust_remote_code=True
        )
        
        print("\n    ✅ Model downloaded and cached successfully!", flush=True)
        print(f"    📍 Cache location: {os.environ.get('TRANSFORMERS_CACHE', 'default')}", flush=True)
        print("="*60 + "\n", flush=True)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}", flush=True)
        print("="*60 + "\n", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    download_with_progress()
