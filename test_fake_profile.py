import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_modules', 'fake_profile'))

from ml_modules.fake_profile.predict import BotDetector

def test_fake_profile_detection():
    print("\n=== Fake Profile / Bot Detection Module Test ===\n")
    
    detector = BotDetector(model_dir='ml_modules/fake_profile')
    
    # Case 1: Obvious Bot
    print("\n--- Testing Case 1: Obvious Bot ---")
    bot_user = {
        'followers': 15,
        'following': 3000,
        'posts': 5000,
        'age_days': 10,
        'verified': 0,
        'ip_diversity': 1,
        'bio_length': 0,
        'profile_completeness': 0.1
    }
    result_bot = detector.predict(bot_user)
    print(f"Input: {bot_user}")
    print(f"Prediction: {'BOT' if result_bot['is_bot'] else 'HUMAN'} (Prob: {result_bot['bot_probability']:.4f})")
    print(f"Confidence: {result_bot['confidence']}")
    print("Details:", result_bot['details'])
    
    # Case 2: Obvious Human
    print("\n--- Testing Case 2: Obvious Human ---")
    human_user = {
        'followers': 800,
        'following': 400,
        'posts': 150,
        'age_days': 700,
        'verified': 1,
        'ip_diversity': 5,
        'bio_length': 120,
        'profile_completeness': 1.0
    }
    result_human = detector.predict(human_user)
    print(f"Input: {human_user}")
    print(f"Prediction: {'BOT' if result_human['is_bot'] else 'HUMAN'} (Prob: {result_human['bot_probability']:.4f})")
    print(f"Confidence: {result_human['confidence']}")
    print("Details:", result_human['details'])
    
    # Case 3: Ambiguous User
    print("\n--- Testing Case 3: Ambiguous User ---")
    ambiguous_user = {
        'followers': 200,
        'following': 500,
        'posts': 50,
        'age_days': 60,
        'verified': 0,
        'ip_diversity': 2,
        'bio_length': 20,
        'profile_completeness': 0.5
    }
    result_amb = detector.predict(ambiguous_user)
    print(f"Input: {ambiguous_user}")
    print(f"Prediction: {'BOT' if result_amb['is_bot'] else 'HUMAN'} (Prob: {result_amb['bot_probability']:.4f})")
    print(f"Confidence: {result_amb['confidence']}")
    print("Details:", result_amb['details'])

if __name__ == "__main__":
    test_fake_profile_detection()
