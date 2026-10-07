"""
Master Model Evaluation & Training Pipeline
Trains all three models:
1. Language Detector
2. Emergency Classifier
3. Urgency Detector

Evaluates held-out test set performance, prints comprehensive reports,
and exports model/model_metrics.json for application transparency.
"""

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from training.language_model import train_language_model
from training.train_model import train_emergency_model
from training.urgency_model import train_urgency_model


def run_full_evaluation():
    print("=" * 70)
    print("MULTILINGUAL EMERGENCY & SAFETY ASSISTANT - MODEL TRAINING & EVALUATION")
    print("=" * 70)
    
    # 1. Language Model
    print("\n>>> [1/3] TRAINING & EVALUATING LANGUAGE DETECTION MODEL")
    _, lang_metrics = train_language_model()
    
    # 2. Emergency Model
    print("\n>>> [2/3] TRAINING & EVALUATING EMERGENCY CLASSIFIER")
    _, emer_metrics = train_emergency_model()
    
    # 3. Urgency Model
    print("\n>>> [3/3] TRAINING & EVALUATING URGENCY DETECTOR")
    _, urg_metrics = train_urgency_model()
    
    metrics_summary = {
        "language_detector": lang_metrics,
        "emergency_classifier": emer_metrics,
        "urgency_detector": urg_metrics,
        "metadata": {
            "dataset": "dataset/emergency_dataset.xlsx",
            "total_records": 360,
            "test_split_ratio": 0.20,
            "evaluation_note": "Model evaluation accuracy represents held-out test set performance across 72 test samples. It is strictly separate from runtime prediction confidence."
        }
    }
    
    out_file = PROJECT_ROOT / "model" / "model_metrics.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
    
    print("\n" + "=" * 70)
    print("MODEL EVALUATION SUMMARY (Held-out 20% Test Set):")
    print("=" * 70)
    print(f"1. Language Detector Accuracy:   {lang_metrics['accuracy'] * 100:.2f}%  (Baseline: 100%)")
    print(f"2. Emergency Classifier Accuracy: {emer_metrics['accuracy'] * 100:.2f}%  (Baseline: ~81.94%)")
    print(f"3. Urgency Detector Accuracy:    {urg_metrics['accuracy'] * 100:.2f}%  (Baseline: 87.50%)")
    print(f"\nSaved metrics summary to: {out_file}")
    print("=" * 70)


if __name__ == "__main__":
    run_full_evaluation()
