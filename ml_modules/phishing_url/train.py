"""
Phishing URL Detection - XGBoost Training
"""
import pandas as pd
import numpy as np
import math
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import xgboost as xgb

def get_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text: return 0
    counts = Counter(text)
    length = len(text)
    entropy = 0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def get_special_chars_count(text):
    """Count special characters"""
    return sum(1 for c in text if not c.isalnum())

def simulate_whois_age(row):
    """
    Simulate WHOIS age (in days).
    Phishing sites tend to be newer (low age).
    Legitimate sites tend to be older (high age).
    """
    if row['is_phishing'] == 1:
        # Phishing: 1 to 60 days (mostly new)
        return np.random.randint(1, 60)
    else:
        # Legitimate: 365 to 3650 days (1 to 10 years)
        return np.random.randint(365, 3650)

def train_model():
    print("🚀 Starting Phishing URL Detection Training...")
    
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'phishing_data.csv')
    model_path = os.path.join(base_dir, 'phishing_model.pkl')
    
    if not os.path.exists(data_path):
        print("⚠️ Dataset not found. Generating dummy data...")
        from generate_data import generate_url_data
        df = generate_url_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    
    print(f"📊 Loaded {len(df)} samples")
    
    # Feature Engineering
    print("🛠️ Extracting features...")
    
    # 1. Length
    df['length'] = df['url'].apply(len)
    
    # 2. Special Characters
    df['special_chars'] = df['url'].apply(get_special_chars_count)
    
    # 3. Token Entropy
    df['token_entropy'] = df['url'].apply(get_entropy)
    
    # 4. Whois Age (Simulated for theory/training purposes)
    # In a real scenario, this would be fetched via WHOIS API
    df['whois_age'] = df.apply(simulate_whois_age, axis=1)
    
    # Features to use
    feature_cols = ['length', 'special_chars', 'whois_age', 'token_entropy']
    X = df[feature_cols]
    y = df['is_phishing']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost
    print("⚡ Training XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save Model
    model_data = {
        'model': model,
        'feature_cols': feature_cols
    }
    joblib.dump(model_data, model_path)
    print(f"💾 Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
