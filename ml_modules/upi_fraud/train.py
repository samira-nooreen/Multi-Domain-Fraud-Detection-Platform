"""
UPI Fraud Detection - Anomaly Detection Model Training
Trains an Isolation Forest model for detecting fraudulent UPI transactions.
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import os

def load_and_prepare_data(filepath='upi_fraud_data.csv'):
    """Load and prepare the dataset"""
    if not os.path.exists(filepath):
        from generate_data import generate_upi_data
        df = generate_upi_data(10000)
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)
    
    # Features
    feature_cols = [
        'amount', 'hour', 'day_of_week', 'transaction_frequency',
        'avg_transaction_amount', 'account_age_days', 'device_change',
        'location_change', 'transactions_last_hour', 'transactions_last_day',
        'merchant_risk_score', 'new_merchant', 'failed_attempts'
    ]
    
    # Ensure all columns exist
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
            
    X = df[feature_cols]
    y = df['is_fraud']
    
    return X, y, feature_cols

def train_model(X, y):
    """Train Isolation Forest model"""
    print("Training Isolation Forest (Anomaly Detection) model...")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Isolation Forest
    # contamination = 'auto' or estimated fraud rate (e.g., 0.05)
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05, 
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_scaled)
    
    # Evaluate
    # Isolation Forest predicts -1 for anomalies (fraud) and 1 for normal
    y_pred_iso = model.predict(X_scaled)
    # Convert to 0 (normal) and 1 (fraud)
    y_pred = np.where(y_pred_iso == -1, 1, 0)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    print("\nClassification Report:")
    print(classification_report(y, y_pred, target_names=['Legitimate', 'Fraud']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y, y_pred))
    
    # Save model and scaler
    joblib.dump(model, 'upi_fraud_model.pkl')
    joblib.dump(scaler, 'upi_fraud_scaler.pkl')
    print("\nModel saved as 'upi_fraud_model.pkl'")
    print("Scaler saved as 'upi_fraud_scaler.pkl'")
    
    return model, scaler

if __name__ == "__main__":
    # Load data
    X, y, feature_cols = load_and_prepare_data()
    
    # Train model
    model, scaler = train_model(X, y)
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)
