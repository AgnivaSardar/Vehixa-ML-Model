# 🚗 Engine Health Model API

A FastAPI-based REST API that serves a trained Machine Learning model for engine failure prediction and diagnostic analysis.

This API predicts:

- Failure probability  
- Engine health status (GOOD / WARNING / CRITICAL)  
- Detailed diagnostic analysis  
- Top influential features  

---

## 🧠 Model Overview

- **Algorithm:** Random Forest Classifier  
- **Class Handling:** Balanced class weights  
- **Output:** Failure probability + health classification + diagnostics  

The model analyzes engine sensor parameters to determine mechanical risk.

---

## 📦 Project Structure
engine-api/
├── app.py
├── engine_model.pkl
├── requirements.txt
└── README.md
