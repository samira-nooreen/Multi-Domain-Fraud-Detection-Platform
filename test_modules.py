import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("TESTING ALL ML MODULES")
print("="*60)

# 1. UPI Fraud
print("\n--- UPI Fraud ---")
try:
    from ml_modules.upi_fraud.predict import UPIFraudDetector
    d = UPIFraudDetector()
    # Test low risk (small normal transaction)
    r = d.predict({'amount': 100, 'transaction_type': 'P2P', 'time_of_day': 'afternoon'})
    print(f"  Low risk test (Rs100 P2P afternoon): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
    # Test high risk (huge amount at night)
    r = d.predict({'amount': 2000000, 'transaction_type': 'P2P', 'time_of_day': 'night'})
    print(f"  High risk test (Rs20L P2P night): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2. Credit Card
print("\n--- Credit Card ---")
try:
    from ml_modules.credit_card.predict import CreditCardFraudDetector
    d = CreditCardFraudDetector()
    r = d.predict({'amount': 50, 'transaction_type': 'online', 'merchant_category': 'grocery', 'time_of_day': 'afternoon', 'currency': 'INR'})
    print(f"  Low risk test (Rs50 grocery): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
    r = d.predict({'amount': 500000, 'transaction_type': 'international', 'merchant_category': 'electronics', 'time_of_day': 'night', 'currency': 'USD'})
    print(f"  High risk test ($500K intl electronics night): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. Loan Default
print("\n--- Loan Default ---")
try:
    from ml_modules.loan_default.predict import LoanDefaultPredictor
    d = LoanDefaultPredictor()
    r = d.predict({'income': 100000, 'loan_amount': 50000, 'credit_score': 800, 'employment_years': 10, 'existing_loans': 0})
    print(f"  Low risk test (high income, good credit): default_prob={r.get('default_probability')}, risk={r.get('risk_level')}")
    r = d.predict({'income': 20000, 'loan_amount': 500000, 'credit_score': 400, 'employment_years': 0, 'existing_loans': 5})
    print(f"  High risk test (low income, bad credit): default_prob={r.get('default_probability')}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 4. Insurance Fraud
print("\n--- Insurance Fraud ---")
try:
    from ml_modules.insurance_fraud.predict import InsuranceFraudDetector
    d = InsuranceFraudDetector()
    r = d.predict({'claim_amount': 5000, 'policy_age_months': 36, 'claim_type': 'accident', 'previous_claims': 0})
    print(f"  Low risk test (small claim, old policy): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
    r = d.predict({'claim_amount': 1000000, 'policy_age_months': 2, 'claim_type': 'theft', 'previous_claims': 5})
    print(f"  High risk test (huge claim, new policy): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 5. Click Fraud
print("\n--- Click Fraud ---")
try:
    from ml_modules.click_fraud.predict import ClickFraudDetector
    d = ClickFraudDetector()
    r = d.predict({'ip_address': '192.168.1.1', 'clicks_per_minute': 2, 'session_duration': 300, 'unique_pages': 5})
    print(f"  Low risk test (normal browsing): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
    r = d.predict({'ip_address': '10.0.0.1', 'clicks_per_minute': 100, 'session_duration': 5, 'unique_pages': 1})
    print(f"  High risk test (bot-like clicks): fraud_prob={r.get('fraud_probability')}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 6. Fake News
print("\n--- Fake News ---")
try:
    from ml_modules.fake_news.predict import FakeNewsDetector
    d = FakeNewsDetector()
    r = d.predict({'text': 'The government announced a new policy today in parliament.', 'source': 'Reuters'})
    print(f"  Low risk test (normal news): result keys={list(r.keys())}")
    print(f"    fake_prob={r.get('fake_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'text': 'SHOCKING!!! You wont BELIEVE what happened!! Click here NOW!!', 'source': 'unknown_blog'})
    print(f"  High risk test (clickbait): fake_prob={r.get('fake_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 7. Spam Email
print("\n--- Spam Email ---")
try:
    from ml_modules.spam_email.predict import SpamEmailDetector
    d = SpamEmailDetector()
    r = d.predict({'subject': 'Meeting tomorrow at 3pm', 'body': 'Hi team, please join the meeting tomorrow.', 'sender': 'boss@company.com'})
    print(f"  Low risk test (normal email): result keys={list(r.keys())}")
    print(f"    spam_prob={r.get('spam_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'subject': 'YOU WON $1000000!!!', 'body': 'Click here to claim your prize now! Act fast!', 'sender': 'winner@free-money.xyz'})
    print(f"  High risk test (spam email): spam_prob={r.get('spam_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 8. Phishing URL
print("\n--- Phishing URL ---")
try:
    from ml_modules.phishing_url.predict import PhishingURLDetector
    d = PhishingURLDetector()
    r = d.predict({'url': 'https://www.google.com'})
    print(f"  Low risk test (google.com): result keys={list(r.keys())}")
    print(f"    phishing_prob={r.get('phishing_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'url': 'http://g00gle-login.suspicious-site.xyz/verify-account.php?id=12345'})
    print(f"  High risk test (phishing URL): phishing_prob={r.get('phishing_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 9. Fake Profile
print("\n--- Fake Profile ---")
try:
    from ml_modules.fake_profile.predict import FakeProfileDetector
    d = FakeProfileDetector()
    r = d.predict({'username': 'john_smith', 'followers': 500, 'following': 300, 'posts': 150, 'account_age_days': 1000, 'bio': 'Software developer from NYC'})
    print(f"  Low risk test (normal profile): result keys={list(r.keys())}")
    print(f"    fake_prob={r.get('fake_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'username': 'xXx_free_money_xXx', 'followers': 50000, 'following': 1, 'posts': 0, 'account_age_days': 2, 'bio': ''})
    print(f"  High risk test (fake profile): fake_prob={r.get('fake_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 10. Document Forgery
print("\n--- Document Forgery ---")
try:
    from ml_modules.document_forgery.predict import DocumentForgeryDetector
    d = DocumentForgeryDetector()
    r = d.predict({'document_type': 'passport', 'text_consistency': 0.95, 'image_quality': 0.9, 'metadata_score': 0.85})
    print(f"  Low risk test (good doc): result keys={list(r.keys())}")
    print(f"    forgery_prob={r.get('forgery_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'document_type': 'id_card', 'text_consistency': 0.2, 'image_quality': 0.3, 'metadata_score': 0.1})
    print(f"  High risk test (bad doc): forgery_prob={r.get('forgery_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 11. Brand Abuse
print("\n--- Brand Abuse ---")
try:
    from ml_modules.brand_abuse.predict import BrandAbuseDetector
    d = BrandAbuseDetector()
    r = d.predict({'url': 'https://www.amazon.com', 'brand_name': 'Amazon'})
    print(f"  Low risk test (real site): result keys={list(r.keys())}")
    print(f"    abuse_prob={r.get('abuse_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
    r = d.predict({'url': 'http://amaz0n-deals.xyz/free-gift', 'brand_name': 'Amazon'})
    print(f"  High risk test (fake site): abuse_prob={r.get('abuse_probability', r.get('fraud_probability'))}, risk={r.get('risk_level')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "="*60)
print("TESTING COMPLETE")
print("="*60)
