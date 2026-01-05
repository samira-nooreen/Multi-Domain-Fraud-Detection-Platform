"""
Insurance Fraud Prediction - Real-Time Inference Engine
Uses Autoencoder (Anomaly Detection)
"""
import pandas as pd
import numpy as np
import joblib
import os

class InsuranceFraudDetector:
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.autoencoder_path = os.path.join(model_dir, 'insurance_autoencoder.pkl')
        self.scaler_path = os.path.join(model_dir, 'insurance_scaler.pkl')
        self.threshold_path = os.path.join(model_dir, 'insurance_threshold.pkl')
        
        self.autoencoder = None
        self.scaler = None
        self.threshold = 0.5
        
        self.load_models()
        
    def load_models(self):
        try:
            if os.path.exists(self.autoencoder_path):
                self.autoencoder = joblib.load(self.autoencoder_path)
                self.scaler = joblib.load(self.scaler_path)
                self.threshold = joblib.load(self.threshold_path)
                print("Insurance autoencoder model loaded successfully.")
            else:
                print("Models not found. Please train first.")
        except Exception as e:
            print(f"Error loading models: {e}")
            self.autoencoder = None

    def predict(self, data):
        if self.autoencoder is None:
            return self._mock_predict(data)
            
        try:
            # 1. Prepare Input Data
            # Ensure all features expected by the model are present
            # Features: age, policy_tenure, policy_amount, claim_amount, claim_ratio, 
            #           past_claims, incident_hour, days_to_report, witness_present, 
            #           police_report, linked_claims
            
            # Handle missing or string inputs
            def get_float(key, default=0.0):
                try:
                    return float(data.get(key, default))
                except:
                    return default

            # Calculate derived features
            claim_amount = get_float('claim_amount')
            policy_amount = get_float('policy_amount', 50000) # Default policy amount if missing
            claim_ratio = claim_amount / policy_amount if policy_amount > 0 else 0
            
            # Simulate Graph Lookup for linked_claims if not provided
            # In a real system, this would query a Graph DB
            linked_claims = get_float('linked_claims', 0)
            
            input_data = {
                'age': get_float('age', 30),
                'policy_tenure': get_float('policy_tenure', 5),
                'policy_amount': policy_amount,
                'claim_amount': claim_amount,
                'claim_ratio': claim_ratio,
                'past_claims': get_float('past_claims', 0),
                'incident_hour': get_float('incident_hour', 12),
                'days_to_report': get_float('days_to_report', 1),
                'witness_present': get_float('witness_present', 0),
                'police_report': get_float('police_report', 0),
                'linked_claims': linked_claims
            }
            
            df = pd.DataFrame([input_data])
            
            # 2. Preprocess
            X_scaled = self.scaler.transform(df)
            
            # 3. Autoencoder Anomaly Detection (Unsupervised)
            reconstruction = self.autoencoder.predict(X_scaled)
            mse = np.mean(np.power(X_scaled - reconstruction, 2), axis=1)[0]
            is_anomaly = mse > self.threshold
            
            # 4. Determine Risk Score
            # Normalize MSE to risk score (0-1)
            final_risk_score = min(mse / (self.threshold * 2), 1.0)
            
            is_fraud = is_anomaly
            
            risk_level = "LOW"
            if final_risk_score > 0.8: risk_level = "CRITICAL"
            elif final_risk_score > 0.6: risk_level = "HIGH"
            elif final_risk_score > 0.4: risk_level = "MODERATE"
            
            # 5. Generate Explanation
            reasons = []
            if is_anomaly: reasons.append(f"Anomalous claim behavior (Score: {mse:.2f})")
            if claim_ratio > 0.8: reasons.append("High claim-to-policy ratio")
            if input_data['days_to_report'] > 14: reasons.append("Late reporting")
            if linked_claims > 2: reasons.append("Suspicious links to other claims")
            
            return {
                'is_fraud': bool(is_fraud),
                'fraud_probability': float(final_risk_score),
                'anomaly_score': float(mse),
                'risk_level': risk_level,
                'reasons': reasons,
                'recommendation': "Reject" if is_fraud else "Approve"
            }
            
        except Exception as e:
            print(f"Prediction Error: {e}")
            return self._mock_predict(data)

    def _mock_predict(self, data):
        # Fallback logic
        score = 0
        reasons = []
        if float(data.get('days_to_report', 0)) > 10: 
            score += 0.3
            reasons.append("Late reporting")
        if float(data.get('claim_amount', 0)) > 20000: 
            score += 0.2
            reasons.append("High claim amount")
        
        is_fraud = score > 0.4
        return {
            'is_fraud': is_fraud,
            'fraud_probability': float(score),
            'risk_level': 'HIGH' if is_fraud else 'LOW',
            'reasons': reasons,
            'recommendation': "Manual Review"
        }
