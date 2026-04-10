from ml_modules.click_fraud.predict import ClickFraudDetector
import numpy as np

np.random.seed(42)
detector = ClickFraudDetector(model_dir='ml_modules/click_fraud')

# Test case: 40 clicks in 50 seconds, Fast/Automated pattern
clicks = 40
time_spent = 50
avg_time = time_spent / clicks
velocity = (clicks / time_spent) * 60

print(f"Input: {clicks} clicks in {time_spent}s")
print(f"Avg time per click: {avg_time:.2f}s")
print(f"Velocity: {velocity:.1f} clicks/min")
print()

# Build sequence with Automated pattern (very consistent, concentrated)
seq = []
for _ in range(clicks):
    time_diff = avg_time * (0.85 + np.random.random() * 0.3)
    click_x = 400 + np.random.uniform(-20, 20)
    click_y = 300 + np.random.uniform(-20, 20)
    referrer_entropy = np.random.uniform(0, 0.5)
    
    seq.append([
        max(0.01, time_diff),
        max(0, click_x),
        max(0, click_y),
        0,  # ip_change
        0,  # ua_change
        14, # hour
        0,  # is_weekend
        max(0, velocity),
        max(0, referrer_entropy)
    ])

result = detector.predict(seq)

print(f"Fraud Probability: {result['fraud_probability']*100:.1f}%")
print(f"Risk Level: {result['risk_level']}")
print(f"Is Fraud: {result['is_fraud']}")
print(f"Recommendation: {result['recommendation']}")
if 'indicators' in result:
    print(f"\nIndicators ({len(result['indicators'])}):")
    for ind in result['indicators']:
        print(f"  - {ind}")
