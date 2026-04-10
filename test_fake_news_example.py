from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector

detector = DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')

# Test the exact fake news example
title = ""
text = "Scientists have confirmed that drinking 5 liters of hot water daily can completely cure cancer within 2 weeks. This method is being hidden by pharmaceutical companies."
source = "https://fakehealthnews.xyz"

result = detector.analyze_article(
    title=title,
    full_text=text,
    publisher=source
)

print("="*70)
print("FAKE NEWS DETECTION TEST")
print("="*70)
print(f"\nInput Text: {text[:80]}...")
print(f"Source: {source}")
print(f"\n{'='*70}")
print(f"RESULTS:")
print(f"{'='*70}")
print(f"Prediction: {result['prediction']}")
print(f"Is Fake: {result['is_fake']}")
print(f"Fake Probability: {result['fake_probability']*100:.1f}%")
print(f"Credibility Score: {result.get('credibility_score', 'NaN')}%")
print(f"Confidence: {result.get('confidence_percent', 'NaN')}%")
print(f"Risk Level: {result.get('risk_level', 'N/A')}")
print(f"\nDetailed Analysis:")
print(f"  {result.get('detailed_analysis', 'N/A')}")
print(f"\nRecommendation:")
if result['is_fake']:
    print(f"  ⚠️ WARNING: This article contains fake news indicators. Do not share without verification.")
else:
    print(f"  ✅ No action required. Article appears authentic.")

print(f"\n{'='*70}")
if result['is_fake'] and result['fake_probability'] > 0.7:
    print("✅ CORRECT - Fake news properly detected!")
else:
    print(f"❌ WRONG - Should be FAKE with high probability")
