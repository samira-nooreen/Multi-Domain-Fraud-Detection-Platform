import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_modules', 'fake_profile'))

from ml_modules.fake_profile.predict import BotDetector

def test_real_user():
    print("\n=== Testing Real User Profile ===\n")
    
    detector = BotDetector(model_dir='ml_modules/fake_profile')
    
    # User's real profile: @_.sammu._01
    real_user = {
        'followers': 390,
        'following': 566,
        'posts': 0,  # No posts yet
        'age_days': 365,  # 1 year old account
        'verified': 0,
        'bio_length': 5,
        'profile_completeness': 0.7,  # Has profile picture
        'ip_diversity': 3  # Reasonable
    }
    
    result = detector.predict(real_user)
    
    print(f"Profile: @_.sammu._01")
    print(f"Followers: {real_user['followers']}")
    print(f"Following: {real_user['following']}")
    print(f"Posts: {real_user['posts']}")
    print(f"Account Age: {real_user['age_days']} days")
    print(f"\n{'='*50}")
    print(f"Prediction: {'BOT' if result['is_bot'] else 'HUMAN'}")
    print(f"Bot Probability: {result['bot_probability']:.4f} ({result['bot_probability']*100:.2f}%)")
    print(f"Human Probability: {(1-result['bot_probability'])*100:.2f}%")
    print(f"Confidence: {result['confidence']}")
    print(f"\nModel Breakdown:")
    for model, prob in result['details'].items():
        print(f"  {model}: {prob:.4f}")

if __name__ == "__main__":
    test_real_user()
