import pandas as pd
import numpy as np
import torch
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    BioGptForSequenceClassification,
    Trainer,
    TrainingArguments,
    logging as hf_logging,
)

# --- GPU and CUDA Optimizations ---
# Set CUDA environment variables for optimal performance
os.environ['CUDA_LAUNCH_BLOCKING'] = '0'  # Async execution for better performance
os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'  # L40S compute capability
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True,max_split_size_mb:512'

# Enable TF32 for faster operations on Ampere+ GPUs (L40S is Ada Lovelace)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
torch.backends.cudnn.benchmark = True  # Auto-tune kernels for better performance

# Check GPU availability
if torch.cuda.is_available():
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
else:
    print("WARNING: CUDA is not available. Training will be slow on CPU.")


# --- Configuration ---
FILE_NAME = "radiology_reports_eng.csv"
DELIMITER = ";"

# --- Feature Configuration ---
TEXT_COLUMNS = ["Observations", "Conclusion", "Recommendations", "Reason"]

# New: Tabular columns to serialize into text
TABULAR_COLUMNS = [
    # "Medical_Unit",
    "Hormonal_Therapy",
    "Family_History",
    "Age",
    "Children"
]
# We are intentionally omitting:
# - ID_R, Year, Month, LMP (per your instruction)
# - Full_Report (as we are combining the specific report sections)

TARGET_COLUMN = "BI-RADS" # The column we want to predict
MODEL_NAME = "microsoft/biogpt"
TEST_SIZE = 0.2  # 20% of data for testing
RANDOM_STATE = 42 # For reproducible results
OUTPUT_DIR = "./biogpt_birads_classifier"
HUGGINGFACE_REPO = "ishro/biogpt-aura"  # HuggingFace repository to push model to

# Set verbosity to 'info' to see progress bars (like tqdm)
hf_logging.set_verbosity_info()

def print_gpu_memory():
    """Print current GPU memory usage for all available GPUs."""
    if torch.cuda.is_available():
        print("\n--- GPU Memory Usage ---")
        for i in range(torch.cuda.device_count()):
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            reserved = torch.cuda.memory_reserved(i) / 1024**3
            total = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"GPU {i} ({torch.cuda.get_device_name(i)}):")
            print(f"  Allocated: {allocated:.2f} GB / {total:.2f} GB ({allocated/total*100:.1f}%)")
            print(f"  Reserved:  {reserved:.2f} GB / {total:.2f} GB ({reserved/total*100:.1f}%)")
        print()

