#!/usr/bin/env python3
"""
Multi-GPU Evaluation Script using Accelerate
This properly distributes evaluation across 2 GPUs
"""

import pandas as pd
import numpy as np
import torch
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    precision_score, 
    recall_score,
    confusion_matrix,
    classification_report
)
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    BioGptForSequenceClassification,
)
from accelerate import Accelerator
from torch.utils.data import DataLoader

# --- Configuration ---
FILE_NAME = "radiology_reports.csv"
DELIMITER = ";"
TEXT_COLUMNS = ["Observations", "Conclusion", "Recommendations", "Reason"]
TABULAR_COLUMNS = ["Hormonal_Therapy", "Family_History", "Age", "Children"]
TARGET_COLUMN = "BI-RADS"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PATH = "./biogpt_birads_classifier/best_model"
BATCH_SIZE = 16  # Per device

def load_and_preprocess_data():
    """Load and preprocess the data"""
    print(f"--- Loading Data from {FILE_NAME} ---")
    df = pd.read_csv(FILE_NAME, delimiter=DELIMITER)
    print(f"Loaded {len(df)} reports.")
    
    # Fill missing values
    for col in TEXT_COLUMNS:
        df[col] = df[col].fillna("")
    for col in TABULAR_COLUMNS:
        df[col] = df[col].fillna("Unknown").astype(str)
    
    # Create text
    df['report_text'] = df[TEXT_COLUMNS].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    def create_metadata_string(row):
        parts = [
            f"Medical Unit: {row['Medical_Unit']}",
            f"Hormonal Therapy: {row['Hormonal_Therapy']}",
            f"Family History: {row['Family_History']}",
            f"Age: {row['Age']}",
            f"Children: {row['Children']}"
        ]
        return ". ".join(parts) + "."
    
    df['metadata_text'] = df.apply(create_metadata_string, axis=1)
    df['text'] = df['metadata_text'] + " [REPORT] " + df['report_text']
    df = df.dropna(subset=[TARGET_COLUMN])
    
    # Labels
    unique_labels = sorted([int(l) for l in df[TARGET_COLUMN].unique()])
    label2id = {label: i for i, label in enumerate(unique_labels)}
    id2label = {i: label for label, i in label2id.items()}
    
    df['label'] = df[TARGET_COLUMN].map(label2id)
    final_df = df[['text', 'label', TARGET_COLUMN]]
    
    return final_df, label2id, id2label

