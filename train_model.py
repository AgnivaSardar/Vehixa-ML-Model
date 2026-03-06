"""
Training script - Run during Render deployment to generate engine_model.pkl
"""
from pathlib import Path

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sys


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "engine_data.csv"
MODEL_PATH = BASE_DIR / "engine_model.pkl"

def train_and_save_model():
    try:
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

        # Load data
        df = pd.read_csv(DATA_PATH)
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Prepare features and target
        X = df.drop('engine_condition', axis=1)
        y = df['engine_condition']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        model = RandomForestClassifier(
            class_weight='balanced', 
            random_state=42, 
            n_estimators=100
        )
        model.fit(X_train, y_train)
        
        # Save model
        joblib.dump(model, MODEL_PATH)
        print(f"✓ Model trained and saved as {MODEL_PATH}")
        return True
        
    except Exception as e:
        print(f"✗ Error training model: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = train_and_save_model()
    sys.exit(0 if success else 1)