def load_and_preprocess_data():
    """
    Loads the CSV, combines text and tabular fields, and maps labels.
    """
    print(f"--- Step 1: Loading Data from {FILE_NAME} ---")
    try:
        df = pd.read_csv(FILE_NAME, delimiter=DELIMITER)
    except FileNotFoundError:
        print(f"Error: File '{FILE_NAME}' not found.")
        print("Please make sure the file is in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        print("Please check the file format and delimiter.")
        sys.exit(1)

    print(f"Loaded {len(df)} reports.")

    # --- Text & Feature Preprocessing ---
    print("Preprocessing text and serializing tabular features...")
    
    # Fill any missing text fields with an empty string
    for col in TEXT_COLUMNS:
        df[col] = df[col].fillna("")
        
    # Fill missing tabular data with "Unknown"
    # We convert all to string to handle mixed types gracefully
    for col in TABULAR_COLUMNS:
        df[col] = df[col].fillna("Unknown").astype(str)

    # --- Create the combined 'text' field ---
    
    # 1. Create the main report text
    df['report_text'] = df[TEXT_COLUMNS].apply(
        lambda x: ' '.join(x.astype(str)), axis=1
    )
    
    # 2. Create the serialized metadata string
    # This creates a string like:
    # "Medical Unit: X. Hormonal Therapy: Y. Family History: Z. Age: A. Children: B."
    def create_metadata_string(row):
        parts = []
        parts.append(f"Medical Unit: {row['Medical_Unit']}")
        parts.append(f"Hormonal Therapy: {row['Hormonal_Therapy']}")
        parts.append(f"Family History: {row['Family_History']}")
        parts.append(f"Age: {row['Age']}")
        parts.append(f"Children: {row['Children']}")
        return ". ".join(parts) + "."

    df['metadata_text'] = df.apply(create_metadata_string, axis=1)

    # 3. Combine metadata and report text with a separator
    # The [REPORT] token helps the model distinguish metadata from the report
    df['text'] = df['metadata_text'] + " [REPORT] " + df['report_text']
    
    print("Example of combined text input:")
    print(df['text'].iloc[0])

    # --- Label Preprocessing ---
    # Drop rows where the target label is missing
    df = df.dropna(subset=[TARGET_COLUMN])
    
    # Get all unique BI-RADS values (e.g., 0, 1, 2, 4, 5, 6)
    # This automatically handles if a category like '3' is missing
    unique_labels = sorted(df[TARGET_COLUMN].unique())
    
    # FIX: Convert numpy.int64 to standard python int for JSON serialization
    unique_labels = [int(label) for label in unique_labels]
    
    # Create the label mappings required by the model
    # Model needs labels to be 0, 1, 2, 3... (SEQUENTIAL, not the original values)
    label2id = {label: i for i, label in enumerate(unique_labels)}
    id2label = {i: label for label, i in label2id.items()}
    num_labels = len(unique_labels)
    
    print(f"Found {num_labels} unique BI-RADS labels: {unique_labels}")
    print(f"Mapped labels to integers: {label2id}")
    print(f"Example: BI-RADS {unique_labels[0]} -> model label {label2id[unique_labels[0]]}")
    
    # Create the final 'label' column with integer IDs (0 to num_labels-1)
    df['label'] = df[TARGET_COLUMN].map(label2id)
    
    # CRITICAL: Verify all labels are valid
    assert df['label'].min() >= 0, f"Label minimum is {df['label'].min()}, should be >= 0"
    assert df['label'].max() < num_labels, f"Label maximum is {df['label'].max()}, should be < {num_labels}"
    print(f"✓ Label validation passed: min={df['label'].min()}, max={df['label'].max()}, num_labels={num_labels}")
    
    # Keep only the columns we need
    # We also keep TARGET_COLUMN for the final evaluation comparison
    final_df = df[['text', 'label', TARGET_COLUMN]]
    
    return final_df, label2id, id2label, num_labels

def tokenize_data(train_df, test_df):
    """
    Loads tokenizer and tokenizes the datasets.
    """
    print(f"--- Step 2: Loading Tokenizer ({MODEL_NAME}) ---")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # Handle BioGPT's lack of a pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    def tokenize_function(examples):
        # Truncate to the model's max input size
        # The new metadata text will take up some of the 512 tokens
        tokenized = tokenizer(
            examples['text'], 
            padding="max_length", 
            truncation=True, 
            max_length=512
        )
        # Add sequence length for efficient batching
        tokenized['length'] = [
            sum(1 for token_id in input_ids if token_id != tokenizer.pad_token_id)
            for input_ids in tokenized['input_ids']
        ]
        return tokenized

    print("Tokenizing datasets...")
    # Convert pandas DataFrames to Hugging Face Dataset objects
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    
    # Apply tokenization
    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    
    # Remove original columns to prepare for the model
    # Check for '__index_level_0__' which is sometimes added by from_pandas
    train_remove_cols = [TARGET_COLUMN, 'text']
    if '__index_level_0__' in tokenized_train.column_names:
        train_remove_cols.append('__index_level_0__')
        
    test_remove_cols = [TARGET_COLUMN, 'text']
    if '__index_level_0__' in tokenized_test.column_names:
        test_remove_cols.append('__index_level_0__')

    tokenized_train = tokenized_train.remove_columns(train_remove_cols)
    tokenized_test = tokenized_test.remove_columns(test_remove_cols)
    
    # Set format for PyTorch
    tokenized_train.set_format("torch")
    tokenized_test.set_format("torch")

    print(f"✓ Tokenization complete")
    print(f"  - Train samples: {len(tokenized_train)}")
    print(f"  - Test samples: {len(tokenized_test)}")

    return tokenized_train, tokenized_test, tokenizer

def compute_metrics(p):
    """
    Calculates accuracy and F1-score for evaluation.
    """
    preds = np.argmax(p.predictions, axis=1)
    labels = p.label_ids
    
    accuracy = accuracy_score(labels, preds)
    # Use 'macro' average for F1-score to treat all classes equally
    f1 = f1_score(labels, preds, average="macro")
    
    return {
        "accuracy": accuracy,
        "f1_macro": f1,
    }

def train_model(
    tokenized_train, 
    tokenized_test, 
    tokenizer, 
    num_labels, 
    id2label, 
    label2id
):
    """
    Loads the model and runs the training with multi-GPU optimization.
    """
    print(f"--- Step 3: Loading Model ({MODEL_NAME}) ---")
    
    # Load the model for sequence classification
    model = BioGptForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id,
        pad_token_id=tokenizer.eos_token_id, # Set pad token
        problem_type="single_label_classification",  # Explicitly set problem type
        ignore_mismatched_sizes=True  # Allow size mismatches for classification head
    )
    
    # Ensure pad_token_id is properly set in config
    model.config.pad_token_id = tokenizer.eos_token_id
    
    # Enable gradient checkpointing to save memory
    model.gradient_checkpointing_enable()
    print("✓ Gradient checkpointing enabled")
    
    # Define Training Arguments with multi-GPU optimizations
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,           # 3 epochs is a good start
        learning_rate=2e-5,           # Standard learning rate for fine-tuning
        
        # --- Multi-GPU Configuration ---
        per_device_train_batch_size=4,   # Further reduced to avoid OOM
        per_device_eval_batch_size=4,    # Reduced to match training batch size
        gradient_accumulation_steps=8,   # Increased to maintain effective batch size = 4 * 8 * 2 GPUs = 64
        
        # --- Mixed Precision Training ---
        fp16=False,                      # Disable FP16
        bf16=True,                       # Use BF16 for better stability on L40S
        bf16_full_eval=True,             # Use BF16 for evaluation too
        
        # --- Memory Optimizations ---
        gradient_checkpointing=True,     # Recompute activations to save memory
        optim="adamw_torch_fused",       # Fused optimizer for faster training
        
        # --- DataLoader Settings ---
        dataloader_num_workers=4,        # Parallel data loading
        dataloader_pin_memory=True,      # Faster data transfer to GPU
        dataloader_prefetch_factor=2,    # Prefetch batches
        
        # --- Evaluation & Saving ---
        weight_decay=0.01,
        eval_strategy="no",              # DISABLE eval during training to save memory
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=10,
        logging_first_step=True,
        load_best_model_at_end=False,    # Can't load best model without eval
        save_total_limit=1,              # Keep only 1 checkpoint to save memory
        eval_accumulation_steps=1,       # Process eval in smaller chunks to avoid OOM
        eval_do_concat_batches=False,    # Don't concatenate eval batches in memory
        
        # --- Performance Settings ---
        ddp_find_unused_parameters=False, # Faster DDP
        ddp_backend="nccl",               # Use NCCL for multi-GPU
        local_rank=-1,                    # Let Trainer handle device placement
        group_by_length=False,            # Disable to avoid index issues with variable lengths
        remove_unused_columns=True,       # Remove non-model columns
        dataloader_drop_last=True,        # Drop incomplete batches to avoid size mismatches
        
        # --- HuggingFace Hub ---
        push_to_hub=True,
        
        # --- Reporting ---
        report_to=["tensorboard"],        # Enable tensorboard logging
        disable_tqdm=False,               # Keep progress bars
    )
    
    print(f"✓ Training configuration:")
    print(f"  - Number of GPUs: {torch.cuda.device_count()}")
    print(f"  - Per device batch size: {training_args.per_device_train_batch_size}")
    print(f"  - Gradient accumulation steps: {training_args.gradient_accumulation_steps}")
    print(f"  - Effective batch size: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps * torch.cuda.device_count()}")
    print(f"  - Mixed precision: BF16")
    print(f"  - Optimizer: {training_args.optim}")
    
    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    print("--- Step 4: Starting Model Training ---")
    print("This may take a while depending on your data size and GPU...")
    
    # Clear CUDA cache before training
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("✓ CUDA cache cleared before training")
        print_gpu_memory()
        
    trainer.train()
    
    # Clear cache after training
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("✓ CUDA cache cleared after training")
    
    print("--- Training Complete ---")
    
    # Save the final best model locally
    trainer.save_model(f"{OUTPUT_DIR}/best_model")
    print(f"Best model saved to {OUTPUT_DIR}/best_model")
    
    return trainer

