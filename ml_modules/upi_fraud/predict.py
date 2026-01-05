"""
UPI Fraud Detection - Prediction Module
Real-time fraud prediction for UPI transactions with minimal inputs
"""
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

class UPIFraudDetector:
    def __init__(self, model_path='upi_fraud_model.pkl', scaler_path='upi_fraud_scaler.pkl'):
        """Initialize the fraud detector"""
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Model loading failed: {e}. Using mock prediction.")
            self.model = None
            self.scaler = None
    
    def predict(self, transaction_data):
        if self.model is None:
            return self._mock_predict(transaction_data)
            
        try:
            # Convert minimal inputs to full feature set
            processed_data = self._process_minimal_inputs(transaction_data)
            
            # Convert to DataFrame
            df = pd.DataFrame([processed_data])
            
            # Ensure all required features are present
            required_features = [
                'amount', 'hour', 'day_of_week', 'transaction_frequency',
                'avg_transaction_amount', 'account_age_days', 'device_change',
                'location_change', 'transactions_last_hour', 'transactions_last_day',
                'merchant_risk_score', 'new_merchant', 'failed_attempts'
            ]
            
            # Fill missing features with defaults
            for feature in required_features:
                if feature not in df.columns:
                    df[feature] = 0
            
            # Select and order features
            X = df[required_features]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Predict
            prediction = self.model.predict(X_scaled)[0]
            probability = self.model.predict_proba(X_scaled)[0]
            
            # Determine risk level
            fraud_prob = probability[1]
            return self._format_result(fraud_prob, transaction_data)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_predict(transaction_data)

    def _process_minimal_inputs(self, data):
        """Convert minimal user inputs to full feature set"""
        # Extract minimal inputs
        amount = float(data.get('amount', 0))
        
        # Parse time of transaction
        time_str = data.get('time_of_transaction', '')
        if time_str:
            try:
                # Assuming time_str is in HH:MM format
                hour = int(time_str.split(':')[0])
            except:
                hour = datetime.now().hour
        else:
            hour = datetime.now().hour
            
        day_of_week = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        # Device change (0/1)
        device_change = int(data.get('device_changed', 0))
        
        # Generate derived features (these would normally come from database/history)
        # For now, we'll generate realistic defaults
        transaction_frequency = np.random.poisson(5)
        avg_transaction_amount = amount * np.random.uniform(0.5, 1.5)
        account_age_days = np.random.randint(30, 3650)
        location_change = np.random.choice([0, 1], p=[0.90, 0.10])
        transactions_last_hour = np.random.poisson(0.5)
        transactions_last_day = np.random.poisson(3)
        merchant_risk_score = np.random.uniform(0, 1)
        new_merchant = np.random.choice([0, 1], p=[0.80, 0.20])
        failed_attempts = np.random.poisson(0.2)
        
        return {
            'amount': amount,
            'hour': hour,
            'day_of_week': day_of_week,
            'transaction_frequency': transaction_frequency,
            'avg_transaction_amount': avg_transaction_amount,
            'account_age_days': account_age_days,
            'device_change': device_change,
            'location_change': location_change,
            'transactions_last_hour': transactions_last_hour,
            'transactions_last_day': transactions_last_day,
            'merchant_risk_score': merchant_risk_score,
            'new_merchant': new_merchant,
            'failed_attempts': failed_attempts
        }
    
    def _mock_predict(self, data):
        # Robust fallback logic
        score = 0
        if float(data.get('amount', 0)) > 50000: score += 0.3
        if int(data.get('failed_attempts', 0)) > 2: score += 0.3
        if float(data.get('merchant_risk_score', 0)) > 0.7: score += 0.2
        if int(data.get('device_change', 0)) == 1: score += 0.1
        
        fraud_prob = min(0.99, score + 0.05)
        return self._format_result(fraud_prob, data)

    def _format_result(self, fraud_prob, data):
        if fraud_prob < 0.3:
            risk_level = "LOW"
            risk_color = "green"
        elif fraud_prob < 0.6:
            risk_level = "MEDIUM"
            risk_color = "yellow"
        elif fraud_prob < 0.8:
            risk_level = "HIGH"
            risk_color = "orange"
        else:
            risk_level = "CRITICAL"
            risk_color = "red"
        
        return {
            'is_fraud': bool(fraud_prob > 0.5),
            'fraud_probability': float(fraud_prob),
            'legitimate_probability': 1 - float(fraud_prob),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendation': self._get_recommendation(fraud_prob, data)
        }

    def _get_recommendation(self, fraud_prob, transaction_data):
        """Generate recommendation based on fraud probability"""
        if fraud_prob > 0.8:
            return "BLOCK TRANSACTION - High fraud risk detected"
        elif fraud_prob > 0.6:
            return "REVIEW REQUIRED - Additional verification recommended"
        elif fraud_prob > 0.3:
            return "MONITOR - Flag for monitoring"
        else:
            return "APPROVE - Low risk transaction"
    
    def batch_predict(self, transactions_df):
        """Predict fraud for multiple transactions"""
        required_features = [
            'amount', 'hour', 'day_of_week', 'transaction_frequency',
            'avg_transaction_amount', 'account_age_days', 'device_change',
            'location_change', 'transactions_last_hour', 'transactions_last_day',
            'merchant_risk_score', 'new_merchant', 'failed_attempts'
        ]
        
        X = transactions_df[required_features]
        X_scaled = self.scaler.transform(X)
        
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        return predictions, probabilities

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = UPIFraudDetector()
    
    # Example transaction with minimal inputs
    transaction = {
        'amount': 75000,
        'time_of_transaction': '02:30',
        'device_changed': 1
    }
    
    # Predict
    result = detector.predict(transaction)
    
    print("="*50)
    print("UPI FRAUD DETECTION RESULT")
    print("="*50)
    print(f"Fraud Detected: {result['is_fraud']}")
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Recommendation: {result['recommendation']}")
    print("="*50)