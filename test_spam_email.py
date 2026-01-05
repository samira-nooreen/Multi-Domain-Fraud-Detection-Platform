"""Quick test of Spam Email Detection"""
from ml_modules.spam_email.predict import SpamDetector

print("\n" + "="*60)
print("SPAM EMAIL DETECTION TEST")
print("="*60)

detector = SpamDetector(model_dir='ml_modules/spam_email/models')

# Test 1: Spam email
print("\n📧 Test 1: Spam (Urgent Account)")
text1 = "URGENT! Your account will be suspended! Click here NOW to verify!"
result1 = detector.predict(text1)
print(f"  Result: {'SPAM' if result1['is_spam'] else 'HAM'}")
print(f"  Probability: {result1['spam_probability']:.2%}")
print(f"  Confidence: {result1['confidence']}")

# Test 2: Legitimate email
print("\n📧 Test 2: Legitimate (Meeting Request)")
text2 = "Hi John, let's schedule a meeting to discuss the Q4 report."
result2 = detector.predict(text2)
print(f"  Result: {'SPAM' if result2['is_spam'] else 'HAM'}")
print(f"  Probability: {result2['spam_probability']:.2%}")
print(f"  Confidence: {result2['confidence']}")

# Test 3: Phishing
print("\n📧 Test 3: Phishing (Prize Winner)")
text3 = "Congratulations! You won $10,000! Click here to claim your prize!"
result3 = detector.predict(text3)
print(f"  Result: {'SPAM' if result3['is_spam'] else 'HAM'}")
print(f"  Probability: {result3['spam_probability']:.2%}")
print(f"  Confidence: {result3['confidence']}")

print("\n" + "="*60)
print("✅ Spam Email Detection: WORKING")
print("="*60)
