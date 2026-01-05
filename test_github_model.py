import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_modules', 'fake_profile'))

from ml_modules.fake_profile.predict import BotDetector

def test_real_profiles():
    print("\n=== Testing Real User Profiles with New Model ===\n")
    
    detector = BotDetector(model_dir='ml_modules/fake_profile')
    
    # Test Case 1: @_.sammu._01 (Original)
    print("--- Test 1: @_.sammu._01 ---")
    user1 = {
        'followers': 390,
        'following': 566,
        'posts': 0,
        'favourites_count': 0,
        'listed_count': 0
    }
    result1 = detector.predict(user1)
    print(f"Input: {user1}")
    print(f"Prediction: {'BOT/FAKE' if result1['is_bot'] else 'GENUINE/HUMAN'}")
    print(f"Fake Probability: {result1['bot_probability']*100:.2f}%")
    print(f"Genuine Probability: {(1-result1['bot_probability'])*100:.2f}%")
    print(f"Confidence: {result1['confidence']}\n")
    
    # Test Case 2: @-.sammu._02 (3 years old)
    print("--- Test 2: @-.sammu._02 (3 years old) ---")
    user2 = {
        'followers': 390,
        'following': 566,
        'posts': 0,
        'favourites_count': 0,
        'listed_count': 0
    }
    result2 = detector.predict(user2)
    print(f"Input: {user2}")
    print(f"Prediction: {'BOT/FAKE' if result2['is_bot'] else 'GENUINE/HUMAN'}")
    print(f"Fake Probability: {result2['bot_probability']*100:.2f}%")
    print(f"Genuine Probability: {(1-result2['bot_probability'])*100:.2f}%")
    print(f"Confidence: {result2['confidence']}\n")
    
    # Test Case 3: Active genuine user
    print("--- Test 3: Active Genuine User ---")
    user3 = {
        'followers': 800,
        'following': 400,
        'posts': 500,
        'favourites_count': 300,
        'listed_count': 10
    }
    result3 = detector.predict(user3)
    print(f"Input: {user3}")
    print(f"Prediction: {'BOT/FAKE' if result3['is_bot'] else 'GENUINE/HUMAN'}")
    print(f"Fake Probability: {result3['bot_probability']*100:.2f}%")
    print(f"Genuine Probability: {(1-result3['bot_probability'])*100:.2f}%")
    print(f"Confidence: {result3['confidence']}\n")

if __name__ == "__main__":
    test_real_profiles()
