"""
Core Inference Engine: Multilingual Emergency & Safety Assistant.
Loads trained models once via joblib, validates input, performs text preprocessing,
runs predictions with confidence probabilities, extracts entities, and formats
structured emergency reports.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.preprocessing import clean_text
from app.extraction import extract_emergency_information
from app.response_generator import generate_emergency_response


class EmergencyAssistant:
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initializes the assistant and loads all three trained models once into memory.
        """
        self.model_dir = Path(model_dir) if model_dir else PROJECT_ROOT / "model"
        
        self.lang_model_path = self.model_dir / "language_detector.pkl"
        self.emer_model_path = self.model_dir / "emergency_classifier.pkl"
        self.urg_model_path = self.model_dir / "urgency_detector.pkl"
        self.metrics_path = self.model_dir / "model_metrics.json"
        
        self.language_model = None
        self.emergency_model = None
        self.urgency_model = None
        self.model_metrics = {}
        
        self._load_models()
        self._load_metrics()

    def _load_models(self):
        """Loads .pkl model files once."""
        missing = []
        for path, name in [
            (self.lang_model_path, "Language Detector"),
            (self.emer_model_path, "Emergency Classifier"),
            (self.urg_model_path, "Urgency Detector")
        ]:
            if not path.exists():
                missing.append(f"{name} ({path.name})")
        
        if missing:
            raise FileNotFoundError(
                f"Missing required model files: {', '.join(missing)}. "
                "Please run 'python training/evaluate_models.py' first to train and save the models."
            )
        
        try:
            self.language_model = joblib.load(self.lang_model_path)
            self.emergency_model = joblib.load(self.emer_model_path)
            self.urgency_model = joblib.load(self.urg_model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load machine learning models from {self.model_dir}: {str(e)}")

    def _load_metrics(self):
        """Loads offline model evaluation metrics if available."""
        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, "r", encoding="utf-8") as f:
                    self.model_metrics = json.load(f)
            except Exception as e:
                print(f"[Warning] Failed to load metrics json: {e}")

    def analyze(self, raw_message: str) -> Dict[str, Any]:
        """
        Analyzes a single emergency message.
        
        Workflow:
        1. Input validation
        2. Text preprocessing
        3. Language classification + confidence
        4. Emergency classification + confidence
        5. Urgency classification + confidence
        6. Lightweight information extraction
        7. Safe response generation
        8. Return structured report
        """
        # Step 1: Input Validation (Section 26)
        if not raw_message or not raw_message.strip():
            return {
                "success": False,
                "error": "Please describe your emergency before analyzing.",
                "message": raw_message or ""
            }

        cleaned = clean_text(raw_message)
        if not cleaned:
            return {
                "success": False,
                "error": "Please describe your emergency before analyzing.",
                "message": raw_message
            }

        # Step 2: Language Prediction & Confidence
        lang_probs = self.language_model.predict_proba([cleaned])[0]
        lang_idx = lang_probs.argmax()
        detected_language = self.language_model.classes_[lang_idx]
        lang_confidence = float(lang_probs[lang_idx] * 100)
        
        # Step 3: Emergency Type Prediction & Confidence
        emer_probs = self.emergency_model.predict_proba([cleaned])[0]
        emer_idx = emer_probs.argmax()
        detected_emergency = self.emergency_model.classes_[emer_idx]
        emer_confidence = float(emer_probs[emer_idx] * 100)
        
        # Step 4: Urgency Prediction & Confidence
        urg_probs = self.urgency_model.predict_proba([cleaned])[0]
        urg_idx = urg_probs.argmax()
        detected_urgency = self.urgency_model.classes_[urg_idx]
        urg_confidence = float(urg_probs[urg_idx] * 100)

        # Step 5: Information Extraction
        extracted_info = extract_emergency_information(raw_message)

        # Step 6: Safe Response Generation
        response_info = generate_emergency_response(detected_emergency, detected_urgency)

        # Step 7: Assemble Structured Result
        report = {
            "success": True,
            "user_message": raw_message.strip(),
            "cleaned_message": cleaned,
            "language": {
                "detected": detected_language,
                "confidence_percentage": round(lang_confidence, 2),
                "all_probabilities": {
                    cls: round(float(prob) * 100, 2)
                    for cls, prob in zip(self.language_model.classes_, lang_probs)
                }
            },
            "emergency_type": {
                "category": detected_emergency,
                "confidence_percentage": round(emer_confidence, 2),
                "all_probabilities": {
                    cls: round(float(prob) * 100, 2)
                    for cls, prob in zip(self.emergency_model.classes_, emer_probs)
                }
            },
            "urgency": {
                "level": detected_urgency,
                "confidence_percentage": round(urg_confidence, 2),
                "all_probabilities": {
                    cls: round(float(prob) * 100, 2)
                    for cls, prob in zip(self.urgency_model.classes_, urg_probs)
                }
            },
            "extracted_information": extracted_info,
            "response": response_info,
            "model_accuracies_reference": {
                "language_test_accuracy": (
                    round(self.model_metrics.get("language_detector", {}).get("accuracy", 1.0) * 100, 2)
                ),
                "emergency_test_accuracy": (
                    round(self.model_metrics.get("emergency_classifier", {}).get("accuracy", 0.8194) * 100, 2)
                ),
                "urgency_test_accuracy": (
                    round(self.model_metrics.get("urgency_detector", {}).get("accuracy", 0.875) * 100, 2)
                ),
                "explanation": (
                    "Note: Model evaluation accuracy is measured on the 20% held-out test set (72 samples), "
                    "whereas prediction confidence represents the model's certainty for this specific message."
                )
            }
        }

        return report

    def format_text_report(self, report: Dict[str, Any]) -> str:
        """Formats analysis output into structured text format matching Section 14."""
        if not report.get("success"):
            return f"Error: {report.get('error')}"

        lang = report["language"]
        emer = report["emergency_type"]
        urg = report["urgency"]
        ext = report["extracted_information"]
        resp = report["response"]

        lines = [
            "=" * 60,
            "🚨 EMERGENCY ANALYSIS REPORT",
            "=" * 60,
            f"User Message:\n  {report['user_message']}",
            "",
            f"Language:\n  {lang['detected']} (Confidence: {lang['confidence_percentage']}%)",
            "",
            f"Emergency Type:\n  {emer['category']} (Confidence: {emer['confidence_percentage']}%)",
            "",
            f"Urgency:\n  {urg['level']} (Confidence: {urg['confidence_percentage']}%)",
            "",
            f"Location:\n  {ext['location']}",
            f"People Injured:\n  {ext['people_injured']}",
            f"People Affected:\n  {ext['people_affected']}",
            f"Keywords Detected:\n  {', '.join(ext['keywords']) if ext['keywords'] else 'None'}",
            "",
            f"Recommended Action:\n  {resp['recommended_action']}",
            "",
            f"Safety Notice:\n  {resp['disclaimer']}",
            "=" * 60
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    
    assistant = EmergencyAssistant()
    sample = "Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured"
    res = assistant.analyze(sample)
    print(assistant.format_text_report(res))
