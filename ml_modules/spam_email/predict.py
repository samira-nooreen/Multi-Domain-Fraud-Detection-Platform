"""
Spam Email Prediction - Naive Bayes
Algorithm: Naive Bayes with TF-IDF
"""
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

class SpamDetector:
    def __init__(self, model_path=None, vec_path=None, model_dir=None):
        """
        Initialize SpamDetector.
        Accepts:
          - model_path + vec_path  (legacy paths to individual files)
          - model_dir              (directory containing models/nb_model.pkl)
        """
        self.model = None
        self.vectorizer = None

        # Priority: explicit paths first, then model_dir, then default
        if model_path and os.path.exists(model_path):
            self._load_from_paths(model_path, vec_path)
        elif model_dir:
            self._load_from_dir(model_dir)
        else:
            # Auto-detect: try same directory as this file
            default_dir = os.path.join(os.path.dirname(__file__), 'models')
            self._load_from_dir(default_dir)

            # Fallback: try root-level files
            if self.model is None:
                root_model = 'spam_model.pkl'
                root_vec = 'spam_vectorizer.pkl'
                if os.path.exists(root_model):
                    self._load_from_paths(root_model, root_vec)

    def _load_from_paths(self, model_path, vec_path=None):
        """Load model and vectorizer from individual file paths."""
        try:
            with open(model_path, 'rb') as f:
                data = joblib.load(f)
            if isinstance(data, dict):
                self.model = data.get('model')
                self.vectorizer = data.get('vectorizer')
            else:
                self.model = data

            # Load separate vectorizer if provided
            if vec_path and os.path.exists(vec_path):
                with open(vec_path, 'rb') as f:
                    self.vectorizer = joblib.load(f)

            print("  Spam model loaded from paths")
        except Exception as e:
            print(f"  Error loading spam model from paths: {e}")

    def _load_from_dir(self, model_dir):
        """Load model from models/nb_model.pkl in directory."""
        model_path = os.path.join(model_dir, 'nb_model.pkl')
        try:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    data = joblib.load(f)
                if isinstance(data, dict):
                    self.model = data.get('model')
                    self.vectorizer = data.get('vectorizer')
                else:
                    self.model = data
                print("  Spam model loaded from dir")
            else:
                print(f"  Model not found at {model_path}")
        except Exception as e:
            print(f"  Error loading spam model from dir: {e}")

    def predict(self, text):
        """Predict spam probability using Naive Bayes with enhanced rules"""
        if self.model is None or self.vectorizer is None:
            return self._mock_predict(text)

        try:
            X = self.vectorizer.transform([text])
            proba = self.model.predict_proba(X)[0][1]
            
            # Extract sender email if present
            sender_email = ''
            if 'From:' in text:
                import re
                match = re.search(r'From:\s*([^\s]+@[^\s]+)', text)
                if match:
                    sender_email = match.group(1).lower()
            
            text_lower = text.lower()
            
            # ============================================
            # TRUSTED DOMAIN DETECTION - Reduce risk
            # ============================================
            trusted_domains = ['.edu', '.gov', '.org', '.ac.in', '.edu.in']
            trusted_domain_found = any(domain in sender_email for domain in trusted_domains)
            
            if trusted_domain_found:
                proba = max(0.05, proba - 0.40)  # Strong reduction for trusted domains
            
            # ============================================
            # LEGITIMATE EMAIL INDICATORS - Reduce risk
            # ============================================
            legitimate_indicators = [
                'university', 'professor', 'assignment', 'meeting', 'schedule',
                'please', 'thank you', 'regards', 'sincerely', 'best',
                'team', 'company', 'office', 'department', 'dear', 'hello',
                'interview', 'candidate', 'availability', 'clarification'
            ]
            legit_count = sum(1 for word in legitimate_indicators if word in text_lower)
            
            if legit_count >= 3:
                proba = max(0.05, proba - 0.35)
            elif legit_count >= 2:
                proba = max(0.10, proba - 0.25)
            elif legit_count >= 1:
                proba = max(0.15, proba - 0.15)
            
            # ============================================
            # SPAM KEYWORD DETECTION - Increase risk
            # ============================================
            spam_keywords = [
                'win', 'free', 'offer', 'click', 'urgent', 'congratulations',
                'lottery', 'prize', 'million', 'cash', 'money', 'guaranteed',
                'limited time', 'act now', 'hurry', 'claim now', 'click here'
            ]
            spam_count = sum(1 for word in spam_keywords if word in text_lower)
            
            if spam_count >= 4:
                proba = min(0.95, proba + 0.40)
            elif spam_count >= 3:
                proba = min(0.90, proba + 0.30)
            elif spam_count >= 2:
                proba = min(0.80, proba + 0.20)
            elif spam_count >= 1:
                proba = min(0.65, proba + 0.10)
            
            # ============================================
            # SUSPICIOUS DOMAIN DETECTION - Increase risk
            # ============================================
            suspicious_domains = ['.xyz', '.ru', '.tk', '.ml', '.ga', '.cf']
            suspicious_domain_found = any(domain in sender_email for domain in suspicious_domains)
            
            if suspicious_domain_found:
                proba = min(0.95, proba + 0.25)
            
            # ============================================
            # PHISHING INDICATORS - Strong increase
            # ============================================
            phishing_indicators = [
                'account suspended', 'verify your account', 'login to verify',
                'click the link below', 'login immediately', 'confirm your identity'
            ]
            phishing_count = sum(1 for phrase in phishing_indicators if phrase in text_lower)
            
            if phishing_count >= 2:
                proba = min(0.98, proba + 0.40)
            elif phishing_count >= 1:
                proba = min(0.90, proba + 0.25)
            
            # ============================================
            # FINAL DECISION
            # ============================================
            is_spam = proba > 0.5
            confidence_value = abs(proba - 0.5) * 2  # 0-1 scale
            confidence_percent = min(100, max(0, confidence_value * 100))
            
            # Determine risk level
            if proba > 0.75:
                risk_level = 'HIGH'
            elif proba > 0.5:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'

            return {
                'is_spam': bool(is_spam),
                'spam_probability': float(proba),
                'category': 'SPAM' if is_spam else 'HAM',
                'confidence': confidence_value,
                'confidence_percent': round(confidence_percent, 2),
                'risk_level': risk_level,
                'model_used': 'Naive Bayes + Rule-Based Enhancement',
                'recommendation': (
                    'BLOCK - High confidence spam detected' if proba > 0.75 else
                    'QUARANTINE - Likely spam' if proba > 0.5 else
                    'ALLOW - Legitimate email'
                ),
                'spam_indicators': self._extract_spam_indicators(text, sender_email),
                'trusted_domain': trusted_domain_found,
                'spam_keywords_found': spam_count,
                'legitimate_indicators_found': legit_count
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._mock_predict(text)

    def _mock_predict(self, text):
        """Fallback heuristic-based prediction"""
        spam_keywords = [
            'free', 'winner', 'urgent', 'click here', 'buy now', 'limited time',
            'offer', 'money', 'cash', 'prize', 'congratulations', 'claim',
            'verify', 'suspended', 'account', 'password', 'reset', 'confirm',
            'won', 'lottery', 'inheritance', 'million', 'bank transfer',
            'nigerian', 'prince', 'unsubscribe', 'earn from home'
        ]

        score = 0.0
        text_lower = text.lower()

        matched = sum(1 for word in spam_keywords if word in text_lower)
        score += min(0.7, matched * 0.08)

        if text.count('!') > 2:
            score += 0.1
        if text.count('$') > 0:
            score += 0.05

        prob = min(0.95, score)

        return {
            'is_spam': bool(prob > 0.5),
            'spam_probability': float(prob),
            'category': 'SPAM' if prob > 0.5 else 'HAM',
            'confidence': 'LOW',
            'risk_level': 'HIGH' if prob > 0.7 else 'MEDIUM' if prob > 0.4 else 'LOW',
            'model_used': 'Heuristic Fallback',
            'recommendation': (
                'BLOCK - Suspicious content detected' if prob > 0.5 else
                'ALLOW - Appears legitimate'
            )
        }
    
    def _extract_spam_indicators(self, text, sender_email=''):
        """Extract specific spam indicators from the email"""
        indicators = []
        text_lower = text.lower()
        
        # Check for spam keywords
        spam_keywords = [
            'free', 'winner', 'urgent', 'click here', 'buy now', 'limited time',
            'offer', 'money', 'cash', 'prize', 'congratulations', 'claim',
            'verify', 'suspended', 'account', 'password', 'reset', 'confirm',
            'win', 'lottery', 'million', 'guaranteed', 'hurry'
        ]
        
        matched_keywords = [word for word in spam_keywords if word in text_lower]
        if matched_keywords:
            indicators.append(f"Spam keywords: {', '.join(matched_keywords[:5])}")
        
        # Check sender domain
        if sender_email:
            suspicious_domains = ['.xyz', '.ru', '.tk', '.ml', '.ga', '.cf']
            if any(domain in sender_email for domain in suspicious_domains):
                indicators.append(f"Suspicious domain in sender email")
            
            trusted_domains = ['.edu', '.gov', '.org']
            if any(domain in sender_email for domain in trusted_domains):
                indicators.append(f"Trusted domain detected")
        
        # Check for excessive punctuation
        if text.count('!') > 3:
            indicators.append(f"Excessive exclamation marks ({text.count('!')})")
        
        if text.count('$') > 2:
            indicators.append("Multiple dollar signs (financial urgency)")
        
        # Check for ALL CAPS
        words = text.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 3]
        if len(caps_words) > 3:
            indicators.append(f"Multiple ALL CAPS words ({len(caps_words)})")
        
        # Check for suspicious links
        import re
        urls = re.findall(r'http[s]?://\S+', text)
        if len(urls) > 2:
            indicators.append(f"Multiple links detected ({len(urls)})")
        
        # Check for phishing patterns
        phishing_patterns = ['click the link', 'verify your account', 'login immediately']
        if any(pattern in text_lower for pattern in phishing_patterns):
            indicators.append("Phishing pattern detected")
        
        if not indicators:
            indicators.append("No specific spam indicators detected")
        
        return " | ".join(indicators)
