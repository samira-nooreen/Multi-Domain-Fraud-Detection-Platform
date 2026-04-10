from ml_modules.spam_email.predict import SpamDetector

detector = SpamDetector(
    model_path='ml_modules/spam_email/spam_model.pkl',
    vec_path='ml_modules/spam_email/spam_vectorizer.pkl'
)

# Test legitimate email
text1 = "From: professor@university.edu\n\nPlease submit your assignment by Friday. Let me know if you need any clarification."
result1 = detector.predict(text1)

print("="*70)
print("TEST 1: LEGITIMATE EMAIL")
print("="*70)
print(f"Spam: {result1['is_spam']}")
print(f"Probability: {result1['spam_probability']*100:.1f}%")
print(f"Risk: {result1['risk_level']}")
print(f"Confidence: {result1['confidence_percent']:.1f}%")
print(f"Recommendation: {result1['recommendation']}")
print(f"Indicators: {result1.get('spam_indicators', 'N/A')}")

# Test spam email
text2 = "From: winner@free-money.xyz\n\nCONGRATULATIONS! You've won $1,000,000! Click here NOW to claim your prize! Limited time offer! Act fast!"
result2 = detector.predict(text2)

print(f"\n{'='*70}")
print("TEST 2: SPAM EMAIL")
print("="*70)
print(f"Spam: {result2['is_spam']}")
print(f"Probability: {result2['spam_probability']*100:.1f}%")
print(f"Risk: {result2['risk_level']}")
print(f"Confidence: {result2['confidence_percent']:.1f}%")
print(f"Recommendation: {result2['recommendation']}")
print(f"Indicators: {result2.get('spam_indicators', 'N/A')}")
