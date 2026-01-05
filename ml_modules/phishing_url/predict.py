"""
Phishing URL Prediction
"""
import joblib
import pandas as pd
import numpy as np
import math
from collections import Counter
import xgboost as xgb
import os

class PhishingDetector:
    def __init__(self, model_path='phishing_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.feature_cols = None
        self.load_model()
        
    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                data = joblib.load(self.model_path)
                if isinstance(data, dict) and 'model' in data:
                    self.model = data['model']
                    self.feature_cols = data.get('feature_cols', [])
                else:
                    self.model = data # Fallback for old models
            else:
                print(f"Model file {self.model_path} not found.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def _get_entropy(self, text):
        if not text: return 0
        counts = Counter(text)
        length = len(text)
        entropy = 0
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy

    def _get_special_chars_count(self, text):
        return sum(1 for c in text if not c.isalnum())

    def _get_whois_age_heuristic(self, url):
        """
        Heuristic for WHOIS age during inference (since we don't have real-time WHOIS API).
        Assume shorter, cleaner domains are older.
        Longer, complex domains are newer.
        """
        # Extract domain roughly
        try:
            domain = url.split('//')[-1].split('/')[0]
        except:
            domain = url
            
        if len(domain) < 10:
            return 2000 # Old (days)
        elif len(domain) < 20:
            return 500 # Medium
        else:
            return 10 # New (very risky)

    def predict(self, url):
        if self.model is None:
            return self._mock_predict(url)
            
        try:
            # Extract features
            features = {
                'length': len(url),
                'special_chars': self._get_special_chars_count(url),
                'whois_age': self._get_whois_age_heuristic(url),
                'token_entropy': self._get_entropy(url)
            }
            
            # Create DataFrame with correct column order
            if self.feature_cols:
                df = pd.DataFrame([features])[self.feature_cols]
            else:
                # Fallback if feature_cols not saved
                df = pd.DataFrame([features])
            
            # Predict
            prob = self.model.predict_proba(df)[0][1]
            
            return {
                'is_phishing': bool(prob > 0.5),
                'phishing_probability': float(prob),
                'risk_level': 'CRITICAL' if prob > 0.8 else ('HIGH' if prob > 0.5 else 'LOW')
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_predict(url)
            
    def _mock_predict(self, url):
        # Heuristic fallback
        score = 0
        if len(url) > 50: score += 0.3
        if self._get_special_chars_count(url) > 5: score += 0.3
        if self._get_entropy(url) > 4.5: score += 0.2
        
        prob = min(0.95, score)
        return {
            'is_phishing': bool(prob > 0.5),
            'phishing_probability': float(prob),
            'risk_level': 'HIGH' if prob > 0.5 else 'LOW'
        }
