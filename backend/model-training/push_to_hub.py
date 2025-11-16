#!/usr/bin/env python3
"""
Push trained model to HuggingFace Hub
"""

from transformers import AutoTokenizer, BioGptForSequenceClassification
from huggingface_hub import HfApi, login
import sys
import os

# Configuration
MODEL_PATH = "./biogpt_birads_classifier/best_model"
REPO_ID = "ishro/biogpt-aura"

def push_to_hub():
    print("="*60)
    print("Push Model to HuggingFace Hub")
    print("="*60)
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"\n❌ Error: Model not found at {MODEL_PATH}")
        print("Please train the model first.")
        sys.exit(1)
    
    print(f"\nModel path: {MODEL_PATH}")
    print(f"Repository: {REPO_ID}")
    print(f"URL: https://huggingface.co/{REPO_ID}")
    
    # Check if already logged in
    print("\n--- Step 1: Checking HuggingFace Authentication ---")
    try:
        api = HfApi()
        user_info = api.whoami()
        print(f"✓ Already logged in as: {user_info['name']}")
    except Exception as e:
        print("\n❌ Not logged in to HuggingFace")
        print("\nPlease run ONE of these commands first:")
        print("  1. huggingface-cli login")
        print("  2. python -c 'from huggingface_hub import login; login()'")
        print("\nThen run this script again.")
        sys.exit(1)
    
    # Load model and tokenizer
    print("\n--- Step 2: Loading Model and Tokenizer ---")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = BioGptForSequenceClassification.from_pretrained(MODEL_PATH)
        print("✓ Model and tokenizer loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)
    
    # Show model info
    print(f"\n--- Model Information ---")
    print(f"Number of labels: {model.config.num_labels}")
    print(f"Label mapping: {model.config.id2label}")
    
    # Push to hub
    print(f"\n--- Step 3: Pushing to HuggingFace Hub ---")
    print("This may take a few minutes...")
    
    try:
        # Push model
        print("\n📤 Pushing model...")
        model.push_to_hub(
            REPO_ID,
            commit_message="Upload BioGPT BI-RADS classifier - 97.36% accuracy",
            private=False  # Set to True if you want a private repo
        )
        print("✓ Model pushed successfully")
        
        # Push tokenizer
        print("\n📤 Pushing tokenizer...")
        tokenizer.push_to_hub(
            REPO_ID,
            commit_message="Upload tokenizer for BioGPT BI-RADS classifier"
        )
        print("✓ Tokenizer pushed successfully")
        
        # Create and push model card
        print("\n📝 Creating model card...")
        model_card = f"""---
language: en
tags:
- biogpt
- medical
- radiology
- birads
- classification
license: mit
metrics:
- accuracy
- f1
model-index:
- name: BioGPT BI-RADS Classifier
  results:
  - task:
      type: text-classification
      name: BI-RADS Classification
    metrics:
    - type: accuracy
      value: 0.9736
      name: Accuracy
    - type: f1
      value: 0.9066
      name: F1 (Macro)
---

# BioGPT BI-RADS Classifier

This model is a fine-tuned version of [microsoft/biogpt-large](https://huggingface.co/microsoft/biogpt-large) for BI-RADS classification of radiology reports.

## Model Description

- **Base Model:** microsoft/biogpt-large
- **Task:** Multi-class text classification (BI-RADS categories 0-6)
- **Training Data:** Radiology reports with BI-RADS annotations
- **Accuracy:** 97.36%
- **F1-Score (Macro):** 90.66%

## Performance

### Overall Metrics
- **Accuracy:** 97.36%
- **F1-Score (Macro):** 90.66%
- **F1-Score (Weighted):** 97.34%
- **Precision (Macro):** 92.65%
- **Recall (Macro):** 88.96%

### Per-Class Performance
| BI-RADS | Precision | Recall | F1-Score | Support |
|---------|-----------|--------|----------|---------|
| 0       | 0.9946    | 0.9482 | 0.9708   | 193     |
| 1       | 0.9504    | 0.9664 | 0.9583   | 119     |
| 2       | 0.9740    | 0.9943 | 0.9840   | 527     |
| 3       | 1.0000    | 0.8333 | 0.9091   | 18      |
| 4       | 0.9000    | 0.8182 | 0.8571   | 11      |
| 5       | 0.6667    | 0.6667 | 0.6667   | 3       |
| 6       | 1.0000    | 1.0000 | 1.0000   | 1       |

## Usage

```python
from transformers import AutoTokenizer, BioGptForSequenceClassification
import torch

# Load model and tokenizer
model = BioGptForSequenceClassification.from_pretrained("{REPO_ID}")
tokenizer = AutoTokenizer.from_pretrained("{REPO_ID}")

# Prepare input
report_text = "Your radiology report text here..."
inputs = tokenizer(report_text, return_tensors="pt", padding=True, truncation=True, max_length=512)

# Get prediction
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=-1).item()

# Map to BI-RADS label
birads_label = model.config.id2label[predicted_class]
print(f"Predicted BI-RADS: {{birads_label}}")
print(f"Confidence: {{predictions[0][predicted_class].item():.4f}}")
```

## Training Details

### Training Hyperparameters
- **Learning Rate:** 2e-5
- **Batch Size:** 4 per device (2 GPUs)
- **Gradient Accumulation Steps:** 8
- **Effective Batch Size:** 64
- **Epochs:** 3
- **Optimizer:** AdamW (fused)
- **Mixed Precision:** BF16
- **Hardware:** 2x NVIDIA L40S (46GB each)

### Training Data
The model was trained on radiology reports with the following features:
- Report observations
- Conclusions
- Recommendations
- Patient metadata (age, hormonal therapy, family history, etc.)

## Limitations
- Performance on BI-RADS categories 5 and 6 is lower due to limited training samples
- Model is trained on specific radiology report format
- May not generalize well to reports from different institutions without fine-tuning

## Ethical Considerations
- This model is intended for research purposes and should not be used as the sole basis for clinical decisions
- Always consult with qualified medical professionals for diagnosis and treatment
- The model may have biases based on the training data distribution

## Citation
If you use this model, please cite:
```bibtex
@misc{{biogpt-birads-classifier,
  author = {{Your Name}},
  title = {{BioGPT BI-RADS Classifier}},
  year = {{2025}},
  publisher = {{HuggingFace}},
  url = {{https://huggingface.co/{REPO_ID}}}
}}
```

## Model Card Authors
{user_info['name']}

## Model Card Contact
For questions or issues, please open an issue on the model repository.
"""
        
        # Push model card
        api.upload_file(
            path_or_fileobj=model_card.encode(),
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="Add model card with evaluation results"
        )
        print("✓ Model card created and pushed")
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Model pushed to HuggingFace Hub")
        print("="*60)
        print(f"\n🌐 View your model at:")
        print(f"   https://huggingface.co/{REPO_ID}")
        print(f"\n📦 Load your model with:")
        print(f"   from transformers import BioGptForSequenceClassification")
        print(f"   model = BioGptForSequenceClassification.from_pretrained('{REPO_ID}')")
        print()
        
    except Exception as e:
        print(f"\n❌ Error pushing to hub: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're logged in: huggingface-cli login")
        print("2. Check you have write access to the repository")
        print("3. Verify your internet connection")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        push_to_hub()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
