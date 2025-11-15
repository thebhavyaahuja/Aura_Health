"""
Translation script for radiology reports from Spanish to English.
Uses Google Cloud Translation API with service account credentials.
"""

import pandas as pd
import time
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import sys

# --- Configuration ---
INPUT_FILE = "radiology_reports.csv"
OUTPUT_FILE = "radiology_reports_eng.csv"
CREDENTIALS_FILE = "aura-health-25-ea7441665e0c.json"
DELIMITER = ";"
SOURCE_LANGUAGE = "es"  # Spanish
TARGET_LANGUAGE = "en"  # English

# Columns that contain text to translate
TEXT_COLUMNS = [
    "Observations", "Conclusion", "Recommendations", "Reason"
]

# Batch size for translation (to avoid rate limits)
BATCH_SIZE = 100
SLEEP_TIME = 1  # seconds between batches


def setup_translation_client():
    """
    Initialize Google Cloud Translation client with service account credentials.
    """
    print(f"Setting up Google Cloud Translation client...")
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE
        )
        client = translate.Client(credentials=credentials)
        print("Translation client ready!")
        return client
    except Exception as e:
        print(f"Error setting up translation client: {e}")
        sys.exit(1)


def translate_text(client, text, source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE):
    """
    Translate a single text string from source to target language.
    Returns the translated text or the original text if translation fails.
    """
    if pd.isna(text) or text == "" or not isinstance(text, str):
        return text
    
    try:
        result = client.translate(
            text,
            source_language=source_lang,
            target_language=target_lang
        )
        return result['translatedText']
    except Exception as e:
        print(f"Translation error: {e}")
        print(f"Problematic text (first 100 chars): {str(text)[:100]}")
        return text  # Return original text if translation fails


def load_data():
    """
    Load the radiology reports CSV file.
    """
    print(f"\n--- Loading data from {INPUT_FILE} ---")
    try:
        df = pd.read_csv(INPUT_FILE, delimiter=DELIMITER, encoding='utf-8')
        print(f"Successfully loaded {len(df)} reports")
        print(f"Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)


def translate_dataframe(df, client):
    """
    Translate all text columns in the dataframe.
    """
    print(f"\n--- Starting Translation ---")
    print(f"Translating from {SOURCE_LANGUAGE} to {TARGET_LANGUAGE}")
    print(f"Text columns to translate: {TEXT_COLUMNS}")
    
    # Create a copy to avoid modifying original
    df_translated = df.copy()
    
    total_rows = len(df)
    
    for col in TEXT_COLUMNS:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in CSV. Skipping.")
            continue
            
        print(f"\n--- Translating column: {col} ---")
        translated_values = []
        
        for idx, text in enumerate(df[col]):
            # Progress indicator
            if idx % 10 == 0:
                print(f"Progress: {idx}/{total_rows} rows ({(idx/total_rows)*100:.1f}%)", end='\r')
            
            translated_text = translate_text(client, text)
            translated_values.append(translated_text)
            
            # Rate limiting: sleep every BATCH_SIZE translations
            if (idx + 1) % BATCH_SIZE == 0:
                print(f"\nProcessed {idx + 1} rows. Sleeping for {SLEEP_TIME}s to avoid rate limits...")
                time.sleep(SLEEP_TIME)
        
        df_translated[col] = translated_values
        print(f"\nCompleted translating column: {col}")
    
    return df_translated


def save_translated_data(df):
    """
    Save the translated dataframe to a new CSV file.
    """
    print(f"\n--- Saving translated data to {OUTPUT_FILE} ---")
    try:
        df.to_csv(OUTPUT_FILE, sep=DELIMITER, index=False, encoding='utf-8')
        print(f"Successfully saved {len(df)} translated reports to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving CSV: {e}")
        sys.exit(1)


def main():
    """
    Main execution flow.
    """
    print("=" * 60)
    print("RADIOLOGY REPORTS TRANSLATION SCRIPT")
    print("Spanish to English Translation using Google Cloud API")
    print("=" * 60)
    
    # Step 1: Setup translation client
    client = setup_translation_client()
    
    # Step 2: Load data
    df = load_data()
    
    # Step 3: Translate
    df_translated = translate_dataframe(df, client)
    
    # Step 4: Save results
    save_translated_data(df_translated)
    
    print("\n" + "=" * 60)
    print("TRANSLATION COMPLETE!")
    print("=" * 60)
    
    # Show a sample comparison
    print("\n--- Sample Translation (First Row) ---")
    sample_col = "Reason" if "Reason" in df.columns else TEXT_COLUMNS[0]
    if sample_col in df.columns:
        print(f"\nOriginal ({sample_col}):")
        print(df[sample_col].iloc[0] if pd.notna(df[sample_col].iloc[0]) else "N/A")
        print(f"\nTranslated ({sample_col}):")
        print(df_translated[sample_col].iloc[0] if pd.notna(df_translated[sample_col].iloc[0]) else "N/A")


if __name__ == "__main__":
    main()