def evaluate_and_predict(trainer, test_df, tokenized_test, id2label):
    """
    Evaluates the model and shows example predictions.
    """
    print("--- Step 5: Evaluating Model on Test Set ---")
    
    # Clear cache before evaluation
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("✓ CUDA cache cleared before evaluation")
    
    # Get final metrics from the test set
    eval_results = trainer.evaluate()
    print("\n--- Final Test Set Metrics ---")
    for key, value in eval_results.items():
        print(f"{key}: {value:.4f}")
    
    # Clear cache after evaluation
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    # --- Show Predictions ---
    print("\n--- Example Predictions ---")
    
    # Get model outputs (logits) - this might use a lot of memory
    predictions = trainer.predict(tokenized_test)
    raw_scores = predictions.predictions
    
    # Get the predicted class ID (the one with the highest score)
    predicted_label_ids = np.argmax(raw_scores, axis=1)
    
    # Map IDs back to original BI-RADS labels
    predicted_labels = [id2label[label_id] for label_id in predicted_label_ids]
    
    # Clean up large arrays
    del raw_scores
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Add predictions to our original test DataFrame
    # Note: test_df was created with .copy(), so this is safe
    test_df['predicted_label_id'] = predicted_label_ids
    test_df['predicted_birads'] = predicted_labels
    
    # Display the first 10 predictions
    print("Showing first 10 test predictions:")
    print(test_df[['text', TARGET_COLUMN, 'predicted_birads']].head(10))

    # Show a full example
    print("\n--- Detailed First Prediction ---")
    print(f"Text: {test_df.iloc[0]['text'][:500]}...")
    print(f"Actual BI-RADS:   {test_df.iloc[0][TARGET_COLUMN]}")
    print(f"Predicted BI-RADS: {test_df.iloc[0]['predicted_birads']}")


