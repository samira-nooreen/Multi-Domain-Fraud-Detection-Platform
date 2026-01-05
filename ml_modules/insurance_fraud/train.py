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
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import classification_report, roc_auc_score, mean_squared_error

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
    
    X = df[features]
    y = df['is_fraud']
    
    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Autoencoder (Unsupervised Anomaly Detection)
    # Train only on NON-FRAUD data to learn "normal" patterns
    print("\nTraining Autoencoder...")
    X_normal = X_scaled[y == 0]
    
    # Simple Autoencoder using MLPRegressor
    # Input -> Hidden (Bottleneck) -> Output
    autoencoder = MLPRegressor(
        hidden_layer_sizes=(16, 8, 16), # Bottleneck at 8
        activation='relu',
        solver='adam',
        max_iter=200,
        random_state=42
    )
    
    # Fit to reconstruct input
    autoencoder.fit(X_normal, X_normal)
    
    # Calculate reconstruction error threshold
    reconstructions = autoencoder.predict(X_normal)
    mse = np.mean(np.power(X_normal - reconstructions, 2), axis=1)
    threshold = np.percentile(mse, 95) # 95th percentile of normal error
    
    print(f"Autoencoder trained. Anomaly Threshold (MSE): {threshold:.4f}")
    
    # 5. Save Models
    joblib.dump(autoencoder, os.path.join(base_dir, 'insurance_autoencoder.pkl'))
    joblib.dump(scaler, os.path.join(base_dir, 'insurance_scaler.pkl'))
    joblib.dump(threshold, os.path.join(base_dir, 'insurance_threshold.pkl'))
    
    print("Models saved successfully.")

if __name__ == "__main__":
    train_models()
