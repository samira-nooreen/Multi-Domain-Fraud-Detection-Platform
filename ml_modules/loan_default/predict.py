"""
Loan Default Prediction - Real-Time Inference Engine
"""
import joblib
import pandas as pd
import numpy as np
import os

class LoanDefaultPredictor:
    def __init__(self, model_path=None, encoder_path=None):
        if model_path is None:
            # Look for model in the same directory as this file
            import os
            model_path = os.path.join(os.path.dirname(__file__), 'loan_model.pkl')
        self.model_path = model_path
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}. Please train the model first.")

    def predict(self, data):
        """
        Predict loan default risk
        data: dict containing loan application details
        """
        # Convert dict to DataFrame
        df = pd.DataFrame([data])
        
        # Ensure all required columns exist (fill with defaults if missing)
        required_cols = [
            'person_age', 'person_income', 'person_emp_length', 'loan_amnt', 
            'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
            'dti_ratio', 'delinquencies_2yrs', 'revolving_utilization', 
            'total_accounts', 'inquiries_6months', 'public_records',
            'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'
        ]
        
        # Map frontend fields to model fields if necessary
        # (Assuming frontend sends matching keys or we map them here)
        if 'annual_income' in data: df['person_income'] = float(data['annual_income'])
        if 'loan_amount' in data: df['loan_amnt'] = float(data['loan_amount'])
        if 'employment_length' in data: df['person_emp_length'] = float(data['employment_length'])
        if 'credit_score' in data: 
            score = float(data['credit_score'])
            # Estimate missing credit history fields from score
            # High score (700+) -> Low risk features
            # Low score (<600) -> High risk features
            
            if 'delinquencies_2yrs' not in data:
                if score >= 700: df['delinquencies_2yrs'] = 0
                elif score >= 650: df['delinquencies_2yrs'] = 0
                elif score >= 600: df['delinquencies_2yrs'] = 1
                else: df['delinquencies_2yrs'] = 3
                
            if 'revolving_utilization' not in data:
                # 850 -> 0%, 300 -> 100% roughly
                # Linear map: util = 1 - (score - 300) / 550
                util = max(0, min(1, 1 - (score - 300) / 550))
                df['revolving_utilization'] = util
                
            if 'public_records' not in data:
                df['public_records'] = 1 if score < 580 else 0
                
            if 'cb_person_default_on_file' not in data:
                df['cb_person_default_on_file'] = 'Y' if score < 600 else 'N'
        
        # Ensure numeric columns are floats
        numeric_cols = ['dti_ratio', 'loan_int_rate', 'person_income', 'loan_amnt', 'person_emp_length']
        for col in numeric_cols:
            if col in df.columns:
                try:
                    df[col] = df[col].astype(float)
                except:
                    pass # Keep as is if fails, defaults will handle or it will crash later
            
        # Calculate derived features if missing
        if 'loan_percent_income' not in df.columns and 'loan_amnt' in df.columns and 'person_income' in df.columns:
            df['loan_percent_income'] = df['loan_amnt'] / df['person_income']
            
        # Fill missing rich features with averages/modes for inference if not provided
        defaults = {
            'dti_ratio': 0.3,
            'delinquencies_2yrs': 0,
            'revolving_utilization': 0.3,
            'total_accounts': 10,
            'inquiries_6months': 0,
            'public_records': 0,
            'loan_int_rate': 10.0,
            'person_age': 30,
            'cb_person_cred_hist_length': 5,
            'cb_person_default_on_file': 'N',
            'loan_intent': 'PERSONAL',
            'person_home_ownership': 'RENT',
            'loan_grade': 'C'
        }
        
        for col, val in defaults.items():
            if col not in df.columns:
                df[col] = val
                
        # Make prediction
        try:
            prob = self.model.predict_proba(df)[0][1]
            prediction = self.model.predict(df)[0]
        except Exception as e:
            # Fallback if columns mismatch significantly
            print(f"Prediction error: {e}")
            prob = 0.5
            prediction = 0

        # Risk Scoring (0-1000 scale, higher is better/safer? Or higher risk? 
        # Usually Credit Score is higher=better. Risk Score: Higher=Riskier.
        # Let's do Risk Score (0-100) where 100 is Max Risk.
        
        risk_score = int(prob * 1000) # 0 to 1000
        
        # Decision Engine
        if prob < 0.10:
            decision = "APPROVE"
            risk_level = "LOW"
            recommendation = "Auto-approve loan application."
        elif prob < 0.30:
            decision = "MANUAL_REVIEW"
            risk_level = "MEDIUM"
            recommendation = "Refer to underwriter for manual review."
        elif prob < 0.50:
            decision = "CONDITIONAL"
            risk_level = "HIGH"
            recommendation = "Approve with higher interest rate or co-signer."
        else:
            decision = "REJECT"
            risk_level = "VERY_HIGH"
            recommendation = "Decline application due to high default risk."
            
        return {
            'default_probability': float(prob),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'decision': decision,
            'recommendation': recommendation,
            'factors': {
                'Income': f"{df['person_income'].iloc[0]:,.2f}",
                'DTI Ratio': f"{df['dti_ratio'].iloc[0]:.2f}",
                'Loan Amount': f"{df['loan_amnt'].iloc[0]:,.2f}"
            }
        }
