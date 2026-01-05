"""
Loan Default Prediction - Multi-Model Training Pipeline
Algorithms: Logistic Regression, Gradient Boosting (XGBoost-like), Neural Network
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def train_models():
    # Get script directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'loan_data.csv')
    
    # 1. Load Data
    if not os.path.exists(data_path):
        print("Generating data...")
        # Add script dir to path to import generate_data
        import sys
        sys.path.append(base_dir)
        from generate_data import generate_loan_data
        df = generate_loan_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
        
    print(f"Loaded {len(df)} records from {data_path}")

    # 2. Feature Engineering & Preprocessing
    # Define features
    numeric_features = [
        'person_age', 'person_income', 'person_emp_length', 'loan_amnt', 
        'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
        'dti_ratio', 'delinquencies_2yrs', 'revolving_utilization', 
        'total_accounts', 'inquiries_6months', 'public_records'
    ]
    categorical_features = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
    
    X = df.drop('loan_status', axis=1)
    y = df['loan_status']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # 3. Define Models
    models = {
        'LightGBM': Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', lgb.LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                class_weight='balanced'
            ))
        ])
    }
    
    best_model = None
    best_auc = 0
    results = {}
    
    # 4. Train and Evaluate
    print("\nTraining Models...")
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        auc = roc_auc_score(y_test, y_prob)
        results[name] = auc
        
        print(f"{name} AUC: {auc:.4f}")
        print(classification_report(y_test, y_pred))
        
        if auc > best_auc:
            best_auc = auc
            best_model = model
            
    print(f"\nLightGBM Model AUC: {best_auc:.4f}")
    
    # 5. Save Best Model
    model_path = os.path.join(base_dir, 'loan_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"Saved best model to {model_path}")
    
    # Save column names for inference
    feature_names = numeric_features + categorical_features
    features_path = os.path.join(base_dir, 'loan_features.pkl')
    joblib.dump(feature_names, features_path)

if __name__ == "__main__":
    train_models()
