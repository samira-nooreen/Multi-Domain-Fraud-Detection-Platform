
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

errors = []
results = []

# 1. UPI Fraud
try:
    from ml_modules.upi_fraud.predict import UPIFraudDetector
    d = UPIFraudDetector(model_path='ml_modules/upi_fraud/upi_fraud_model.pkl', scaler_path='ml_modules/upi_fraud/upi_fraud_scaler.pkl')
    r = d.predict({'amount': 5000, 'time_of_transaction': '14:30', 'device_changed': 0})
    r2 = d.predict({'amount': 5000, 'time_of_transaction': '02:00', 'device_changed': 1})
    results.append(f"UPI OK: low={r['fraud_probability']:.2f} high={r2['fraud_probability']:.2f} risk_low={r['risk_level']} risk_high={r2['risk_level']}")
except Exception as e:
    errors.append(f"UPI FAIL: {e}")

# 2. Credit Card
try:
    from ml_modules.credit_card.predict import CreditCardFraudDetector
    d = CreditCardFraudDetector(model_path='ml_modules/credit_card/credit_card_model.pkl', scaler_path='ml_modules/credit_card/credit_card_scaler.pkl', features_path='ml_modules/credit_card/credit_card_features.pkl')
    r = d.predict({'amount': 5000, 'transaction_type': 'POS', 'card_present': 1, 'location': 'Mumbai'})
    r2 = d.predict({'amount': 200000, 'transaction_type': 'Online', 'card_present': 0, 'location': 'Unknown'})
    results.append(f"Credit OK: low={r['fraud_probability']:.2f} high={r2['fraud_probability']:.2f}")
except Exception as e:
    errors.append(f"Credit FAIL: {e}")

# 3. Loan Default
try:
    from ml_modules.loan_default.predict import LoanDefaultPredictor
    d = LoanDefaultPredictor(model_path='ml_modules/loan_default/loan_model.pkl')
    r = d.predict({'monthly_income': 50000, 'loan_amount': 100000, 'loan_duration': 24, 'credit_score': 750, 'dti_ratio': 0.2, 'loan_intent': 'PERSONAL', 'person_home_ownership': 'RENT', 'loan_grade': 'A'})
    r2 = d.predict({'monthly_income': 10000, 'loan_amount': 500000, 'loan_duration': 12, 'credit_score': 450, 'dti_ratio': 5.0, 'loan_intent': 'PERSONAL', 'person_home_ownership': 'RENT', 'loan_grade': 'E'})
    results.append(f"Loan OK: low={r['default_probability']:.2f} high={r2['default_probability']:.2f} dec_low={r['decision']} dec_high={r2['decision']}")
except Exception as e:
    errors.append(f"Loan FAIL: {e}")

# 4. Insurance Fraud
try:
    from ml_modules.insurance_fraud.predict import InsuranceFraudDetector
    d = InsuranceFraudDetector()
    r = d.predict({'claim_amount': 5000, 'past_claims': 1, 'policy_tenure': 5, 'policy_amount': 50000, 'days_to_report': 2, 'claim_type': 'accident', 'age': 35})
    r2 = d.predict({'claim_amount': 80000, 'past_claims': 15, 'policy_tenure': 2, 'policy_amount': 50000, 'days_to_report': 45, 'claim_type': 'fire', 'age': 25})
    results.append(f"Insurance OK: low={r['fraud_probability']:.2f} high={r2['fraud_probability']:.2f}")
except Exception as e:
    errors.append(f"Insurance FAIL: {e}")

# 5. Click Fraud
try:
    from ml_modules.click_fraud.predict import ClickFraudDetector
    d = ClickFraudDetector(model_dir='ml_modules/click_fraud')
    normal_seq = [[1.5, 100, 200, 0, 0, 10, 0, 5] for _ in range(10)]
    bot_seq = [[0.05, 100, 200, 0, 0, 10, 0, 5] for _ in range(50)]
    r = d.predict(normal_seq)
    r2 = d.predict(bot_seq)
    results.append(f"Click OK: normal={r['fraud_probability']:.2f} bot={r2['fraud_probability']:.2f}")
