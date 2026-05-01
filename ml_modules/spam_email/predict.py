"""
Spam Email Prediction - Naive Bayes
Algorithm: Naive Bayes with TF-IDF
"""
import numpy as np
import joblib
import os
import re
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
                match = re.search(r'From:\s*([^\s]+@[^\s]+)', text)
                if match:
                    sender_email = match.group(1).lower()

            sender_domain = self._get_sender_domain(sender_email)
            sender_local = sender_email.split('@', 1)[0] if '@' in sender_email else ''
            urls = re.findall(r'http[s]?://[^\s)\]>]+', text)
            shortened_links = self._extract_shortened_links(urls)
            spoofed_sender = self._detect_sender_spoof(sender_email, sender_domain)
            
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
                proba = min(0.90, proba + 0.25)
            elif spam_count >= 3:
                proba = min(0.85, proba + 0.18)
            elif spam_count >= 2:
                proba = min(0.78, proba + 0.12)
            elif spam_count >= 1:
                proba = min(0.70, proba + 0.06)
            
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
            strong_phishing_indicators = [
                'account suspended', 'login immediately', 'confirm your identity',
                'urgent action required', 'security alert', 'update your payment method',
                'your account will be closed', 'your account will be blocked',
                'bank account will be blocked', 'enter your password',
                'verify immediately'
            ]
            soft_phishing_indicators = [
                'verify your account', 'login to verify', 'click the link below',
                'reset your password'
            ]
            strong_phishing_count = sum(1 for phrase in strong_phishing_indicators if phrase in text_lower)
            soft_phishing_count = sum(1 for phrase in soft_phishing_indicators if phrase in text_lower)
            phishing_count = strong_phishing_count + soft_phishing_count
            phishing_score = (strong_phishing_count * 2) + soft_phishing_count

            # Credential-harvest and account-lockout combos should be treated as high-risk phishing.
            credential_harvest = (
                ('password' in text_lower or 'otp' in text_lower or 'pin' in text_lower)
                and ('enter' in text_lower or 'provide' in text_lower or 'submit' in text_lower)
                and ('verify' in text_lower or 'account' in text_lower)
            )
            account_lockout_threat = (
                'account will be blocked' in text_lower
                or 'bank account will be blocked' in text_lower
                or 'account suspended' in text_lower
                or 'account will be closed' in text_lower
            )

            if credential_harvest:
                phishing_score += 3
            if account_lockout_threat:
                phishing_score += 2

            if phishing_score >= 3:
                proba = min(0.98, proba + 0.40)
            elif phishing_score >= 1:
                proba = min(0.90, proba + 0.25)

            # ============================================
            # SHORTENED/SUSPICIOUS LINKS - Strong increase
            # ============================================
            if len(shortened_links) >= 2:
                proba = min(0.98, proba + 0.30)
            elif len(shortened_links) == 1:
                proba = min(0.90, proba + 0.20)

            # ============================================
            # SENDER SPOOF DETECTION - Strong increase
            # ============================================
            if spoofed_sender:
                proba = min(0.95, proba + 0.30)

            # ============================================
            # LOTTERY / REWARD SCAM DETECTION - Strong increase
            # ============================================
            scam_score = 0
            if ('won' in text_lower and 'prize' in text_lower) or ('lottery' in text_lower and ('won' in text_lower or 'prize' in text_lower)):
                scam_score += 4
            if 'claim your prize now' in text_lower or 'claim now' in text_lower:
                scam_score += 2
            if (re.search(r'₹\s*\d|rs\.?\s*\d|\$\s*\d', text_lower) is not None) and ('won' in text_lower or 'claim' in text_lower):
                scam_score += 2
            if any(token in sender_local for token in ['lottery', 'winner', 'prize', 'claim', 'reward', 'jackpot']):
                scam_score += 3

            if scam_score >= 6:
                proba = min(0.98, proba + 0.35)
            elif scam_score >= 4:
                proba = min(0.95, proba + 0.25)
            elif scam_score >= 2:
                proba = min(0.88, proba + 0.12)

            # Context dampening for routine internal verification language
            # (avoid false positives when soft phrases appear without threat context).
            if (
                strong_phishing_count == 0
                and soft_phishing_count >= 1
                and len(urls) == 0
                and legit_count >= 2
                and trusted_domain_found
            ):
                proba = max(0.05, proba - 0.12)

            # ============================================
            # PROMOTIONAL (NON-PHISHING) CALIBRATION
            # ============================================
            # Keep generic promotional mail as MEDIUM unless phishing/spoof/link abuse exists.
            if (
                spam_count >= 2
                and phishing_count == 0
                and phishing_score < 3
                and scam_score < 2
                and len(shortened_links) == 0
                and not spoofed_sender
            ):
                proba = min(proba, 0.72)
            
            # ============================================
            # FINAL DECISION
            # ============================================
            # Use a stricter spam threshold to reduce borderline false positives.
            is_spam = proba >= 0.6
            confidence_value = abs(proba - 0.5) * 2  # 0-1 scale
            confidence_percent = min(100, max(0, confidence_value * 100))
            
            # Determine risk level
            if proba >= 0.8:
                risk_level = 'HIGH'
            elif proba >= 0.5:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'

            if confidence_percent < 10 and 0.45 <= proba <= 0.65:
                recommendation = 'VERIFY - Borderline result; review sender and content before quarantine'
            else:
                recommendation = (
                    'BLOCK - High confidence spam detected' if proba >= 0.8 else
                    'QUARANTINE - Likely spam' if proba >= 0.6 else
                    'VERIFY - Suspicious promotional content; review before trusting' if proba >= 0.5 else
                    'ALLOW - Legitimate email'
                )

            return {
                'is_spam': bool(is_spam),
                'spam_probability': float(proba),
                'category': 'SPAM' if is_spam else 'HAM',
                'confidence': confidence_value,
                'confidence_percent': round(confidence_percent, 2),
                'risk_level': risk_level,
                'model_used': 'Naive Bayes + Rule-Based Enhancement',
                'recommendation': recommendation,
                'spam_indicators': self._extract_spam_indicators(text, sender_email),
                'trusted_domain': trusted_domain_found,
                'spam_keywords_found': spam_count,
                'legitimate_indicators_found': legit_count,
                'phishing_indicators_found': phishing_count,
                'strong_phishing_indicators_found': strong_phishing_count,
                'scam_score': scam_score,
                'shortened_links_found': len(shortened_links),
                'spoofed_sender_detected': spoofed_sender,
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
        sender_domain = self._get_sender_domain(sender_email)
        
        # Check for spam keywords
        spam_keywords = [
            'free', 'winner', 'urgent', 'click here', 'buy now', 'limited time',
            'offer', 'money', 'cash', 'prize', 'congratulations', 'claim',
            'suspended', 'win', 'lottery', 'million', 'guaranteed', 'hurry'
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

            if self._detect_sender_spoof(sender_email, sender_domain):
                indicators.append("Sender domain appears spoofed for a known brand")
        
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
        urls = re.findall(r'http[s]?://\S+', text)
        if len(urls) > 2:
            indicators.append(f"Multiple links detected ({len(urls)})")

        shortened_links = self._extract_shortened_links(urls)
        if shortened_links:
            indicators.append(f"Shortened or obfuscated link detected ({', '.join(shortened_links[:3])})")
        
        # Check for phishing patterns
        phishing_patterns = ['click the link', 'verify your account', 'login immediately', 'urgent action required']
        if any(pattern in text_lower for pattern in phishing_patterns):
            indicators.append("Phishing pattern detected")

        if ('enter your password' in text_lower or 'provide password' in text_lower or 'submit otp' in text_lower):
            indicators.append("Credential-harvest request detected")

        if ('account will be blocked' in text_lower or 'bank account will be blocked' in text_lower or 'account suspended' in text_lower):
            indicators.append("Account lockout threat detected")

        if ('won' in text_lower and 'prize' in text_lower) or 'lottery' in text_lower:
            indicators.append("Lottery/reward scam pattern detected")

        if 'claim your prize now' in text_lower or 'claim now' in text_lower:
            indicators.append("Urgent reward-claim call to action detected")
        
        if not indicators:
            indicators.append("No specific spam indicators detected")
        
        return " | ".join(indicators)

    def _extract_shortened_links(self, urls):
        """Return shortened-link domains found in URL list."""
        short_domains = {'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly'}
        found = []
        for url in urls:
            domain = url.lower().split('/')[2] if '://' in url else ''
            domain = domain.split(':')[0]
            if domain.startswith('www.'):
                domain = domain[4:]
            if domain in short_domains:
                found.append(domain)
        return found

    def _get_sender_domain(self, sender_email):
        """Extract sender domain from sender email address."""
        if not sender_email or '@' not in sender_email:
            return ''
        return sender_email.split('@', 1)[1].lower().strip()

    def _detect_sender_spoof(self, sender_email, sender_domain):
        """Detect likely brand spoofing in sender email/domain."""
        if not sender_email:
            return False

        brand_domains = {
            'paypal': 'paypal.com',
            'amazon': 'amazon.com',
            'apple': 'apple.com',
            'microsoft': 'microsoft.com',
            'google': 'google.com',
            'netflix': 'netflix.com',
            'bankofamerica': 'bankofamerica.com',
        }

        for brand, official_domain in brand_domains.items():
            if brand in sender_email and not sender_domain.endswith(official_domain):
                return True
        return False
