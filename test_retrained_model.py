"""
Test the retrained Fake News Detection model
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_modules.fake_news.predict import FakeNewsDetector

# The exact article from the user's test
test_article = "Eating Garlic Stops All Colds Instantly A viral post claims that eating raw garlic three times a day can prevent and cure all colds instantly. The post includes pictures of celebrities eating garlic."

print("="*70)
print("TESTING RETRAINED FAKE NEWS DETECTOR")
print("="*70)
print(f"\nArticle: {test_article}\n")

try:
    detector = FakeNewsDetector(model_dir='ml_modules/fake_news/models')
    result = detector.predict(test_article, use_ensemble=True)

    print("RESULT:")
    if result['is_fake']:
        print("  Classification: FAKE NEWS")
    else:
        print("  Classification: REAL NEWS")
    
    print(f"  Fake Probability: {result['fake_probability']:.2%}")
    print(f"  Confidence: {result['confidence']}")

    if 'models_used' in result:
        print(f"  Models Used: {', '.join(result['models_used'])}")
        print(f"\n  Individual Predictions:")
        for model, pred in result.get('individual_predictions', {}).items():
            print(f"    - {model}: {pred['probability']:.2%} (weight: {pred['weight']})")

    print("\n" + "="*70)
    if result['is_fake'] and result['fake_probability'] > 0.7:
        print("SUCCESS: Model correctly identified this as FAKE NEWS!")
        print("The retrained model now properly detects medical misinformation.")
    else:
        print("WARNING: Model still needs improvement")
        print(f"Expected: FAKE (>70%), Got: {result['fake_probability']:.2%}")
    print("="*70)
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
