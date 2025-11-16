#!/usr/bin/env python3
"""
Check Risk Prediction Database
Shows current predictions in the database
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "predictions.db"

def format_timestamp(ts):
    """Format timestamp for display"""
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return ts
    return "N/A"

def check_database():
    """Check and display predictions"""
    if not DB_PATH.exists():
        print("❌ Database not found!")
        print(f"   Expected location: {DB_PATH}")
        return
    
    print("━" * 80)
    print("  🗃️  Risk Prediction Database Contents")
    print("━" * 80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total Predictions: {count}\n")
    
    if count == 0:
        print("No predictions found in database.")
        conn.close()
        return
    
    # Get all predictions
    cursor.execute("""
        SELECT 
            id, document_id, predicted_birads, confidence_score, 
            risk_level, status, created_at, processing_time
        FROM predictions
        ORDER BY created_at DESC
    """)
    
    predictions = cursor.fetchall()
    
    print(f"{'ID':<10} {'Document ID':<15} {'BI-RADS':<8} {'Conf':<6} {'Risk':<10} {'Status':<10} {'Created':<20} {'Time(s)':<8}")
    print("─" * 115)
    
    for pred in predictions:
        pred_id, doc_id, birads, conf, risk, status, created, proc_time = pred
        print(f"{pred_id[:8]:<10} {doc_id[:13]:<15} {birads:<8} {conf:<6.3f} {risk:<10} {status:<10} {format_timestamp(created):<20} {proc_time:<8.3f}")
    
    # Show detailed info for last prediction
    print("\n" + "━" * 80)
    print("  📋 Latest Prediction Details")
    print("━" * 80)
    
    cursor.execute("""
        SELECT 
            id, document_id, structuring_id, predicted_birads, 
            predicted_label_id, confidence_score, probabilities,
            risk_level, status, error_message, model_version,
            model_path, input_text, processing_time, created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    latest = cursor.fetchone()
    if latest:
        (pred_id, doc_id, struct_id, birads, label_id, conf, probs_json, 
         risk, status, error, model_ver, model_path, input_text, proc_time, created) = latest
        
        print(f"\nPrediction ID: {pred_id}")
        print(f"Document ID: {doc_id}")
        print(f"Structuring ID: {struct_id}")
        print(f"Predicted BI-RADS: {birads}")
        print(f"Label ID: {label_id}")
        print(f"Confidence: {conf:.3f}")
        print(f"Risk Level: {risk}")
        print(f"Status: {status}")
        
        if error:
            print(f"Error: {error}")
        
        print(f"Model: {model_ver}")
        print(f"Model Path: {model_path}")
        print(f"Processing Time: {proc_time:.3f}s")
        print(f"Created: {format_timestamp(created)}")
        
        if probs_json:
            print("\nProbabilities:")
            try:
                probs = json.loads(probs_json)
                for birads_score, prob in sorted(probs.items()):
                    bar_length = int(prob * 50)
                    bar = "█" * bar_length + "░" * (50 - bar_length)
                    print(f"  BI-RADS {birads_score}: {bar} {prob:.4f}")
            except:
                print(f"  {probs_json}")
        
        if input_text:
            print(f"\nInput Text Preview:")
            print(f"  {input_text[:200]}...")
    
    conn.close()
    print("\n" + "━" * 80)

if __name__ == "__main__":
    check_database()
