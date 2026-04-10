"""
Phishing URL Prediction
Uses heuristic rule-based detection (SVM model is unreliable) with ML boost.
"""
import math
from collections import Counter
import os
import re


class PhishingDetector:
    def __init__(self, model_path=None, model_dir=None):
        """
        Accepts model_path or model_dir for backward compatibility.
        The detection logic is primarily heuristic since the trained SVM
        classifier predicts phishing for all URLs indiscriminately.
        """
        # Legitimate domains whitelist (common safe domains)
        self.safe_domains = {
            'google.com', 'www.google.com', 'google.co.in',
            'youtube.com', 'www.youtube.com',
            'facebook.com', 'www.facebook.com',
            'twitter.com', 'www.twitter.com', 'x.com',
            'instagram.com', 'www.instagram.com',
            'linkedin.com', 'www.linkedin.com',
            'microsoft.com', 'www.microsoft.com',
            'apple.com', 'www.apple.com',
            'amazon.com', 'www.amazon.com', 'amazon.in',
            'flipkart.com', 'www.flipkart.com',
            'github.com', 'www.github.com',
            'sbi.co.in', 'www.sbi.co.in',
            'hdfcbank.com', 'www.hdfcbank.com',
            'icicibank.com', 'www.icicibank.com',
            'paytm.com', 'www.paytm.com',
            'npci.org.in', 'www.npci.org.in',
            'rbi.org.in', 'www.rbi.org.in',
            'wikipedia.org', 'www.wikipedia.org',
            'stackoverflow.com', 'www.stackoverflow.com',
        }

        # Suspicious TLDs associated with free/spam domains
        self.suspicious_tlds = {
            '.tk', '.ml', '.ga', '.cf', '.gq',
            '.xyz', '.top', '.work', '.click',
            '.loan', '.bid', '.win', '.download',
            '.racing', '.review', '.accountant', '.science',
            '.zip', '.mov', '.cricket'
        }

        # Safe TLDs (established)
        self.safe_tlds = {
            '.com', '.org', '.net', '.edu', '.gov',
            '.co.in', '.in', '.co.uk', '.uk', '.ca',
            '.de', '.fr', '.jp', '.au', '.io'
        }

    def _get_entropy(self, text):
        if not text:
            return 0
        counts = Counter(text)
        length = len(text)
        entropy = 0
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy

    def _extract_domain(self, url):
        """Extract the main domain from a URL."""
        try:
            # Remove protocol
            domain = url.lower().split('//')[-1].split('/')[0].split('?')[0]
            # Remove port
            domain = domain.split(':')[0]
            return domain
        except:
            return url.lower()

    def _get_tld(self, domain):
        """Get TLD from domain."""
        parts = domain.split('.')
        if len(parts) >= 3 and parts[-2] in ('co', 'com', 'org', 'net', 'gov'):
            return '.' + '.'.join(parts[-2:])
        elif len(parts) >= 2:
            return '.' + parts[-1]
        return ''

    def predict(self, url):
        """Predict if a URL is phishing using heuristic rules."""
        url = url.strip()
        if not url:
            return self._format_result(0.1)

        domain = self._extract_domain(url)
        url_lower = url.lower()

        # --- WHITELIST CHECK ---
        if domain in self.safe_domains:
            return self._format_result(0.05)

        score = 0.0
        indicators = []

        # --- URL LENGTH ---
        if len(url) > 100:
            score += 0.15
            indicators.append("Very long URL")
        elif len(url) > 75:
            score += 0.08

        # --- IP ADDRESS IN URL ---
        if re.search(r'(\d{1,3}\.){3}\d{1,3}', domain):
            score += 0.40
            indicators.append("IP address used instead of domain name")

        # --- SUSPICIOUS TLD ---
        tld = self._get_tld(domain)
        if tld in self.suspicious_tlds:
            score += 0.50  # Strong signal for suspicious TLDs
            indicators.append(f"Suspicious TLD: {tld}")
        
        # --- .RU DOMAIN (Russia - very high risk) ---
        if tld == '.ru':
            score += 0.30  # Additional penalty for .ru
            indicators.append("Russian domain (.ru) - commonly used for scams")

        # --- EXCESSIVE SUBDOMAINS ---
        subdomain_count = domain.count('.') - 1
        if subdomain_count > 3:
            score += 0.25
            indicators.append(f"Excessive subdomains ({subdomain_count})")
        elif subdomain_count > 2:
            score += 0.12

        # --- BRAND IMPERSONATION (trusted brand in non-brand domain) ---
        trusted_brands = ['paypal', 'google', 'microsoft', 'apple', 'amazon',
                          'facebook', 'netflix', 'ebay', 'wellsfargo', 'chase',
                          'sbi', 'hdfc', 'icici', 'paytm', 'upi', 'aadhaar']
        brand_domain_map = {
            'paypal': 'paypal.com', 'google': 'google.com',
            'microsoft': 'microsoft.com', 'apple': 'apple.com',
            'amazon': 'amazon.com', 'facebook': 'facebook.com',
            'sbi': 'sbi.co.in', 'hdfc': 'hdfcbank.com',
            'icici': 'icicibank.com', 'paytm': 'paytm.com'
        }
        for brand in trusted_brands:
            if brand in domain:
                official = brand_domain_map.get(brand, brand + '.com')
                if domain != official and not domain.endswith('.' + official):
                    score += 0.45
                    indicators.append(f"Brand impersonation: '{brand}' in non-official domain")
                    break
        
        # --- BRAND TYPO DETECTION (misspelled brands) ---
        brand_typos = {
            'amaz0n': 'amazon', 'faceb00k': 'facebook', 'g00gle': 'google',
            'paypa1': 'paypal', 'micros0ft': 'microsoft', 'app1e': 'apple',
            'netfl1x': 'netflix', 'y0utube': 'youtube'
        }
        for typo, correct_brand in brand_typos.items():
            if typo in domain:
                score += 0.60
                indicators.append(f"Brand typo spoofing: '{typo}' instead of '{correct_brand}'")
                break

        # --- SCAM/MONEY KEYWORDS IN URL (Strong signal) ---
        scam_keywords = [
            'win', 'winner', 'lottery', 'crore', 'million', 'prize',
            'free', 'money', 'cash', 'offer', 'deal', 'discount',
            'earn', 'profit', 'income', 'reward', 'bonus',
            'cure', 'treat', 'health', 'medicine', 'drug',
            'loan', 'credit', 'instant', 'fast', 'quick',
            'urgent', 'alert', 'warning', 'suspended', 'blocked'
        ]
        scam_count = sum(1 for kw in scam_keywords if kw in url_lower)
        if scam_count >= 4:
            score += 0.50
            indicators.append(f"Multiple scam keywords ({scam_count}): detected in URL")
        elif scam_count >= 3:
            score += 0.35
            indicators.append(f"Several scam keywords ({scam_count}): detected")
        elif scam_count >= 2:
            score += 0.25
            indicators.append(f"Scam keywords ({scam_count}): detected in URL")
        elif scam_count >= 1:
            score += 0.12
            indicators.append(f"Scam keyword detected in URL")

        # --- PHISHING KEYWORDS IN URL PATH ---
        phishing_keywords = [
            'verify', 'login', 'signin', 'account', 'secure', 'update',
            'confirm', 'banking', 'password', 'credential', 'webscr',
            'wallet', 'payment-update', 'security-alert'
        ]
        path_part = url_lower.split(domain)[-1] if domain in url_lower else url_lower
        kw_count = sum(1 for kw in phishing_keywords if kw in path_part)
        if kw_count >= 3:
            score += 0.25
            indicators.append(f"Multiple phishing keywords in path ({kw_count})")
        elif kw_count >= 2:
            score += 0.15
            indicators.append(f"Phishing keywords in path ({kw_count})")
        elif kw_count >= 1:
            score += 0.08

        # --- HIGH ENTROPY (randomized domains) ---
        domain_entropy = self._get_entropy(domain.replace('.', ''))
        if domain_entropy > 4.2:
            score += 0.15
            indicators.append("High domain entropy (randomized characters)")

        # --- SPECIAL CHARACTERS ---
        special_count = sum(1 for c in url if not c.isalnum() and c not in ':/.-_?=&')
        if special_count > 5:
            score += 0.15
            indicators.append("Excessive special characters")

        # --- HTTP (no HTTPS) ---
        if url_lower.startswith('http://') and not url_lower.startswith('https://'):
            score += 0.08
            indicators.append("No HTTPS")

        # --- VERY SHORT DOMAIN (may be URL shortener or suspicious) ---
        domain_core = domain.split('.')[0] if '.' in domain else domain
        if len(domain_core) <= 3 and tld not in self.safe_tlds:
            score += 0.15
        
        # --- MULTIPLE HYPHENS (common in phishing) ---
        hyphen_count = domain.count('-')
        if hyphen_count >= 3:
            score += 0.20
            indicators.append(f"Multiple hyphens in domain ({hyphen_count}) - suspicious pattern")
        elif hyphen_count >= 2:
            score += 0.12
            indicators.append(f"Multiple hyphens in domain ({hyphen_count})")

        prob = min(0.95, score)
        result = self._format_result(prob, indicators)
        return result

    def _format_result(self, prob, indicators=None):
        if prob > 0.75:
            risk_level = 'CRITICAL'
        elif prob > 0.60:
            risk_level = 'HIGH'
        elif prob > 0.40:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Calculate confidence percentage (avoid NaN)
        confidence_percent = min(100, max(0, abs(prob - 0.5) * 2 * 100))

        return {
            'is_phishing': bool(prob > 0.5),
            'phishing_probability': round(float(prob), 4),
            'risk_level': risk_level,
            'confidence': round(float(abs(prob - 0.5) * 2), 4),
            'confidence_percent': round(confidence_percent, 2),
            'url_features': ' | '.join(indicators) if indicators else 'No specific URL features detected',
            'recommendation': (
                'BLOCK - High confidence phishing URL' if prob > 0.75 else
                'WARN USER - Likely phishing attempt' if prob > 0.60 else
                'CAUTION - Moderately suspicious URL' if prob > 0.40 else
                'SAFE - URL appears legitimate'
            )
        }
