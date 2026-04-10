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
    def _parse_device_changed(self, value):
        """Parse device_changed field - handles both string and int inputs"""
        if isinstance(value, str):
            return 1 if value.lower() in ['yes', 'y', 'true', '1'] else 0
        return int(value)
    
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
        # Try to use trained model first, fallback to enhanced mock
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

            # Check model type and predict accordingly
            model_type = type(self.model).__name__

            if model_type in ('IsolationForest',):
                # Isolation Forest: decision_function returns anomaly score
                # Lower (more negative) = more anomalous = more fraud
                score = self.model.decision_function(X_scaled)[0]
                import math
                try:
                    prob = 1 / (1 + math.exp(score * 10))
                except OverflowError:
                    prob = 1.0 if score < 0 else 0.0
            else:
                # XGBoost / RandomForest / any classifier with predict_proba
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba(X_scaled)[0]
                    # class 1 = fraud
                    prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
                else:
                    # Binary predict fallback
                    pred = self.model.predict(X_scaled)[0]
                    prob = float(pred)
            
            base_fraud_prob = prob
            
            # Apply hybrid rule-based boosting (same logic as mock)
            final_prob = self._apply_hybrid_boosting(base_fraud_prob, transaction_data)
            
            return self._format_result(final_prob, transaction_data)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_predict(transaction_data)
    
    def _apply_hybrid_boosting(self, base_prob, data):
        """Apply rule-based boosting to ML probability - SIMPLIFIED VERSION"""
        risk_boost = 0.0
        amount = float(data.get('amount', 0))
        
        # Time-based risk boosting
        time_str = data.get('time_of_transaction', '')
        night_time_boost = 0.0
        if time_str:
            try:
                hour = int(time_str.split(':')[0])
                if hour >= 23 or hour <= 5:
                    night_time_boost = 0.35  # Significant boost for night transactions
                elif hour >= 6 and hour <= 8:
                    night_time_boost = 0.15
            except:
                pass
        
        # Device change boosting
        if self._parse_device_changed(data.get('device_changed', 0)) == 1:
            risk_boost += 0.25
        
        # Use default behavioral deviation (since user_avg_amount field removed)
        user_avg_amount = 5000.0  # Fixed default
        if amount > user_avg_amount * 20:  # 20x deviation (more conservative)
            risk_boost += 0.3
        elif amount > user_avg_amount * 10:  # 10x deviation
            risk_boost += 0.2
        elif amount > user_avg_amount * 5:  # 5x deviation
            risk_boost += 0.1
        
        # High-risk combinations (POST-PROCESSING)
        final_prob = base_prob + risk_boost + night_time_boost
        
        # Ensure minimum risk for critical scenarios
        if amount > 500000 and (night_time_boost > 0.2 or self._parse_device_changed(data.get('device_changed', 0)) == 1):
            final_prob = max(final_prob, 0.25)
        
        if amount > 1000000 and night_time_boost > 0.2:
            final_prob = max(final_prob, 0.4)
        
        return min(0.95, final_prob)

    def _process_minimal_inputs(self, data):
        """Convert minimal user inputs to full feature set - DETERMINISTIC"""
        import hashlib
        # Extract minimal inputs
        amount = float(data.get('amount', 0))
        time_str = data.get('time_of_transaction', '')
        device_change = self._parse_device_changed(data.get('device_changed', 0))
        
        # Create a seed string based on inputs to ensure consistency
        seed_str = f"{amount}_{time_str}_{device_change}"
        
        # Helper for deterministic values
        def get_value(salt, min_val, max_val):
            hash_input = f"{seed_str}_{salt}"
            hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
            return min_val + (hash_val % (max_val - min_val + 1))
            
        def get_clamped_poisson(salt, lam, max_val):
            val = get_value(salt, 0, 100) / 100.0
            if val < 0.1: return 0
            if val < 0.3: return int(lam * 0.5)
            if val < 0.7: return int(lam)
            if val < 0.9: return int(lam * 1.5)
            return min(int(lam * 2.5), max_val)

        # Parse time
        if time_str:
            try:
                hour = int(time_str.split(':')[0])
            except:
                hour = datetime.now().hour
        else:
            hour = datetime.now().hour
            
        day_of_week = datetime.now().weekday()
        
        # Account age: 100 to 2000 days
        account_age_days = get_value("age", 180, 2000)
        
        if amount > 50000:
            avg_transaction_amount = get_value("avg", 2000, 10000)
        else:
            avg_transaction_amount = get_value("avg", int(amount * 0.5) + 1, int(amount * 1.5) + 1)
            
        transaction_frequency = get_clamped_poisson("freq", 3, 10)
        location_change = 1 if get_value("loc", 0, 100) > 95 else 0
        transactions_last_hour = get_clamped_poisson("hist_h", 1, 5)
        transactions_last_day = get_clamped_poisson("hist_d", 5, 20)
        merchant_risk_score = get_value("merch", 1, 100) / 100.0
        new_merchant = 1 if get_value("new_m", 0, 100) > 80 else 0
        failed_attempts = 0 if get_value("fail", 0, 100) > 90 else get_clamped_poisson("fail_c", 0, 2)
        
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
        """Enhanced mock prediction with realistic risk assessment - SIMPLIFIED VERSION"""
        base_score = 0.0
        risk_boost = 0.0
        reasons = []
        
        # Amount-based risk (critical factor)
        amount = float(data.get('amount', 0))
        if amount > 1000000:  # 10+ lakhs
            base_score += 0.4
            reasons.append("Very high transaction amount (Rs.10+ lakhs)")
        elif amount > 500000:  # 5+ lakhs
            base_score += 0.3
            reasons.append("High transaction amount (Rs.5+ lakhs)")
        elif amount > 100000:  # 1+ lakh
            base_score += 0.15
            reasons.append("Moderate transaction amount (Rs.1+ lakh)")
        
        # Time-based risk (CRITICAL for unusual hours)
        time_str = data.get('time_of_transaction', '')
        night_time_risk = 0.0
        if time_str:
            try:
                hour = int(time_str.split(':')[0])
                if hour >= 23 or hour <= 5:
                    night_time_risk = 0.35
                    reasons.append(f"Transaction during unusual hours ({hour:02d}:00)")
                elif hour >= 6 and hour <= 8:
                    night_time_risk = 0.15
                    reasons.append(f"Early morning transaction ({hour:02d}:00)")
            except:
                pass
        
        # Device change risk
        device_change = self._parse_device_changed(data.get('device_changed', 0))
        if device_change == 1:
            risk_boost += 0.25
            reasons.append("Device change detected")
        
        # Amount deviation from average
        user_avg_amount = 5000.0
        if amount > user_avg_amount * 20:
            risk_boost += 0.3
            reasons.append(f"Amount significantly higher than typical (Rs.{user_avg_amount:,.0f})")
        elif amount > user_avg_amount * 10:
            risk_boost += 0.2
            reasons.append(f"Amount much higher than typical (Rs.{user_avg_amount:,.0f})")
        elif amount > user_avg_amount * 5:
            risk_boost += 0.1
            reasons.append(f"Amount higher than typical (Rs.{user_avg_amount:,.0f})")
        
        # Add base risk for any transaction
        base_score += 0.02
        
        final_score = base_score + risk_boost + night_time_risk
        fraud_prob = min(0.95, final_score)
        
        if amount > 500000 and (night_time_risk > 0.2 or device_change == 1):
            fraud_prob = max(fraud_prob, 0.25)
            if "High risk combination detected" not in reasons:
                reasons.append("High risk combination detected")
        
        if amount > 1000000 and night_time_risk > 0.2:
            fraud_prob = max(fraud_prob, 0.4)
            if "Critical risk: High amount at unusual time" not in reasons:
                reasons.append("Critical risk: High amount at unusual time")
        
        result = self._format_result(fraud_prob, data)
        result['risk_factors'] = reasons
        return result

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
        """Generate recommendation based on fraud probability and risk factors"""
        amount = float(transaction_data.get('amount', 0))
        time_str = transaction_data.get('time_of_transaction', '')
        device_changed = int(transaction_data.get('device_changed', 0))
        
        is_high_value = amount > 500000
        is_very_high_value = amount > 1000000
        
        is_unusual_time = False
        if time_str:
            try:
                hour = int(time_str.split(':')[0])
                is_unusual_time = (hour >= 23 or hour <= 5)
            except:
                pass
        
        if fraud_prob > 0.7:
            if is_very_high_value and is_unusual_time:
                return "BLOCK TRANSACTION - Rs.10+ lakh at unusual hours is extremely high risk"
            elif is_very_high_value and device_changed:
                return "BLOCK TRANSACTION - Rs.10+ lakh with device change requires immediate verification"
            else:
                return "BLOCK TRANSACTION - Critical fraud risk detected"
        elif fraud_prob > 0.5:
            if is_very_high_value:
                return "STEP-UP AUTHENTICATION REQUIRED - Rs.10+ lakh transaction needs additional verification"
            elif is_high_value and (is_unusual_time or device_changed):
                return "STEP-UP AUTHENTICATION REQUIRED - High-value transaction with risk factors"
            else:
                return "REVIEW REQUIRED - High fraud risk detected"
        elif fraud_prob > 0.3:
            if is_high_value or is_unusual_time:
                return "ADDITIONAL VERIFICATION - Medium-high risk transaction"
            else:
                return "MONITOR - Medium fraud risk detected"
        elif fraud_prob > 0.15:
            return "CAUTION ADVISED - Low-medium risk transaction"
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
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X_scaled)[:, 1]
        else:
            probabilities = predictions.astype(float)
        return predictions, probabilities
