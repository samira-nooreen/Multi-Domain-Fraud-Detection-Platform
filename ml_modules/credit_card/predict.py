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
    def _extract_hour(self, time_value):
        """Extract hour from HH:MM (24h) or HH:MM AM/PM formats."""
        if not time_value:
            return None
        try:
            raw = str(time_value).strip()
            if 'am' in raw.lower() or 'pm' in raw.lower():
                dt = datetime.strptime(raw.upper(), '%I:%M %p')
                return dt.hour
            return int(raw.split(':')[0])
        except Exception:
            return None

    def _is_foreign_or_unusual_location(self, location):
        """Heuristic check for foreign or unusual transaction location."""
        if not location:
            return True

        loc = location.lower().strip()
        indian_markers = [
            'india', 'mumbai', 'delhi', 'bangalore', 'bengaluru', 'chennai',
            'hyderabad', 'pune', 'kolkata', 'ahmedabad', 'jaipur', 'surat',
            'lucknow', 'indore', 'kochi', 'nagpur', 'noida', 'gurgaon', 'thane'
        ]
        if any(marker in loc for marker in indian_markers):
            return False

        foreign_markers = [
            'new york', 'usa', 'united states', 'uk', 'london', 'canada', 'toronto',
            'dubai', 'singapore', 'paris', 'sydney', 'berlin', 'tokyo',
            'foreign', 'international', 'unknown', 'unusual'
        ]
        return any(marker in loc for marker in foreign_markers)

    def __init__(self, model_path='ml_modules/credit_card/credit_card_model.pkl',
                 scaler_path='ml_modules/credit_card/credit_card_scaler.pkl',
                 features_path='ml_modules/credit_card/credit_card_features.pkl'):
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
        Predict fraud for a single transaction.
        Uses ensemble model with rule-based boosting for high-risk cases.
        """
        amount = float(transaction_data.get('amount', 0))
        transaction_type = transaction_data.get('transaction_type', 'POS')
        card_present = int(transaction_data.get('card_present', 1))
        location = transaction_data.get('location', '').lower()
        transaction_time = transaction_data.get('time_of_transaction', '')
        hour = self._extract_hour(transaction_time)
        is_unusual_hour = hour is not None and (hour >= 23 or hour <= 5)
        is_foreign_or_unusual_location = self._is_foreign_or_unusual_location(location)

        high_risk_indicators = []

        # Immediate extreme-risk override (before any model)
        if amount >= 1000000 and transaction_type == 'Online' and not card_present:
            fraud_prob = 0.95
            result = self._format_result(fraud_prob)
            result['risk_factors'] = [
                "Very high transaction amount (Rs.10+ lakhs)",
                "Online transaction without card present",
                "EXTREME RISK: Combination of very high amount, online, no card present"
            ]
            return result

        if self.model is None:
            return self._mock_prediction(transaction_data)

        try:
            processed_data = self._process_minimal_inputs(transaction_data)
            df = pd.DataFrame([processed_data])

            for feature in self.feature_cols:
                if feature not in df.columns:
                    df[feature] = 0

            X = df[self.feature_cols]
            X_scaled = self.scaler.transform(X)

            # Handle both ensemble dict model and plain classifier
            if isinstance(self.model, dict):
                iso_scores = self.model['isolation_forest'].decision_function(X_scaled)
                X_extended = np.column_stack([X_scaled, iso_scores])
                probability = self.model['random_forest'].predict_proba(X_extended)[0]
                fraud_prob = round(float(probability[1]), 4)
            else:
                # Plain classifier (e.g. RandomForest, XGBoost, LightGBM)
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba(X_scaled)[0]
                    fraud_prob = round(float(proba[1]) if len(proba) > 1 else float(proba[0]), 4)
                else:
                    pred = float(self.model.predict(X_scaled)[0])
                    fraud_prob = pred

            # Rule-based boosting on top of model score
            
            # AMOUNT-BASED RISK
            if amount >= 1000000:
                high_risk_indicators.append("Very high transaction amount (Rs.10+ lakhs)")
                if fraud_prob < 0.70:
                    fraud_prob = 0.75  # Force HIGH risk for 10L+
            elif amount >= 500000:
                high_risk_indicators.append("High transaction amount (Rs.5+ lakhs)")
                if fraud_prob < 0.50:
                    fraud_prob = 0.55  # Force MEDIUM-HIGH for 5L+
            elif amount >= 100000:
                if fraud_prob < 0.20 and transaction_type == 'Online':
                    fraud_prob = 0.30  # Push to MEDIUM for 1L+ online
                    high_risk_indicators.append("Medium-high transaction amount (Rs.1L+)")
            elif amount >= 50000:
                if fraud_prob < 0.15 and transaction_type == 'Online' and not card_present:
                    fraud_prob = 0.25  # MEDIUM risk for 50K+ online no card

            # TRANSACTION TYPE RISK
            if transaction_type == 'Online' and not card_present:
                high_risk_indicators.append("Online transaction without card present")
                # Apply amount-aware floor so normal e-commerce is not over-penalized.
                if amount >= 500000:
                    cnp_floor = 0.70
                elif amount >= 100000:
                    cnp_floor = 0.58
                elif amount >= 50000:
                    cnp_floor = 0.48
                else:
                    cnp_floor = 0.35
                fraud_prob = min(0.95, max(fraud_prob, cnp_floor))

            # Location context risk
            if is_foreign_or_unusual_location:
                high_risk_indicators.append("Foreign or unusual transaction location")
                fraud_prob = min(0.95, fraud_prob + (0.12 if amount >= 50000 else 0.07))

            # Time-of-day risk (if provided)
            if is_unusual_hour:
                high_risk_indicators.append("Transaction during unusual hours")
                fraud_prob = min(0.95, fraud_prob + 0.18)
            elif hour is not None and 6 <= hour <= 8:
                high_risk_indicators.append("Early-hour transaction")
                fraud_prob = min(0.95, fraud_prob + 0.07)

            if amount >= 500000 and transaction_type == 'Online':
                fraud_prob = min(0.95, fraud_prob * 1.5)
                high_risk_indicators.append("High-value online transaction")

            if not card_present and amount >= 100000:
                fraud_prob = min(0.95, fraud_prob + 0.20)
                high_risk_indicators.append("Card not present for significant amount")

            if not card_present and amount >= 50000:
                fraud_prob = min(0.95, max(fraud_prob, 0.45))

            # Force HIGH for interview-realistic red-flag combos
            if transaction_type == 'Online' and not card_present and amount >= 75000:
                if is_foreign_or_unusual_location and is_unusual_hour:
                    fraud_prob = min(0.95, max(fraud_prob, 0.68))
                    high_risk_indicators.append("High-risk combo: online CNP + foreign location + unusual hour")
                elif is_foreign_or_unusual_location or is_unusual_hour:
                    fraud_prob = min(0.95, max(fraud_prob, 0.60))
                    high_risk_indicators.append("High-risk combo: online CNP with major contextual red flag")
            
            # Ensure minimum probability shows some risk (not 0%)
            if fraud_prob < 0.01 and amount > 0:
                fraud_prob = 0.01  # At least 0.01% to show it's being analyzed

            result = self._format_result(fraud_prob)
            if high_risk_indicators:
                result['risk_factors'] = high_risk_indicators
            return result

        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_prediction(transaction_data)

    def _process_minimal_inputs(self, data):
        """Convert minimal user inputs to full feature set - DETERMINISTIC"""
        import hashlib
        
        amount = float(data.get('amount', 0))
        location = data.get('location', '')
        transaction_type = data.get('transaction_type', 'POS')
        card_present = int(data.get('card_present', 1))
        time_of_transaction = data.get('time_of_transaction', '')
        
        seed_str = f"{amount}_{location}_{transaction_type}_{card_present}"
        
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
        
        parsed_hour = self._extract_hour(time_of_transaction)
        hour = parsed_hour if parsed_hour is not None else datetime.now().hour
        day_of_week = datetime.now().weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        card_age_days = get_value("age", 180, 3650)
        
        if amount >= 1000000:
            credit_limit = 2000000
            available_credit = 500000
        elif amount >= 500000:
            credit_limit = 1000000
            available_credit = 300000
        elif amount >= 100000:
            credit_limit = 500000
            available_credit = 200000
        else:
            credit_limit = [100000, 200000, 500000][get_value("limit", 0, 2)]
            available_credit = credit_limit - (get_value("avail", 0, 70) / 100.0 * credit_limit)
        
        if amount >= 500000:
            transactions_last_24h = get_clamped_poisson("vel_h_high", 8, 20)
            transactions_last_week = get_clamped_poisson("vel_w_high", 25, 50)
        else:
            transactions_last_24h = get_clamped_poisson("vel_h", 2, 5)
            transactions_last_week = get_clamped_poisson("vel_w", 10, 20)
            
        if amount >= 500000:
            avg_transaction_amount = amount / 20
        else:
            avg_transaction_amount = get_value("avg", int(amount * 0.2) + 1, int(amount * 0.8) + 1)
            if avg_transaction_amount < 100: avg_transaction_amount = 500
        
        if amount >= 500000:
            distance_from_home = get_value("dist_h_high", 50, 200)
            distance_from_last_transaction = get_value("dist_l_high", 25, 100)
        else:
            distance_from_home = get_value("dist_h", 1, 20)
            distance_from_last_transaction = get_value("dist_l", 0, 10)
            
        if transaction_type == 'Online':
            merchant_category = 'online'
        else:
            cats = ['retail', 'gas', 'restaurant', 'travel']
            merchant_category = cats[get_value("cat", 0, 3)]
            
        is_online = 1 if transaction_type == 'Online' else 0
        is_international = 0
        pin_entered = card_present
        chip_used = 1 if card_present else 0
        
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
        
        merchant_categories = ['retail', 'online', 'gas', 'restaurant', 'travel', 'other']
        for category in merchant_categories:
            base_data[f'merchant_{category}'] = 1 if merchant_category == category else 0
            
        return base_data
    
    def _format_result(self, fraud_prob):
        """Format prediction result with proper risk classification"""
        if fraud_prob < 0.15:
            risk_level = "LOW"
            risk_color = "green"
            recommendation = "APPROVE"
        elif fraud_prob < 0.3:
            risk_level = "LOW-MEDIUM"
            risk_color = "yellow"
            recommendation = "MONITOR"
        elif fraud_prob < 0.5:
            risk_level = "MEDIUM"
            risk_color = "orange"
            recommendation = "REVIEW REQUIRED"
        elif fraud_prob < 0.7:
            risk_level = "HIGH"
            risk_color = "red"
            recommendation = "STEP-UP AUTHENTICATION"
        else:
            risk_level = "CRITICAL"
            risk_color = "darkred"
            recommendation = "BLOCK TRANSACTION"
            
        return {
            'is_fraud': bool(fraud_prob > 0.5),
            'fraud_probability': float(fraud_prob),
            'legitimate_probability': round(1 - float(fraud_prob), 4),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendation': recommendation
        }
    
    def _mock_prediction(self, data):
        """Enhanced mock prediction with proper fraud detection rules"""
        amount = float(data.get('amount', 0))
        transaction_type = data.get('transaction_type', 'POS')
        card_present = int(data.get('card_present', 1))
        location = data.get('location', '').lower()
        time_of_transaction = data.get('time_of_transaction', '')
        hour = self._extract_hour(time_of_transaction)
        is_unusual_hour = hour is not None and (hour >= 23 or hour <= 5)
        is_foreign_or_unusual_location = self._is_foreign_or_unusual_location(location)
        
        risk_factors = []
        risk_score = 0.0
        
        # Amount-based risk
        if amount >= 1000000:
            risk_score += 0.5
            risk_factors.append("Very high transaction amount (Rs.10+ lakhs)")
        elif amount >= 500000:
            risk_score += 0.35
            risk_factors.append("High transaction amount (Rs.5+ lakhs)")
        elif amount >= 100000:
            risk_score += 0.2
            risk_factors.append("Moderate transaction amount (Rs.1+ lakh)")
        elif amount >= 50000:
            risk_score += 0.1
            risk_factors.append("Significant transaction amount (Rs.50k+)")
        
        # Transaction type risk
        if transaction_type == 'Online':
            risk_score += 0.1
            risk_factors.append("Online transaction")
        elif transaction_type == 'ATM':
            risk_score += 0.1
            risk_factors.append("ATM transaction")
        
        # Card present risk (important but not always high-risk by itself)
        if not card_present:
            risk_score += 0.18
            risk_factors.append("Card not present")
        
        # Online + no card = very high risk
        if transaction_type == 'Online' and not card_present:
            risk_score += 0.08  # Extra boost for CNP e-commerce pattern
            risk_factors.append("Card-not-present online transaction (high fraud risk)")
        
        # Location-based risk
        if is_foreign_or_unusual_location:
            risk_score += 0.1
            risk_factors.append("Foreign or unusual location")

        if is_unusual_hour:
            risk_score += 0.18
            risk_factors.append("Transaction during unusual hours")
        
        risk_score += 0.03  # Base risk

        if transaction_type == 'Online' and not card_present and amount >= 75000:
            if is_foreign_or_unusual_location and is_unusual_hour:
                risk_score = max(risk_score, 0.68)
                risk_factors.append("High-risk combo: online CNP + foreign location + unusual hour")
            elif is_foreign_or_unusual_location or is_unusual_hour:
                risk_score = max(risk_score, 0.60)
                risk_factors.append("High-risk combo: online CNP with major contextual red flag")

        risk_score = min(0.95, risk_score)
        
        result = self._format_result(risk_score)
        result['risk_factors'] = risk_factors
        return result
