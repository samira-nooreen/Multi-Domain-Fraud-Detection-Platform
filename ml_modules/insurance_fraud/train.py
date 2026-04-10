"""
Insurance Claim Fraud - Autoencoder Training Pipeline
Algorithm: Autoencoder (Anomaly Detection)
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt

def train_models():
    # Get script directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'insurance_data.csv')
    
    # 1. Load Data
    if not os.path.exists(data_path):
        print("Generating data...")
        import sys
        sys.path.append(base_dir)
        from generate_data import generate_insurance_data
        df = generate_insurance_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
        
    print(f"Loaded {len(df)} records.")

    # 2. Preprocessing
    features = [
        'age', 'policy_tenure', 'policy_amount', 'claim_amount', 'claim_ratio',
        'past_claims', 'incident_hour', 'days_to_report', 'witness_present',
        'police_report', 'linked_claims'
    ]
    
    # Ensure columns exist
    for col in features:
        if col not in df.columns:
            df[col] = 0
            
    X = df[features]
    y = df['is_fraud']
    
    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train XGBoost Classifier
    print("\nTraining XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
    
    # 5. Save Models
    joblib.dump(model, os.path.join(base_dir, 'insurance_model.pkl'))
    joblib.dump(scaler, os.path.join(base_dir, 'insurance_scaler.pkl'))
    
    print("Models saved successfully as 'insurance_model.pkl' and 'insurance_scaler.pkl'")

if __name__ == "__main__":
    train_models()
