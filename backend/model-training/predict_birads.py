import torch
import numpy as np
import sys
from transformers import (
    AutoTokenizer,
    BioGptForSequenceClassification,
    logging as hf_logging,
)
from scipy.special import softmax

# --- Configuration ---
# This MUST point to the directory where your best model was saved
MODEL_PATH = "./biogpt_birads_classifier/best_model"

# Suppress warnings
hf_logging.set_verbosity_error()

class BiradsPredictor:
    """
    A class to load the trained BI-RADS model and make predictions.
    """
    def __init__(self, model_path):
        print(f"--- Loading Model from {model_path} ---")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = BioGptForSequenceClassification.from_pretrained(model_path)
            
            # Check for GPU
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval() # Set model to evaluation mode (disables dropout)
            
            print(f"--- Model loaded successfully on {self.device} ---")
            
        except OSError:
            print(f"Error: Model not found at {model_path}")
            print("Please make sure you have trained the model and the path is correct.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while loading the model: {e}")
            sys.exit(1)

    def predict(self, report_text: str):
        """
        Predicts the BI-RADS score for a single report text.
        
        Args:
            report_text (str): The combined text of the report (Observations, etc.)

        Returns:
            dict: A dictionary containing the predicted label and probabilities.
        """
        if not report_text or not report_text.strip():
            print("Warning: Received empty report text.")
            return None

        # 1. Tokenize the input text
        inputs = self.tokenizer(
            report_text,
            return_tensors="pt", # Return PyTorch tensors
            padding="max_length",
            truncation=True,
            max_length=512
        )
        
        # Move tensors to the same device as the model
        inputs = {key: val.to(self.device) for key, val in inputs.items()}

        # 2. Get predictions (no gradients needed)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 'outputs.logits' contains the raw scores
        logits = outputs.logits
        
        # 3. Convert logits to probabilities
        # Move logits to CPU for numpy conversion
        scores = logits.cpu().numpy()[0]
        probabilities = softmax(scores)
        
        # 4. Get the predicted class ID
        predicted_label_id = np.argmax(probabilities)
        
        # 5. Map ID back to the original label (e.g., '4')
        predicted_label = self.model.config.id2label[predicted_label_id]
        
        # 6. Create a nice probability dictionary
        prob_dict = {
            self.model.config.id2label[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        return {
            "predicted_birads": predicted_label,
            "predicted_label_id": int(predicted_label_id),
            "probabilities": prob_dict
        }

# --- This is how you use the predictor ---
if __name__ == "__main__":
    
    # Create an instance of the predictor. This loads the model.
    predictor = BiradsPredictor(model_path=MODEL_PATH)

    # --- Example 1: A potentially suspicious report ---
    example_report_1 = (
        "Observations: Dense fibroglandular tissue. "
        "A 12mm irregular, spiculated mass is noted in the "
        "upper outer quadrant of the left breast. "
        "Conclusion: Suspicious finding. "
        "Recommendations: Ultrasound-guided biopsy is recommended."
    )
    
    print("\n--- Predicting for Example 1 ---")
    prediction_1 = predictor.predict(example_report_1)
    print(f"Report Text: {example_report_1[:100]}...")
    print(f"Predicted BI-RADS: {prediction_1['predicted_birads']}")
    print("Probabilities:")
    print(prediction_1['probabilities'])

    # --- Example 2: A clearly benign report ---
    example_report_2 = (
        "Observations: Scattered fibroglandular densities. "
        "No masses, calcifications, or architectural distortion. "
        "Skin and nipples are unremarkable. "
        "Conclusion: Negative mammogram. "
        "Recommendations: Routine screening mammogram in one year."
    )
    
    print("\n--- Predicting for Example 2 ---")
    prediction_2 = predictor.predict(example_report_2)
    print(f"Report Text: {example_report_2[:100]}...")
    print(f"Predicted BI-RADS: {prediction_2['predicted_birads']}")
    print("Probabilities:")
    print(prediction_2['probabilities'])
