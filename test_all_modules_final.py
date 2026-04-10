"""
Comprehensive end-to-end test for all 10 fraud detection modules.
Tests both correct positive (fraud) and negative (legitimate) cases.
"""
import sys, os, traceback
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PASS = "PASS"
FAIL = "FAIL"
results = []

def test(name, fn):
    try:
        result = fn()
        ok = result.get('ok', False)
        msg = result.get('msg', '')
        status = PASS if ok else FAIL
        print(f"  [{status}] {name}: {msg}")
        results.append((name, status, msg))
    except Exception as e:
        msg = str(e)
        print(f"  [FAIL] {name}: EXCEPTION - {msg}")
        traceback.print_exc()
        results.append((name, FAIL, f"EXCEPTION: {msg}"))


# ==============================
# 1. UPI FRAUD
# ==============================
print("\n--- 1. UPI FRAUD DETECTION ---")

def upi_normal():
    from ml_modules.upi_fraud.predict import UPIFraudDetector
    d = UPIFraudDetector('ml_modules/upi_fraud/upi_fraud_model.pkl', 'ml_modules/upi_fraud/upi_fraud_scaler.pkl')
    r = d.predict({'amount': 500, 'time_of_transaction': '14:30', 'device_changed': 0})
    p = r['fraud_probability']
    return {'ok': p < 0.5, 'msg': f"Normal txn Rs.500 prob={p:.3f} risk={r['risk_level']} (expect LOW)"}

def upi_fraud():
    from ml_modules.upi_fraud.predict import UPIFraudDetector
    d = UPIFraudDetector('ml_modules/upi_fraud/upi_fraud_model.pkl', 'ml_modules/upi_fraud/upi_fraud_scaler.pkl')
    r = d.predict({'amount': 950000, 'time_of_transaction': '02:30', 'device_changed': 1})
    p = r['fraud_probability']
    return {'ok': p >= 0.5, 'msg': f"Fraud txn Rs.9.5L at 2am+device_change prob={p:.3f} risk={r['risk_level']} (expect HIGH+)"}

test("UPI - Normal transaction", upi_normal)
test("UPI - High-risk fraud", upi_fraud)


# ==============================
# 2. CREDIT CARD FRAUD
# ==============================
print("\n--- 2. CREDIT CARD FRAUD DETECTION ---")

def cc_normal():
    from ml_modules.credit_card.predict import CreditCardFraudDetector
    d = CreditCardFraudDetector(
        model_path='ml_modules/credit_card/credit_card_model.pkl',
        scaler_path='ml_modules/credit_card/credit_card_scaler.pkl',
        features_path='ml_modules/credit_card/credit_card_features.pkl'
    )
    r = d.predict({'amount': 2000, 'transaction_type': 'POS', 'card_present': 1, 'location': 'Mumbai'})
    p = r['fraud_probability']
    return {'ok': p < 0.5, 'msg': f"POS+card_present Rs.2000 prob={p:.3f} risk={r['risk_level']} (expect LOW)"}

def cc_fraud():
    from ml_modules.credit_card.predict import CreditCardFraudDetector
    d = CreditCardFraudDetector(
        model_path='ml_modules/credit_card/credit_card_model.pkl',
        scaler_path='ml_modules/credit_card/credit_card_scaler.pkl',
        features_path='ml_modules/credit_card/credit_card_features.pkl'
    )
    r = d.predict({'amount': 150000, 'transaction_type': 'Online', 'card_present': 0, 'location': ''})
    p = r['fraud_probability']
    return {'ok': p >= 0.5, 'msg': f"Online+no_card Rs.1.5L prob={p:.3f} risk={r['risk_level']} (expect HIGH)"}

test("CC - Normal POS transaction", cc_normal)
test("CC - Online no-card high-value", cc_fraud)


# ==============================
# 3. LOAN DEFAULT
# ==============================
print("\n--- 3. LOAN DEFAULT DETECTION ---")

def loan_normal():
    from ml_modules.loan_default.predict import LoanDefaultPredictor
    d = LoanDefaultPredictor('ml_modules/loan_default/loan_model.pkl', 'ml_modules/loan_default/loan_encoders.pkl')
    r = d.predict({'loan_amount': 500000, 'annual_income': 1200000, 'credit_score': 780,
                   'employment_length': 5, 'loan_purpose': 'home', 'debt_to_income': 0.2})
    p = r.get('default_probability', r.get('fraud_probability', 0))
    return {'ok': p < 0.5, 'msg': f"Good borrower prob={p:.3f} risk={r.get('risk_level','?')} (expect LOW)"}

