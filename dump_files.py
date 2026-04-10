
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'app.py',
    'ml_modules/upi_fraud/predict.py',
    'ml_modules/credit_card/predict.py',
    'ml_modules/loan_default/predict.py',
    'ml_modules/insurance_fraud/predict.py',
    'ml_modules/click_fraud/predict.py',
    'ml_modules/fake_news/predict.py',
    'ml_modules/spam_email/predict.py',
    'ml_modules/phishing_url/predict.py',
    'ml_modules/fake_profile/predict.py',
    'ml_modules/document_forgery/predict.py',
]

for f in files:
    print(f"\n{'='*60}")
    print(f"FILE: {f}")
    print('='*60)
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            print(fh.read())
    except Exception as e:
        print(f"ERROR: {e}")
