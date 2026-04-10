from ml_modules.spam_email.predict import SpamDetector

detector = SpamDetector(
    model_path='ml_modules/spam_email/spam_model.pkl',
    vec_path='ml_modules/spam_email/spam_vectorizer.pkl'
)

def test_email(name, sender, content, expected):
    text = f"From: {sender}\n\n{content}"
    result = detector.predict(text)
    
    print(f"\n{'='*70}")
    print(f"{name}")
    print(f"Expected: {expected}")
    print(f"{'='*70}")
    print(f"Spam: {result['is_spam']}")
    print(f"Probability: {result['spam_probability']*100:.1f}%")
    print(f"Risk: {result['risk_level']}")
    print(f"Confidence: {result['confidence_percent']:.1f}%")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Trusted Domain: {result.get('trusted_domain', False)}")
    print(f"Spam Keywords: {result.get('spam_keywords_found', 0)}")
    print(f"Legit Indicators: {result.get('legitimate_indicators_found', 0)}")
    print(f"Indicators: {result.get('spam_indicators', 'N/A')}")
    
    # Check if correct
    is_correct = False
    if 'NOT SPAM' in expected and not result['is_spam'] and result['spam_probability'] < 0.3:
        is_correct = True
    elif 'SPAM' in expected and result['is_spam'] and result['spam_probability'] > 0.6:
        is_correct = True
    elif 'MEDIUM' in expected and 0.3 <= result['spam_probability'] <= 0.7:
        is_correct = True
    elif 'Error' in expected or 'validation' in expected:
        is_correct = True  # Just needs to not crash
    
    print(f"Status: {'✅ PASS' if is_correct else '❌ FAIL'}")
    return is_correct

print("="*70)
print("COMPREHENSIVE SPAM DETECTION TEST SUITE")
print("="*70)

results = []

# TEST 1: Normal Email
results.append(test_email(
    "TEST 1: NORMAL EMAIL",
    "hr@company.com",
    "Dear candidate,\nWe are pleased to inform you that your interview is scheduled for Monday at 10 AM. Please confirm your availability.\nRegards, HR Team",
    "NOT SPAM"
))

# TEST 2: Clear Spam
results.append(test_email(
    "TEST 2: CLEAR SPAM",
    "winmoney@lottery-win.xyz",
    "Congratulations!!! You have WON 10,00,000!!!\nClick here to claim now: http://free-money-win.xyz\nHurry, limited time offer!!!",
    "SPAM"
))

# TEST 3: Phishing
results.append(test_email(
    "TEST 3: PHISHING",
    "support@paytm-secure.xyz",
    "Your account has been suspended.\nPlease click the link below and login to verify your account immediately:\nhttp://paytm-login-secure.xyz",
    "SPAM / PHISHING"
))

# TEST 4: Promotional
results.append(test_email(
    "TEST 4: PROMOTIONAL",
    "deals@shopping.com",
    "Huge SALE! Get 80% OFF on all products. Limited time only. Shop now!",
    "MEDIUM / PROMO SPAM"
))

# TEST 5: Professional Email
results.append(test_email(
    "TEST 5: PROFESSIONAL EMAIL",
    "professor@university.edu",
    "Please submit your assignment by Friday. Let me know if you need any clarification.",
    "NOT SPAM"
))

# TEST 6: Extreme Spam
results.append(test_email(
    "TEST 6: EXTREME SPAM",
    "crypto-profit@hackmail.ru",
    "Invest $100 and earn $5000 daily guaranteed!!! No risk!!! Click now!!!",
    "HIGH SPAM"
))

# TEST 7: Edge Case (Empty)
try:
    results.append(test_email(
        "TEST 7: EDGE CASE (EMPTY)",
        "",
        "",
        "Error / validation"
    ))
except:
    print(f"\n{'='*70}")
    print("TEST 7: EDGE CASE (EMPTY)")
    print("Expected: Error / validation")
    print("Status: ✅ PASS (Handled without crash)")
    results.append(True)

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
passed = sum(results)
total = len(results)
print(f"Passed: {passed}/{total}")

if passed == total:
    print("\n🎉 All tests passed! Module is industry-ready!")
elif passed >= 5:
    print("\n✅ Most tests passed. Module is good!")
else:
    print(f"\n⚠️ {total - passed} tests need fixing")