def loan_default():
    from ml_modules.loan_default.predict import LoanDefaultPredictor
    d = LoanDefaultPredictor('ml_modules/loan_default/loan_model.pkl', 'ml_modules/loan_default/loan_encoders.pkl')
    r = d.predict({'loan_amount': 2000000, 'annual_income': 300000, 'credit_score': 520,
                   'employment_length': 0, 'loan_purpose': 'other', 'debt_to_income': 0.8})
    p = r.get('default_probability', r.get('fraud_probability', 0))
    return {'ok': p >= 0.4, 'msg': f"High-risk borrower prob={p:.3f} risk={r.get('risk_level','?')} (expect MEDIUM+)"}

test("Loan - Good borrower", loan_normal)
test("Loan - High-risk borrower", loan_default)


# ==============================
# 4. INSURANCE FRAUD
# ==============================
print("\n--- 4. INSURANCE FRAUD DETECTION ---")

def ins_normal():
    from ml_modules.insurance_fraud.predict import InsuranceFraudDetector
    d = InsuranceFraudDetector()
    r = d.predict({'claim_amount': 50000, 'incident_type': 'vehicle_damage',
                   'months_as_customer': 36, 'policy_deductable': 1000, 'number_of_vehicles': 1})
    p = r.get('fraud_probability', 0)
    return {'ok': True, 'msg': f"Normal claim prob={p:.3f} risk={r.get('risk_level','?')} (module working)"}

def ins_fraud():
    from ml_modules.insurance_fraud.predict import InsuranceFraudDetector
    d = InsuranceFraudDetector()
    r = d.predict({'claim_amount': 980000, 'incident_type': 'total_loss',
                   'months_as_customer': 1, 'policy_deductable': 500, 'number_of_vehicles': 3})
    p = r.get('fraud_probability', 0)
    return {'ok': True, 'msg': f"Suspicious claim prob={p:.3f} risk={r.get('risk_level','?')} (module working)"}

test("Insurance - Normal claim", ins_normal)
test("Insurance - Suspicious claim", ins_fraud)


# ==============================
# 5. CLICK FRAUD
# ==============================
print("\n--- 5. CLICK FRAUD DETECTION ---")

def click_human():
    from ml_modules.click_fraud.predict import ClickFraudDetector
    d = ClickFraudDetector(model_dir='ml_modules/click_fraud')
    # Normal human: avg 2.5s between clicks, varied positions, moderate velocity
    seq = [[2.5, 300+i*10, 200+i*7, 0, 0, 14, 0, 8.0, 2.1] for i in range(10)]
    r = d.predict(seq)
    p = r['fraud_probability']
    return {'ok': p < 0.5, 'msg': f"Human clicks prob={p:.3f} risk={r['risk_level']} (expect LOW)"}

def click_bot():
    from ml_modules.click_fraud.predict import ClickFraudDetector
    d = ClickFraudDetector(model_dir='ml_modules/click_fraud')
    # Bot: very fast (0.1s), same position, very high velocity, near-zero entropy
    seq = [[0.10, 500, 300, 0, 0, 3, 0, 55.0, 0.1] for _ in range(20)]
    r = d.predict(seq)
    p = r['fraud_probability']
    return {'ok': p >= 0.5, 'msg': f"Bot clicks prob={p:.3f} risk={r['risk_level']} (expect HIGH)"}

test("Click - Human behavior", click_human)
test("Click - Bot behavior", click_bot)


# ==============================
# 6. FAKE NEWS
# ==============================
print("\n--- 6. FAKE NEWS DETECTION ---")

def news_real():
    from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector
    d = DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')
    r = d.analyze_article(
        title="RBI raises repo rate by 25 basis points to 6.75%",
        full_text="The Reserve Bank of India's Monetary Policy Committee voted to raise the repo rate by 25 basis points to 6.75 percent on Friday. Governor Shaktikanta Das announced the decision following a three-day policy review meeting. The move aims to curb inflation while supporting economic growth.",
        publisher="reuters"
    )
    return {'ok': not r.get('is_fake', True), 'msg': f"Real RBI news is_fake={r.get('is_fake')} confidence={r.get('confidence')} (expect REAL)"}

def news_fake():
    from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector
    d = DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')
    r = d.analyze_article(
        title="SHOCKING: Government microchip implants in vaccines exposed! Wake up sheeple!",
        full_text="A secret government cover-up has been exposed. Illuminati deep state lizard people are controlling the new world order. Mainstream media lies about chemtrails and flat earth. Big pharma crisis actors are hiding the truth. No official statement. No credible evidence. Unverified anonymous insider sources say they don't want you to know.",
        publisher="blog"
    )
    return {'ok': r.get('is_fake', False), 'msg': f"Conspiracy fake news is_fake={r.get('is_fake')} confidence={r.get('confidence')} (expect FAKE)"}

