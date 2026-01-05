"""
Credit Card Fraud Detection - Random Forest Model Training
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model():
    """Train Isolation Forest + Random Forest ensemble for credit card fraud detection"""
    
    # Check if data exists
    if not os.path.exists('credit_card_data.csv'):
        print("Generating data...")
        from generate_data import generate_credit_card_data
        df = generate_credit_card_data(15000)
        df.to_csv('credit_card_data.csv', index=False)
    
    # Load data
    df = pd.read_csv('credit_card_data.csv')
    
    # Prepare features
    exclude_cols = ['transaction_id', 'is_fraud']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols]
    y = df['is_fraud']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Isolation Forest (unsupervised)
    print("Training Isolation Forest model...")
    iso_forest = IsolationForest(
        contamination=0.1,  # Adjust based on expected fraud rate
        random_state=42,
        n_estimators=100
    )
    
    # Fit on normal transactions only
    X_normal = X_train_scaled[y_train == 0]
    iso_forest.fit(X_normal)
    
    # Get anomaly scores
    iso_scores_train = iso_forest.decision_function(X_train_scaled)
    iso_scores_test = iso_forest.decision_function(X_test_scaled)
    
    # Train Random Forest with additional isolation forest scores
    print("Training Random Forest model with isolation forest features...")
    # Add isolation forest scores as additional features
    X_train_extended = np.column_stack([X_train_scaled, iso_scores_train])
    X_test_extended = np.column_stack([X_test_scaled, iso_scores_test])
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_extended, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_extended)
    y_pred_proba = model.predict_proba(X_test_extended)[:, 1]
    
    # Evaluation
    print("\n" + "="*50)
    print("CREDIT CARD FRAUD DETECTION - MODEL EVALUATION")
    print("="*50)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC Score: {auc_score:.4f}")
    
    # Feature importance
    # Extend feature names to include isolation forest score
    extended_feature_names = list(feature_cols) + ['isolation_forest_score']
    feature_importance = pd.DataFrame({
        'feature': extended_feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    # Save models
    model_data = {
        'random_forest': model,
        'isolation_forest': iso_forest,
        'scaler': scaler,
        'feature_cols': feature_cols
    }
    joblib.dump(model_data, 'credit_card_model.pkl')
    joblib.dump(scaler, 'credit_card_scaler.pkl')
    joblib.dump(feature_cols, 'credit_card_features.pkl')
    print("\nEnsemble models saved successfully!")
    
    return model, scaler, feature_cols

if __name__ == "__main__":
    train_model()