def evaluate_model():
    # Initialize Accelerator
    accelerator = Accelerator()
    
    if accelerator.is_main_process:
        print("="*60)
        print("BioGPT Multi-GPU Evaluation with Accelerate")
        print("="*60)
        print(f"Number of GPUs: {accelerator.num_processes}")
    
    # Load data
    df, label2id, id2label = load_and_preprocess_data()
    
    # Split
    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=df['label']
    )
    
    if accelerator.is_main_process:
        print(f"\nTest set size: {len(test_df)} samples")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = BioGptForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    
    # Tokenize test data
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            padding="max_length",
            truncation=True,
            max_length=512
        )
    
    test_dataset = Dataset.from_pandas(test_df.copy())
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    
    # Remove non-model columns
    cols_to_remove = [TARGET_COLUMN, 'text']
    if '__index_level_0__' in tokenized_test.column_names:
        cols_to_remove.append('__index_level_0__')
    tokenized_test = tokenized_test.remove_columns(cols_to_remove)
    
    # Rename 'label' to 'labels' (model expects 'labels')
    tokenized_test = tokenized_test.rename_column('label', 'labels')
    tokenized_test.set_format("torch")
    
    # Create dataloader
    test_dataloader = DataLoader(
        tokenized_test, 
        batch_size=BATCH_SIZE,
        shuffle=False
    )
    
    # Prepare with accelerator
    model, test_dataloader = accelerator.prepare(model, test_dataloader)
    
    if accelerator.is_main_process:
        print(f"\n--- Running Evaluation on {accelerator.num_processes} GPUs ---")
    
    # Run predictions
    all_predictions = []
    all_labels = []
    
    with torch.no_grad():
        for batch_idx, batch in enumerate(test_dataloader):
            outputs = model(**batch)
            logits = outputs.logits
            
            # Gather from all GPUs
            logits = accelerator.gather_for_metrics(logits)
            labels = accelerator.gather_for_metrics(batch['labels'])
            
            all_predictions.append(logits.cpu().numpy())
            all_labels.append(labels.cpu().numpy())
            
            if accelerator.is_main_process and batch_idx % 10 == 0:
                total_batches = len(test_dataloader)
                print(f"  Processed {batch_idx}/{total_batches} batches...")
    
    # Only main process computes metrics
    if accelerator.is_main_process:
        # Concatenate all predictions
        all_logits = np.vstack(all_predictions)
        true_label_ids = np.concatenate(all_labels)
        predicted_label_ids = np.argmax(all_logits, axis=1)
        
        # Trim to actual test set size (gather might add padding)
        true_label_ids = true_label_ids[:len(test_df)]
        predicted_label_ids = predicted_label_ids[:len(test_df)]
        
        # Map back to original labels
        predicted_birads = [id2label[lid] for lid in predicted_label_ids]
        true_birads = test_df[TARGET_COLUMN].values
        
        # Calculate metrics
        print("\n" + "="*60)
        print("EVALUATION RESULTS")
        print("="*60)
        
        accuracy = accuracy_score(true_label_ids, predicted_label_ids)
        f1_macro = f1_score(true_label_ids, predicted_label_ids, average='macro')
        f1_weighted = f1_score(true_label_ids, predicted_label_ids, average='weighted')
        precision = precision_score(true_label_ids, predicted_label_ids, average='macro')
        recall = recall_score(true_label_ids, predicted_label_ids, average='macro')
        
        print(f"\n📊 Overall Metrics:")
        print(f"  Accuracy:            {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"  F1-Score (Macro):    {f1_macro:.4f}")
        print(f"  F1-Score (Weighted): {f1_weighted:.4f}")
        print(f"  Precision (Macro):   {precision:.4f}")
        print(f"  Recall (Macro):      {recall:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(true_label_ids, predicted_label_ids)
        label_names = [id2label[i] for i in range(len(id2label))]
        
        print(f"\n📈 Confusion Matrix:")
        print(f"\n     Predicted →")
        print(f"True ↓  {' '.join([f'{l:>5}' for l in label_names])}")
        for i, row in enumerate(cm):
            print(f"{label_names[i]:>5}   {' '.join([f'{val:>5}' for val in row])}")
        
        # Classification Report
        print(f"\n📋 Detailed Classification Report:")
        print(classification_report(
            true_label_ids, 
            predicted_label_ids,
            target_names=[f"BI-RADS {label}" for label in label_names],
            digits=4
        ))
        
        # Per-class accuracy
        print(f"\n🎯 Per-Class Accuracy:")
        for i, label in enumerate(label_names):
            mask = true_label_ids == i
            if mask.sum() > 0:
                class_acc = (predicted_label_ids[mask] == i).sum() / mask.sum()
                print(f"  BI-RADS {label}: {class_acc:.4f} ({class_acc*100:.2f}%) - {mask.sum()} samples")
        
        # Sample predictions
        print(f"\n📝 Sample Predictions (first 10):")
        print("-" * 100)
        for idx in range(min(10, len(test_df))):
            true_val = true_birads[idx]
            pred_val = predicted_birads[idx]
            status = "✓" if true_val == pred_val else "✗"
            text_preview = test_df.iloc[idx]['text'][:80] + "..."
            print(f"{status} True: {true_val} | Pred: {pred_val} | {text_preview}")
        
        # Save results
        results_df = test_df.copy()
        results_df['predicted_birads'] = predicted_birads
        results_df['correct'] = results_df[TARGET_COLUMN] == results_df['predicted_birads']
        
        output_file = "evaluation_results.csv"
        results_df.to_csv(output_file, index=False)
        print(f"\n💾 Full results saved to: {output_file}")
        
        # Summary
        correct = results_df['correct'].sum()
        total = len(results_df)
        print(f"\n✅ Correct predictions: {correct}/{total} ({correct/total*100:.2f}%)")
        print(f"❌ Incorrect predictions: {total-correct}/{total} ({(total-correct)/total*100:.2f}%)")
        
        print("\n" + "="*60)
        print("Evaluation Complete!")
        print("="*60)

if __name__ == "__main__":
    try:
        evaluate_model()
    except KeyboardInterrupt:
        print("\n\nEvaluation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
