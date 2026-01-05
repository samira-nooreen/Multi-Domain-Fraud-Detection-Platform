from ml_modules.fake_news.predict import FakeNewsDetector

detector = FakeNewsDetector(model_dir='ml_modules/fake_news/models')

# Test obvious fake news
fake_text = "SHOCKING: Lemon juice cures all cancer! Doctors HATE this miracle cure that Big Pharma hides!"
result = detector.predict(fake_text)

print(f"Text: {fake_text}")
print(f"Is Fake: {result['is_fake']}")
print(f"Fake Probability: {result['fake_probability']:.2%}")
print(f"Confidence: {result['confidence']}")
if 'models_used' in result:
    print(f"Models: {result['models_used']}")
if 'model_used' in result:
    print(f"Model: {result['model_used']}")