def push_to_huggingface(trainer, tokenizer):
    """
    Push the trained model to HuggingFace Hub.
    You need to be logged in to HuggingFace CLI before running this.
    Run: huggingface-cli login
    """
    print("\n--- Step 6: Pushing Model to HuggingFace Hub ---")
    print(f"Repository: {HUGGINGFACE_REPO}")
    
    try:
        # Push the best model to HuggingFace
        print("Pushing model...")
        trainer.model.push_to_hub(HUGGINGFACE_REPO)
        
        print("Pushing tokenizer...")
        tokenizer.push_to_hub(HUGGINGFACE_REPO)
        
        # Also push all checkpoints (optional - contains training history)
        print("\nPushing all training checkpoints...")
        trainer.push_to_hub(HUGGINGFACE_REPO, commit_message="Upload all training checkpoints")
        
        print(f"\n✓ Successfully pushed model to: https://huggingface.co/{HUGGINGFACE_REPO}")
        print(f"✓ The model can now be loaded with: BioGptForSequenceClassification.from_pretrained('{HUGGINGFACE_REPO}')")
        
    except Exception as e:
        print(f"\n✗ Failed to push model to HuggingFace: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're logged in: huggingface-cli login")
        print("2. Check that the repository exists or you have permission to create it")
        print("3. Verify your internet connection")
        print("\nThe model is still saved locally at:", f"{OUTPUT_DIR}/best_model")
        raise


def main():
    # Print initial GPU status
    print_gpu_memory()
    
    # Step 1: Load and process data
    df, label2id, id2label, num_labels = load_and_preprocess_data()
    
    # Split into training and testing sets
    train_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df['label'] # Ensures class balance in splits
    )
    
    # Step 2: Tokenize
    tokenized_train, tokenized_test, tokenizer = tokenize_data(
        train_df.copy(), test_df.copy()
    )
    
    # Step 3 & 4: Train
    print_gpu_memory()
    trainer = train_model(
        tokenized_train, 
        tokenized_test, 
        tokenizer, 
        num_labels, 
        id2label, 
        label2id
    )
    
    # Print GPU usage after training
    print_gpu_memory()
    
    # Step 5: Evaluate and show predictions
    evaluate_and_predict(trainer, test_df.copy(), tokenized_test, id2label)
    
    # Step 6: Push to HuggingFace Hub
    print("\n" + "="*60)
    push_choice = input("Do you want to push the model to HuggingFace? (yes/no): ").strip().lower()
    if push_choice in ['yes', 'y']:
        push_to_huggingface(trainer, tokenizer)
    else:
        print("Skipping HuggingFace push. Model is saved locally at:", f"{OUTPUT_DIR}/best_model")
    
    # Final memory cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("\n✓ CUDA cache cleared")
        print_gpu_memory()


if __name__ == "__main__":
    main()