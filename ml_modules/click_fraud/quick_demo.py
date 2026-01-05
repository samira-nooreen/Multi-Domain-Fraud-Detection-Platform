"""
Quick Demo - Click Fraud Detection
Works without PyTorch - uses Logistic Regression & CatBoost
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os

print("="*70)
print("🖱️  CLICK FRAUD DETECTION - QUICK DEMO")
print("="*70)

# Load or generate data
if not os.path.exists('click_data.csv'):
    print("\n📦 Generating dataset...")
    from generate_data import generate_tabular_data
    X, y = generate_tabular_data(1000)
    df = pd.DataFrame(X, columns=[
        'avg_time_diff', 'std_time_diff', 'min_time_diff', 'max_time_diff',
        'avg_click_x', 'std_click_x', 'avg_click_y', 'std_click_y',
        'total_ip_changes', 'total_ua_changes', 'avg_hour', 'weekend_ratio',
        'avg_click_velocity', 'std_click_velocity', 'total_clicks'
    ])
    df['is_fraud'] = y
    df.to_csv('click_data.csv', index=False)
else:
    df = pd.read_csv('click_data.csv')

print(f"\n📊 Dataset: {len(df)} samples")
print(f"   Normal: {len(df[df['is_fraud']==0])} | Fraud: {len(df[df['is_fraud']==1])}")

# Prepare data
y = df['is_fraud'].values
X = df.drop('is_fraud', axis=1).values

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Logistic Regression
print("\n🚀 Training Logistic Regression...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr.fit(X_train_scaled, y_train)

y_pred = lr.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"✓ Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))

# Try CatBoost if available
try:
    from catboost import CatBoostClassifier
    
    print("\n🚀 Training CatBoost...")
    cb = CatBoostClassifier(
        iterations=100,
        depth=6,
        learning_rate=0.1,
        verbose=False,
        random_state=42
    )
    cb.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=False)
    
    y_pred_cb = cb.predict(X_test)
    accuracy_cb = accuracy_score(y_test, y_pred_cb)
    
    print(f"✓ Accuracy: {accuracy_cb:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_cb, target_names=['Normal', 'Fraud']))
    
except ImportError:
    print("\n⚠️  CatBoost not installed. Install with: pip install catboost")

# Test predictions
print("\n" + "="*70)
print("🧪 TESTING PREDICTIONS")
print("="*70)

# Bot-like session (fast, consistent clicks)
bot_features = np.array([[
    0.12,  # avg_time_diff (very fast)
    0.02,  # std_time_diff (very consistent)
    0.10,  # min_time_diff
    0.15,  # max_time_diff
    500,   # avg_click_x (concentrated)
    5,     # std_click_x (low variance)
    300,   # avg_click_y
    5,     # std_click_y
    0,     # total_ip_changes (no changes)
    0,     # total_ua_changes
    14,    # avg_hour
    0,     # weekend_ratio
    50,    # avg_click_velocity (very high)
    2,     # std_click_velocity
    20     # total_clicks
]])

# Human-like session (slower, varied clicks)
human_features = np.array([[
    2.5,   # avg_time_diff (slower)
    1.2,   # std_time_diff (varied)
    0.8,   # min_time_diff
    5.0,   # max_time_diff
    400,   # avg_click_x (spread out)
    200,   # std_click_x (high variance)
    350,   # avg_click_y
    180,   # std_click_y
    1,     # total_ip_changes
    0,     # total_ua_changes
    15,    # avg_hour
    0.3,   # weekend_ratio
    8,     # avg_click_velocity (normal)
    3,     # std_click_velocity
    15     # total_clicks
]])

print("\n🤖 Bot-like session:")
bot_scaled = scaler.transform(bot_features)
bot_proba = lr.predict_proba(bot_scaled)[0][1]
print(f"   Logistic Regression: {bot_proba:.2%} fraud probability")
print(f"   → {'🚨 FRAUD DETECTED' if bot_proba > 0.5 else '✅ NORMAL'}")

print("\n👤 Human-like session:")
human_scaled = scaler.transform(human_features)
human_proba = lr.predict_proba(human_scaled)[0][1]
print(f"   Logistic Regression: {human_proba:.2%} fraud probability")
print(f"   → {'🚨 FRAUD DETECTED' if human_proba > 0.5 else '✅ NORMAL'}")

print("\n" + "="*70)
print("✅ Demo complete!")
print("\nTo train all 4 models (including Wide & Deep and Autoencoder):")
print("  1. Install: pip install catboost torch")
print("  2. Run: python train.py")
print("="*70)
