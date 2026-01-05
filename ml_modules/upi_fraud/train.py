"""
UPI Fraud Detection - XGBoost Model Training
Trains an XGBoost classifier for detecting fraudulent UPI transactions with minimal inputs
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_prepare_data(filepath='upi_fraud_data.csv'):
    """Load and prepare the dataset"""
    df = pd.read_csv(filepath)
    
    # Features and target
    feature_cols = [
        'amount', 'hour', 'day_of_week', 'transaction_frequency',
        'avg_transaction_amount', 'account_age_days', 'device_change',
        'location_change', 'transactions_last_hour', 'transactions_last_day',
        'merchant_risk_score', 'new_merchant', 'failed_attempts'
    ]
    
    X = df[feature_cols]
    y = df['is_fraud']
    
    return X, y, feature_cols

def train_model(X, y):
    """Train XGBoost model"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Calculate scale_pos_weight for imbalanced data
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    # Train XGBoost model
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric='auc'
    )
    
    model.fit(
        X_train_scaled, y_train,
        eval_set=[(X_test_scaled, y_test)],
        verbose=False
    )
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluation
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC Score: {auc_score:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    print(f"\nCross-Validation AUC Scores: {cv_scores}")
    print(f"Mean CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    # Save model and scaler
    joblib.dump(model, 'upi_fraud_model.pkl')
    joblib.dump(scaler, 'upi_fraud_scaler.pkl')
    print("\nModel saved as 'upi_fraud_model.pkl'")
    print("Scaler saved as 'upi_fraud_scaler.pkl'")
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
    plt.xlabel('Importance')
    plt.title('Top 10 Feature Importance - UPI Fraud Detection')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    print("Feature importance plot saved as 'feature_importance.png'")
    
    # Plot ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'XGBoost (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve - UPI Fraud Detection')
    plt.legend()
    plt.tight_layout()
    plt.savefig('roc_curve.png')
    print("ROC curve saved as 'roc_curve.png'")
    
    return model, scaler, feature_importance

if __name__ == "__main__":
    # Check if data exists, if not generate it
    if not os.path.exists('upi_fraud_data.csv'):
        print("Data file not found. Generating data...")
        from generate_data import generate_upi_data
        df = generate_upi_data(10000)
        df.to_csv('upi_fraud_data.csv', index=False)
    
    # Load data
    X, y, feature_cols = load_and_prepare_data()
    
    # Train model
    model, scaler, feature_importance = train_model(X, y)
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)