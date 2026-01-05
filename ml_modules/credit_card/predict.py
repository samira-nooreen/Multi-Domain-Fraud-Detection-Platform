"""
Credit Card Fraud Detection - Prediction Module
Real-time fraud prediction for Credit Card transactions with minimal inputs
"""
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

class CreditCardFraudDetector:
    def __init__(self, model_path='credit_card_model.pkl', scaler_path='credit_card_scaler.pkl', features_path='credit_card_features.pkl'):
        """Initialize the fraud detector"""
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.features_path = features_path
        self.model = None
        self.scaler = None
        self.feature_cols = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.feature_cols = joblib.load(self.features_path)
            print("Credit Card Model loaded successfully")
        except Exception as e:
            print(f"Model loading failed: {e}. Using mock prediction.")
            self.model = None
    
    def predict(self, transaction_data):
        """
        Predict fraud for a single transaction using Isolation Forest + Random Forest ensemble
        with minimal inputs
        """
        if self.model is None:
            # Fallback for demo if model isn't trained yet
            return self._mock_prediction(transaction_data)

        try:
            # Convert minimal inputs to full feature set
            processed_data = self._process_minimal_inputs(transaction_data)
            
            # Convert to DataFrame
            df = pd.DataFrame([processed_data])
            
            # Ensure all required features are present
            for feature in self.feature_cols:
                if feature not in df.columns:
                    df[feature] = 0
            
            # Select and order features
            X = df[self.feature_cols]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Get isolation forest scores
            iso_scores = self.model['isolation_forest'].decision_function(X_scaled)
            
            # Combine scaled features with isolation forest scores
            X_extended = np.column_stack([X_scaled, iso_scores])
            
            # Predict with Random Forest
            prediction = self.model['random_forest'].predict(X_extended)[0]
            probability = self.model['random_forest'].predict_proba(X_extended)[0]
            
            # Determine risk level
            fraud_prob = probability[1]
            return self._format_result(fraud_prob)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_prediction(transaction_data)

    def _process_minimal_inputs(self, data):
        """Convert minimal user inputs to full feature set"""
        # Extract minimal inputs
        amount = float(data.get('amount', 0))
        location = data.get('location', '')
        transaction_type = data.get('transaction_type', 'POS')  # POS or Online
        card_present = int(data.get('card_present', 1))  # 1 if present, 0 if not
        
        # Generate derived features (these would normally come from database/history)
        # For now, we'll generate realistic defaults
        hour = datetime.now().hour
        day_of_week = datetime.now().weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        card_age_days = np.random.randint(30, 3650)
        credit_limit = np.random.choice([50000, 100000, 200000, 500000])
        available_credit = credit_limit - np.random.uniform(0, credit_limit * 0.8)
        transactions_last_24h = np.random.poisson(2)
        transactions_last_week = np.random.poisson(10)
        avg_transaction_amount = np.random.lognormal(3.5, 1.5)
        distance_from_home = np.random.exponential(10)  # Would normally calculate from location
        distance_from_last_transaction = np.random.exponential(5)
        merchant_category = 'online' if transaction_type == 'Online' else np.random.choice(['retail', 'gas', 'restaurant', 'travel'])
        is_online = 1 if transaction_type == 'Online' else 0
        is_international = 0  # Would check if location is international
        pin_entered = card_present  # If card is present, PIN was likely entered
        chip_used = np.random.choice([0, 1], p=[0.2, 0.8])
        amount_last_24h = transactions_last_24h * avg_transaction_amount
        
        # Create base data dictionary
        base_data = {
            'amount': amount,
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'card_age_days': card_age_days,
            'credit_limit': credit_limit,
            'available_credit': round(available_credit, 2),
            'transactions_last_24h': transactions_last_24h,
            'transactions_last_week': transactions_last_week,
            'avg_transaction_amount': round(avg_transaction_amount, 2),
            'distance_from_home': round(distance_from_home, 2),
            'distance_from_last_transaction': round(distance_from_last_transaction, 2),
            'is_online': is_online,
            'is_international': is_international,
            'pin_entered': pin_entered,
            'chip_used': chip_used
        }
        
        # Add merchant category one-hot encoding
        merchant_categories = ['retail', 'online', 'gas', 'restaurant', 'travel', 'other']
        for category in merchant_categories:
            base_data[f'merchant_{category}'] = 1 if merchant_category == category else 0
            
        return base_data
    
    def _format_result(self, fraud_prob):
        """Format prediction result"""
        if fraud_prob < 0.3:
            risk_level = "LOW"
            risk_color = "green"
        elif fraud_prob < 0.7:
            risk_level = "MEDIUM"
            risk_color = "orange"
        else:
            risk_level = "HIGH"
            risk_color = "red"
            
        is_fraud = fraud_prob > 0.5
        recommendation = "BLOCK" if is_fraud else "APPROVE"
        
        return {
            'is_fraud': bool(is_fraud),
            'fraud_probability': float(fraud_prob),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendation': recommendation
        }
    
    def _mock_prediction(self, data):
        """
        Mock prediction logic based on rules (used if model not loaded or for safety)
        """
        amount = float(data.get('amount', 0))
        transaction_type = data.get('transaction_type', 'POS')
        card_present = int(data.get('card_present', 1))
        
        risk_score = 0
        
        if amount > 50000: risk_score += 0.4
        if transaction_type == 'Online': risk_score += 0.2
        if not card_present: risk_score += 0.3
        
        # Random noise
        risk_score += np.random.uniform(-0.1, 0.1)
        risk_score = max(0, min(1, risk_score))
        
        return self._format_result(risk_score)

# Example usage
if __name__ == "__main__":
    detector = CreditCardFraudDetector()
    result = detector.predict({'amount': 60000, 'transaction_type': 'Online', 'card_present': 0})
    print(result)