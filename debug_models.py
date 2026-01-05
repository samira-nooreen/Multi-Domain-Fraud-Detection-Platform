"""Debug script to check model predictions"""
from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector
import pickle
import sys
import os

# Redirect output to file
log_file = open('debug_results.log', 'w', encoding='utf-8')
sys.stdout = log_file

print("="*70)
print("DEBUGGING FAKE NEWS MODELS")
print("="*70)

try:
    detector = DJDarkCyberFakeNewsDetector(model_dir='ml_modules/fake_news/models')
    print("✅ Detector initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize detector: {e}")
    sys.exit(1)

# Test cases
test_cases = [
    ("REAL", "Officials report 3.5% increase in economic growth this year."),
    ("FAKE", "SHOCKING: Lemon juice cures all cancer! Doctors HATE this!"),
    ("FAKE", "You won't BELIEVE what this celebrity did - SHOCKING!"),
    ("FAKE", "Secret cure for diabetes that Big Pharma doesn't want you to know!"),
    ("REAL", "Scientists at MIT publish research on renewable energy."),
]

print("\nTesting individual models:\n")

for expected, text in test_cases:
    print(f"\n{'-'*70}")
    print(f"Expected: {expected}")
    print(f"Text: {text[:60]}...")
    print(f"{'-'*70}")
    
    # Test Detector
    try:
        result = detector.analyze_article(title="", full_text=text)
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Is Fake: {result['is_fake']}")
        print(f"Source Analysis: {result['source_analysis']}")
        
        # Check if correct
        is_correct = (expected == "FAKE" and result['is_fake']) or (expected == "REAL" and not result['is_fake'])
        print(f"Result: {'CORRECT' if is_correct else 'WRONG'}")
    except Exception as e:
        print(f"Error during prediction: {e}")

# Check model files
print("\n" + "="*70)
print("CHECKING MODEL FILES")
print("="*70)

try:
    with open('ml_modules/fake_news/models/nb_model.pkl', 'rb') as f:
        nb_model = pickle.load(f)
    print(f"Naive Bayes model loaded")
    # print(f"  Type: {type(nb_model)}")
except Exception as e:
    print(f"Error loading NB model: {e}")

log_file.close()
