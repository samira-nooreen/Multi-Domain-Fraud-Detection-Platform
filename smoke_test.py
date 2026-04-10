"""Smoke test: import all modules used by app.py routes and run one prediction each."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

errors = []

tests = [
    ("UPI Fraud", lambda: __import__('ml_modules.upi_fraud.predict', fromlist=['UPIFraudDetector'])
        .UPIFraudDetector('ml_modules/upi_fraud/upi_fraud_model.pkl','ml_modules/upi_fraud/upi_fraud_scaler.pkl')
        .predict({'amount':500,'time_of_transaction':'10:00','device_changed':0})),
    ("Credit Card", lambda: __import__('ml_modules.credit_card.predict', fromlist=['CreditCardFraudDetector'])
        .CreditCardFraudDetector('ml_modules/credit_card/credit_card_model.pkl','ml_modules/credit_card/credit_card_scaler.pkl','ml_modules/credit_card/credit_card_features.pkl')
        .predict({'amount':2000,'transaction_type':'POS','card_present':1,'location':'Mumbai'})),
    ("Loan Default", lambda: __import__('ml_modules.loan_default.predict', fromlist=['LoanDefaultPredictor'])
        .LoanDefaultPredictor('ml_modules/loan_default/loan_model.pkl','ml_modules/loan_default/loan_encoders.pkl')
        .predict({'loan_amount':500000,'annual_income':1200000,'credit_score':780,'employment_length':5,'loan_purpose':'home','debt_to_income':0.2})),
    ("Insurance Fraud", lambda: __import__('ml_modules.insurance_fraud.predict', fromlist=['InsuranceFraudDetector'])
        .InsuranceFraudDetector()
        .predict({'claim_amount':50000,'incident_type':'vehicle_damage','months_as_customer':36})),
    ("Click Fraud", lambda: __import__('ml_modules.click_fraud.predict', fromlist=['ClickFraudDetector'])
        .ClickFraudDetector(model_dir='ml_modules/click_fraud')
        .predict([[2.5,300,200,0,0,14,0,8.0,2.1] for _ in range(5)])),
    ("Fake News", lambda: __import__('ml_modules.fake_news.predict', fromlist=['DJDarkCyberFakeNewsDetector'])
        .DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')
        .analyze_article("RBI raises rate","The Reserve Bank of India raised rates.","reuters")),
    ("Spam Email", lambda: __import__('ml_modules.spam_email.predict', fromlist=['SpamDetector'])
        .SpamDetector(model_path='ml_modules/spam_email/spam_model.pkl',vec_path='ml_modules/spam_email/spam_vectorizer.pkl')
        .predict("Hello, meeting tomorrow at 10am?")),
    ("Phishing URL", lambda: __import__('ml_modules.phishing_url.predict', fromlist=['PhishingDetector'])
        .PhishingDetector()
        .predict("https://www.google.com")),
    ("Fake Profile", lambda: __import__('ml_modules.fake_profile.predict', fromlist=['BotDetector'])
        .BotDetector(model_dir='ml_modules/fake_profile')
        .predict({'username':'john_doe','account_creation_date':'2020-01-01','follower_count':500,'posts_count':80})),
    ("Document Forgery", lambda: __import__('ml_modules.document_forgery.predict', fromlist=['ForgeryDetector'])
        .ForgeryDetector(model_path='ml_modules/document_forgery/forgery_model.pkl')
        .predict()),
    ("Brand Abuse", lambda: __import__('ml_modules.brand_abuse.predict', fromlist=['BrandAbuseDetector'])
        .BrandAbuseDetector(model_path='ml_modules/brand_abuse/brand_abuse_model.pkl')
        .predict({'url':'https://amaz0n-deals.tk','brand_keywords':['amazon'],'listing_title':'Cheap Amazon products'})),
]

print("SMOKE TEST - All 11 modules\n" + "="*50)
passed = failed = 0
for name, fn in tests:
    try:
        result = fn()
        assert isinstance(result, dict), f"Result not a dict: {result}"
        print(f"  [OK] {name}: {list(result.keys())[:4]}")
        passed += 1
    except Exception as e:
        print(f"  [ERR] {name}: {e}")
        failed += 1

print(f"\n{'='*50}")
print(f"PASSED: {passed}/11   FAILED: {failed}/11")
