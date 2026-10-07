# Multilingual Emergency & Safety Assistant 🚨
### AI-Powered Emergency Understanding for English, Tamil & Tanglish

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg)](https://tailwindcss.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)

---

## 1. Problem Statement
During critical emergency situations, distressed citizens often communicate in different natural languages, vernacular terms, or code-mixed dialects:
- **English**: *"There is a serious accident near my school, someone is bleeding."*
- **Tamil (தமிழ்)**: *"எங்கள் வீட்டில் தீப்பிடித்துவிட்டது, உடனடியாக உதவி தேவை."*
- **Tanglish (Tamil transliterated in Latin script)**: *"Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured."*

Traditional emergency intake systems and dispatch centers struggle with non-standard linguistic input and code-mixed scripts. Translating text via commercial APIs before classification frequently distorts crucial context, introduces latency, and drops localized geographical cues. 

This project provides an end-to-end, native AI assistant that directly classifies emergency messages in **English, Tamil, and Tanglish** without intermediate translation, evaluates urgency, extracts vital incident parameters (location, casualty count, keywords), and synthesizes safe, structured incident reports.

---

## 2. Objectives
1. **Direct Multi-dialect Understanding**: Native text processing for English, Tamil Unicode, and Tanglish without prior translation.
2. **Three-Tier ML Classification**:
   - **Language Identification**: English vs. Tamil vs. Tanglish.
   - **Emergency Categorization**: Medical, Accident, Fire, Police / Crime, Personal Safety, Natural Disaster.
   - **Urgency Assessment**: High vs. Medium urgency.
3. **Lightweight Entity Extraction**: Deterministic rule-based extraction for location landmarks, injured counts, and disaster trigger keywords without hallucination.
4. **Deterministic Safe Response Generation**: Safe, actionable instructions directing victims to emergency hotlines (112, 108, 100, 101) while strictly avoiding false claims of automatic dispatch.
5. **Modern Interactive Dashboard**: Professional web interface designed for college project vivas, academic demonstrations, and emergency desk simulation.

---

## 3. Key Features
- **Zero Retranslation Latency**: Analyzes native scripts and transliterated strings directly using sub-word n-gram character TF-IDF representations.
- **Academic Rigor & Transparency**: Distinguishes between **Offline Model Evaluation Accuracy** (held-out test set) and **Individual Prediction Confidence** (per-inference softmax probability).
- **Incident Entity Extraction**:
  - Automatically identifies landmark locations (e.g., *"near Thoothukudi bus stand"* $\rightarrow$ `Thoothukudi bus stand`).
  - Detects casualties and injury counts without hallucinating absent data.
- **Safety-First Architecture**: Strictly adheres to emergency prototype ethics by including disclaimers and emergency hotline quick-dials.
- **Local Incident History**: Keeps a session log of analyzed emergencies stored client-side in browser storage.
- **Unified Single-Server Deployment**: FastAPI backend serves both the REST API and the compiled React production bundle on port 8000.

---

## 4. System Architecture

```text
+-------------------------------------------------------------+
|                     USER EMERGENCY MESSAGE                  |
|  (English / Tamil / Tanglish - e.g., "Road la accident...") |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                      TEXT PREPROCESSING                     |
|  - Unicode NFC Normalization (Preserves Tamil U+0B80-0BFF)   |
|  - Whitespace Cleaning & Lowercasing                        |
+-------------------------------------------------------------+
                               |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
+---------------+      +---------------+      +---------------+
|    MODEL 1    |      |    MODEL 2    |      |    MODEL 3    |
|   Language    |      |   Emergency   |      |    Urgency    |
|   Detector    |      |  Classifier   |      |   Detector    |
|  (100% Acc)   |      |  (81.94% Acc) |      |  (87.50% Acc) |
+---------------+      +---------------+      +---------------+
        |                      |                      |
        +----------------------+----------------------+
                               |
                               v
+-------------------------------------------------------------+
|                    INFORMATION EXTRACTION                   |
|  - Location Landmark Detection                              |
|  - Injury / Casualty Count Detection                        |
|  - Emergency Keyword Triggers                               |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  SAFE RESPONSE GENERATION                   |
|  - Deterministic action guidance based on (Type, Urgency)   |
|  - Emergency Hotline Directory (112, 108, 100, 101, 1091)   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  STRUCTURED INCIDENT REPORT                 |
|            Rendered in Modern React/Tailwind UI             |
+-------------------------------------------------------------+
```

---

## 5. Dataset Overview
- **File**: `dataset/emergency_dataset.xlsx`
- **Total Records**: 360 balanced records
- **Languages (120 per class)**:
  - English: 120
  - Tamil: 120
  - Tanglish: 120
- **Emergency Categories**:
  - Medical (78 records)
  - Accident (72 records)
  - Fire (72 records)
  - Police / Crime (66 records)
  - Personal Safety (36 records)
  - Natural Disaster (36 records)
- **Urgency Distribution**:
  - High (300 records)
  - Medium (60 records)

---

## 6. Machine Learning Algorithms

### Model 1: Language Detector
- **Input**: Cleaned Text
- **Vectorization**: Character n-grams (`analyzer="char_wb"`, `ngram_range=(2, 5)`)
- **Classifier**: Logistic Regression (`max_iter=1000`)
- **Target**: `Language` (`English`, `Tamil`, `Tanglish`)
- **Model File**: `model/language_detector.pkl`

### Model 2: Emergency Classifier
- **Input**: Cleaned Text
- **Vectorization**: Character n-grams (`analyzer="char_wb"`, `ngram_range=(2, 5)`, `sublinear_tf=True`)
- **Classifier**: Logistic Regression (`class_weight="balanced"`, `max_iter=1000`)
- **Target**: `Emergency_Type` (6 classes)
- **Model File**: `model/emergency_classifier.pkl`

### Model 3: Urgency Detector
- **Input**: Cleaned Text
- **Vectorization**: Character n-grams (`analyzer="char_wb"`, `ngram_range=(2, 5)`, `sublinear_tf=True`)
- **Classifier**: Logistic Regression (`class_weight="balanced"`, `max_iter=1000`)
- **Target**: `Urgency` (`High`, `Medium`)
- **Model File**: `model/urgency_detector.pkl`

---

## 7. Model Performance & Evaluation

Models were evaluated on a **stratified 20% held-out test set (72 unseen samples)**:

| Model | Evaluation Accuracy | Test Samples | Baseline Achieved |
| :--- | :---: | :---: | :---: |
| **Language Detector** | **100.00%** | 72 | 100% |
| **Emergency Classifier** | **81.94%** | 72 | ~81.94% |
| **Urgency Detector** | **87.50%** | 72 | 87.50% |

### Emergency Classifier Detailed Metrics
```text
                   precision    recall  f1-score   support

        Accident       0.85      0.79      0.81        14
            Fire       1.00      0.93      0.97        15
         Medical       0.78      0.88      0.82        16
Natural Disaster       0.83      0.71      0.77         7
 Personal Safety       0.57      0.57      0.57         7
  Police / Crime       0.79      0.85      0.81        13

        accuracy                           0.82        72
       macro avg       0.80      0.79      0.79        72
    weighted avg       0.82      0.82      0.82        72
```

---

## 8. Project Structure

```text
Multilingual-Emergency-Safety-Assistant/
├── dataset/
│   └── emergency_dataset.xlsx          # 360-record dataset
├── model/
│   ├── language_detector.pkl           # Trained Model 1
│   ├── emergency_classifier.pkl        # Trained Model 2
│   ├── urgency_detector.pkl            # Trained Model 3
│   └── model_metrics.json              # Offline evaluation report
├── training/
│   ├── language_model.py               # Language training script
│   ├── train_model.py                  # Emergency training script
│   ├── urgency_model.py                # Urgency training script
│   └── evaluate_models.py              # Master evaluation pipeline
├── app/
│   ├── __init__.py
│   ├── preprocessing.py                # Unicode & whitespace cleaner
│   ├── extraction.py                   # Rule-based information extraction
│   ├── response_generator.py           # Safe response templates
│   ├── assistant.py                    # Core inference engine (loads PKL once)
│   └── server.py                       # FastAPI API & static server
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── EmergencyInput.jsx
│   │   │   ├── AnalysisResults.jsx
│   │   │   ├── HistoryLog.jsx
│   │   │   └── MetricsModal.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── requirements.txt                    # Python dependencies
├── test_assistant.py                   # Automated test suite (all pass)
└── README.md                           # Documentation
```

---

## 9. Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js v18+ (for frontend development/builds)

### Step 1: Clone or Navigate to Directory
```bash
cd "c:/Users/Manasa C/OneDrive/Desktop/Multilingual-Emergency-Safety-Assistant"
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: (Optional) Build Frontend Assets
The frontend is already pre-compiled into `frontend/dist`. To rebuild:
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## 10. How to Train Models
The training scripts run separately from the inference engine and save persistent `.pkl` files:

```bash
# Train all models and produce model/model_metrics.json
python training/evaluate_models.py
```

Individual training scripts:
```bash
python training/language_model.py
python training/train_model.py
python training/urgency_model.py
```

---

## 11. How to Run the Application

### Option A: Run Full Web Application (Unified Server)
Start the FastAPI server which serves both the REST API and the React web dashboard:
```bash
python -m app.server
```
Then open your web browser at:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### Option B: Run Automated Tests
```bash
python test_assistant.py
```

### Option C: Run CLI Inference
```bash
python app/assistant.py
```

---

## 12. Sample Test Cases & Outputs

| Language | Input Message | Detected Language | Emergency Type | Urgency | Extracted Info |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **English** | `"I need an ambulance immediately, 1 person unconscious near City Hospital"` | English | Medical | HIGH | Location: `City Hospital`, Injured: `1` |
| **Tamil** | `"எங்கள் வீட்டில் தீப்பிடித்துவிட்டது"` | Tamil | Fire | HIGH | Location: `Not detected`, Injured: `Not detected` |
| **Tanglish** | `"Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured"` | Tanglish | Accident | HIGH | Location: `Thoothukudi bus stand`, Injured: `2` |
| **Tanglish** | `"Yaaro enna follow panranga"` | Tanglish | Police / Crime | HIGH | Location: `Not detected`, Injured: `Not detected` |
| **Tamil** | `"எங்கள் பகுதியில் வெள்ளம் ஏற்பட்டுள்ளது, 5 பேர் சிக்கியுள்ளனர்"` | Tamil | Natural Disaster | HIGH | Affected: `5`, Location: `Not detected` |

---

## 13. Safety & Ethical Disclaimers
1. **Assistance Prototype Only**: This system does not automatically dispatch police, ambulances, or firefighters.
2. **Explicit Advice**: Users in distress are instructed to dial emergency helplines directly (`112` for National Emergency, `108` for Ambulance, `100` for Police, `101` for Fire).
3. **No False Guarantees**: Outputs clearly communicate prediction confidence levels and indicate missing information rather than hallucinating facts.

---

## 14. Viva & College Project Presentation Tips
- **Why TF-IDF with character-level n-grams (`char_wb`)?**
  Character n-grams are immune to colloquial spelling variations common in Tanglish (e.g., *"accident aaiduchu"* vs *"aayiduchu"* vs *"ayidichu"*) and handle complex agglutinative morphology in Tamil script without needing custom tokenizers.
- **Why Logistic Regression?**
  It provides fast, explainable, low-resource classification with well-calibrated posterior probabilities (`predict_proba`) suitable for real-time edge or server deployment.
- **Model Accuracy vs. Prediction Confidence**:
  Emphasize that 81.94% is the statistical test accuracy on 72 held-out samples, while 62.27% is the model's confidence for an individual input.

---

## 15. Limitations & Future Scope
- **Current Limitations**:
  - Small training corpus (360 samples).
  - Rule-based location extraction handles common prepositions and landmark nouns, but may miss complex colloquial clauses.
- **Future Enhancements**:
  - Voice-based input with automatic speech recognition (ASR) for spoken Tamil and Tanglish.
  - Integration with device GPS coordinates with user permission.
  - Multi-task transformer fine-tuning (e.g., IndicBERT, MuRIL) for deeper context.
  - Support for additional regional languages (Telugu, Malayalam, Kannada, Hindi).
  - Direct integration with Smart City CAD (Computer Aided Dispatch) systems via authenticated webhooks.
