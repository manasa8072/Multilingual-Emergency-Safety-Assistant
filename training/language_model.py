"""
Model 1: Language Detection Model
Trains a character-level TF-IDF + Logistic Regression model to identify English, Tamil, and Tanglish.
Saves model to model/language_detector.pkl
"""

import os
import sys
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Ensure root directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from app.preprocessing import clean_text


def train_language_model(data_path="dataset/emergency_dataset.xlsx", model_dir="model"):
    data_file = PROJECT_ROOT / data_path
    save_dir = PROJECT_ROOT / model_dir
    os.makedirs(save_dir, exist_ok=True)
    
    if not data_file.exists():
        raise FileNotFoundError(f"Dataset not found at {data_file}")
    
    print(f"[Language Model] Loading dataset from {data_file}...")
    df = pd.read_excel(data_file)
    
    # Preprocessing
    df["Clean_Text"] = df["Text"].apply(clean_text)
    
    X = df["Clean_Text"]
    y = df["Language"]
    
    # Stratified train/test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Pipeline: char_wb TF-IDF (2,5) + Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5)
        )),
        ("classifier", LogisticRegression(
            random_state=42,
            max_iter=1000
        ))
    ])
    
    print("[Language Model] Training...")
    pipeline.fit(X_train, y_train)
    
    # Evaluation on held-out 20% test set
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[Language Model] Held-out Test Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    model_path = save_dir / "language_detector.pkl"
    joblib.dump(pipeline, model_path)
    print(f"[Language Model] Saved trained model to {model_path}")
    
    return pipeline, {
        "accuracy": float(acc),
        "classes": list(pipeline.classes_),
        "test_size": len(y_test),
        "train_size": len(y_train),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, output_dict=True)
    }


if __name__ == "__main__":
    train_language_model()