except Exception as e:
    errors.append(f"Click FAIL: {e}")

# 6. Fake News
try:
    from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector
    d = DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')
    r = d.analyze_article("Scientists discover new vaccine", "Researchers at MIT published peer-reviewed study showing 95% efficacy.", "reuters")
    r2 = d.analyze_article("SHOCKING TRUTH EXPOSED", "The illuminati deep state new world order is covering up microchips in vaccines wake up sheeple!", "blog")
    results.append(f"FakeNews OK: real={r.get('is_fake')} fake={r2.get('is_fake')}")
except Exception as e:
    errors.append(f"FakeNews FAIL: {e}")

# 7. Spam Email
try:
    from ml_modules.spam_email.predict import SpamDetector
    d = SpamDetector(model_path='ml_modules/spam_email/spam_model.pkl', vec_path='ml_modules/spam_email/spam_vectorizer.pkl')
    r = d.predict("Hello, meeting is scheduled for tomorrow at 3pm.")
    r2 = d.predict("URGENT! You have WON $1,000,000! Click here NOW to claim your prize!")
    results.append(f"Spam OK: ham={r['spam_probability']:.2f} spam={r2['spam_probability']:.2f}")
except Exception as e:
    errors.append(f"Spam FAIL: {e}")

# 8. Phishing URL
try:
    from ml_modules.phishing_url.predict import PhishingDetector
    d = PhishingDetector(model_path='ml_modules/phishing_url/phishing_model.pkl')
    r = d.predict("https://google.com")
    r2 = d.predict("http://paypal-secure-login.verify-account-update.tk/user/confirm?session=abc123&token=xyz789")
    results.append(f"Phishing OK: legit={r['phishing_probability']:.2f} phish={r2['phishing_probability']:.2f}")
except Exception as e:
    errors.append(f"Phishing FAIL: {e}")

# 9. Fake Profile
try:
    from ml_modules.fake_profile.predict import BotDetector
    d = BotDetector(model_dir='ml_modules/fake_profile')
    r = d.predict({'username': 'active_user', 'account_creation_date': '2020-01-01', 'follower_count': 800, 'posts_count': 150})
    r2 = d.predict({'username': 'bot123', 'account_creation_date': '2024-11-01', 'follower_count': 10, 'posts_count': 0})
    results.append(f"FakeProfile OK: real={r['bot_probability']:.2f} bot={r2['bot_probability']:.2f}")
except Exception as e:
    errors.append(f"FakeProfile FAIL: {e}")

# 10. Document Forgery
try:
    from ml_modules.document_forgery.predict import ForgeryDetector
    d = ForgeryDetector(model_path='ml_modules/document_forgery/forgery_model.pkl')
    r = d._mock_predict()
    results.append(f"DocForgery OK: prob={r['forgery_probability']:.2f}")
except Exception as e:
    errors.append(f"DocForgery FAIL: {e}")

# 11. Brand Abuse
try:
    from ml_modules.brand_abuse.predict import BrandAbuseDetector
    d = BrandAbuseDetector(model_path='ml_modules/brand_abuse/brand_abuse_model.pkl')
    r = d.predict({'url': 'https://nike.com/products', 'brand_keywords': ['Nike'], 'seller_name': 'Nike Official Store', 'listing_title': 'Nike Air Max', 'description': 'Authentic Nike shoes'})
    r2 = d.predict({'url': 'https://instagram.com/marketplace', 'brand_keywords': ['Nike'], 'seller_name': 'nike_outlet_official', 'listing_title': '70% OFF Nike same as original', 'description': 'Best copy replica nike same as original oem'})
    results.append(f"BrandAbuse OK: legit={r['abuse_probability']:.2f} abuse={r2['abuse_probability']:.2f}")
except Exception as e:
    errors.append(f"BrandAbuse FAIL: {e}")

print("=== RESULTS ===")
for r in results:
    print(r)
print("\n=== ERRORS ===")
for e in errors:
    print(e)
