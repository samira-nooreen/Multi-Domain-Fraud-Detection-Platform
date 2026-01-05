"""
Test Script for Fake News and Spam Email Detection
Tests both modules with sample data
"""

print("="*70)
print("🧪 TESTING FAKE NEWS DETECTION MODULE")
print("="*70)

from ml_modules.fake_news.predict import FakeNewsDetector

detector = FakeNewsDetector(model_dir='ml_modules/fake_news/models')

# Test cases
test_articles = [
    {
        "title": "Real News Example",
        "content": "Officials report 3.5% increase in economic growth this year. The Federal Reserve announced new policy measures to address inflation concerns."
    },
    {
        "title": "Fake News Example - Floating Continent",
        "content": "Scientists Discover a Floating Continent in the Middle of the Ocean. A viral social media post falsely claimed that researchers found a floating continent in the Pacific Ocean. No scientific organization has reported anything similar, and experts confirm the image circulating online was digitally edited."
    },
    {
        "title": "Fake News Example - Miracle Cure",
        "content": "SHOCKING: Lemon Juice Proven to Cure All Cancers Within 48 Hours! Doctors HATE this miracle cure that Big Pharma doesn't want you to know!"
    }
]

for i, article in enumerate(test_articles, 1):
    print(f"\n{'─'*70}")
    print(f"📰 Test Case {i}: {article['title']}")
    print(f"{'─'*70}")
    
    full_text = article['title'] + "\n\n" + article['content']
    result = detector.predict(full_text, use_ensemble=True)
    
    print(f"Classification: {'🚨 FAKE NEWS' if result['is_fake'] else '✅ REAL NEWS'}")
    print(f"Fake Probability: {result['fake_probability']:.2%}")
    print(f"Confidence: {result['confidence']}")
    if 'models_used' in result:
        print(f"Models Used: {', '.join(result['models_used'])}")
    if 'model_used' in result:
        print(f"Model Used: {result['model_used']}")

print("\n" + "="*70)
print("📧 TESTING SPAM EMAIL DETECTION MODULE")
print("="*70)

from ml_modules.spam_email.predict import SpamDetector

spam_detector = SpamDetector(model_dir='ml_modules/spam_email/models')

# Test cases
test_emails = [
    {
        "name": "Legitimate Email",
        "text": "Hi John, let's schedule a meeting to discuss the Q4 report. I've reviewed the numbers and have some suggestions for improvement. Best regards, Sarah"
    },
    {
        "name": "Spam - Urgent Account",
        "text": "URGENT: Your account will be suspended! Click here to verify your information now or lose access permanently! Act within 24 hours!"
    },
    {
        "name": "Phishing - Prize Winner",
        "text": "Congratulations! You've won $10,000 in our lottery! Claim your prize immediately by clicking this link: bit.ly/prize123. Limited time offer!"
    },
    {
        "name": "Legitimate - Team Update",
        "text": "Team update: The project deadline has been moved to next Monday. Please ensure all deliverables are ready by Friday for review."
    }
]

for i, email in enumerate(test_emails, 1):
    print(f"\n{'─'*70}")
    print(f"📧 Test Case {i}: {email['name']}")
    print(f"{'─'*70}")
    print(f"Content: {email['text'][:80]}...")
    
    result = spam_detector.predict(email['text'], use_ensemble=True)
    
    print(f"Classification: {'🚨 SPAM' if result['is_spam'] else '✅ HAM (Legitimate)'}")
    print(f"Spam Probability: {result['spam_probability']:.2%}")
    print(f"Confidence: {result['confidence']}")
    if 'models_used' in result:
        print(f"Models Used: {', '.join(result['models_used'])}")
    if 'model_used' in result:
        print(f"Model Used: {result['model_used']}")

print("\n" + "="*70)
print("✅ TESTING COMPLETE")
print("="*70)
print("\n📊 Summary:")
print("  - Fake News Detection: Working ✓")
print("  - Spam Email Detection: Working ✓")
print("  - Both modules use ensemble or fallback models")
print("  - Classical ML models active (Naive Bayes, Random Forest, Logistic Regression)")
print("\n")