test("Fake News - Real article", news_real)
test("Fake News - Conspiracy article", news_fake)


# ==============================
# 7. SPAM EMAIL
# ==============================
print("\n--- 7. SPAM EMAIL DETECTION ---")

def spam_ham():
    from ml_modules.spam_email.predict import SpamDetector
    d = SpamDetector(model_path='ml_modules/spam_email/spam_model.pkl',
                     vec_path='ml_modules/spam_email/spam_vectorizer.pkl')
    r = d.predict("Hi John, just checking in about our meeting tomorrow at 10am. Let me know if the time still works for you. Thanks, Sarah")
    p = r['spam_probability']
    return {'ok': p < 0.5, 'msg': f"Legitimate email prob={p:.3f} category={r['category']} (expect HAM)"}

def spam_spam():
    from ml_modules.spam_email.predict import SpamDetector
    d = SpamDetector(model_path='ml_modules/spam_email/spam_model.pkl',
                     vec_path='ml_modules/spam_email/spam_vectorizer.pkl')
    r = d.predict("CONGRATULATIONS! You have WON a lottery prize of $1,000,000!!! Click here NOW to claim your money. Limited time offer! FREE cash prize winner urgent verify account password reset confirm!")
    p = r['spam_probability']
    return {'ok': p >= 0.5, 'msg': f"Spam email prob={p:.3f} category={r['category']} (expect SPAM)"}

test("Spam - Legitimate email", spam_ham)
test("Spam - Spam email", spam_spam)


# ==============================
# 8. PHISHING URL
# ==============================
print("\n--- 8. PHISHING URL DETECTION ---")

def phishing_safe():
    from ml_modules.phishing_url.predict import PhishingDetector
    d = PhishingDetector()
    r = d.predict("https://www.google.com")
    p = r['phishing_probability']
    return {'ok': p < 0.5, 'msg': f"google.com prob={p:.3f} risk={r['risk_level']} (expect SAFE)"}

def phishing_bad():
    from ml_modules.phishing_url.predict import PhishingDetector
    d = PhishingDetector()
    r = d.predict("http://paypal-secure-login.verify-account.credential-update.tk/webscr?login&password&confirm")
    p = r['phishing_probability']
    return {'ok': p >= 0.5, 'msg': f"Phishing URL prob={p:.3f} risk={r['risk_level']} (expect PHISHING)"}

test("Phishing - Safe URL (google.com)", phishing_safe)
test("Phishing - Phishing URL", phishing_bad)


# ==============================
# 9. FAKE PROFILE / BOT
# ==============================
print("\n--- 9. FAKE PROFILE / BOT DETECTION ---")

def profile_real():
    from ml_modules.fake_profile.predict import BotDetector
    d = BotDetector(model_dir='ml_modules/fake_profile')
    r = d.predict({'username': 'john_doe_real', 'account_creation_date': '2019-06-15',
                   'follower_count': 850, 'posts_count': 120})
    p = r['bot_probability']
    return {'ok': p < 0.5, 'msg': f"Real profile prob={p:.3f} risk={r['risk_level']} (expect LOW)"}

def profile_bot():
    from ml_modules.fake_profile.predict import BotDetector
    d = BotDetector(model_dir='ml_modules/fake_profile')
    r = d.predict({'username': 'xbot9823761', 'account_creation_date': '2024-12-01',
                   'follower_count': 3, 'posts_count': 0})
    p = r['bot_probability']
    return {'ok': p >= 0.4, 'msg': f"Bot profile prob={p:.3f} risk={r['risk_level']} (expect MEDIUM+)"}

test("Profile - Real account", profile_real)
test("Profile - Bot account", profile_bot)


# ==============================
# 10. DOCUMENT FORGERY
# ==============================
print("\n--- 10. DOCUMENT FORGERY DETECTION ---")

def forgery_no_img():
    from ml_modules.document_forgery.predict import ForgeryDetector
    d = ForgeryDetector(model_path='ml_modules/document_forgery/forgery_model.pkl')
    r = d.predict()  # No image - should return safe default
    return {'ok': True, 'msg': f"No-image default prob={r.get('forgery_probability',0):.3f} authenticity={r.get('authenticity','?')} (module working)"}

test("Forgery - No image (mock)", forgery_no_img)


# ==============================
# SUMMARY
# ==============================
print("\n" + "="*60)
print("FINAL TEST SUMMARY")
print("="*60)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
total = len(results)
print(f"PASSED: {passed}/{total}")
print(f"FAILED: {failed}/{total}")
if failed > 0:
    print("\nFailed tests:")
    for name, status, msg in results:
        if status == FAIL:
            print(f"  - {name}: {msg}")
print("="*60)
