from ml_modules.click_fraud.predict import ClickFraudDetector
import numpy as np

np.random.seed(42)
detector = ClickFraudDetector(model_dir='ml_modules/click_fraud')

# Test case: 8 clicks in 20 seconds, Suspicious Pattern
clicks = 8
time_spent = 20
avg_time = time_spent / clicks
velocity = (clicks / time_spent) * 60

print(f"Input: {clicks} clicks in {time_spent}s")
print(f"Avg time per click: {avg_time:.2f}s")
print(f"Velocity: {velocity:.1f} clicks/min")
print()

# Build sequence with Suspicious pattern
seq = []
for _ in range(clicks):
    time_diff = avg_time * (0.5 + np.random.random())
    click_x = 400 + np.random.uniform(-50, 50)
    click_y = 300 + np.random.uniform(-50, 50)
    referrer_entropy = np.random.uniform(0.3, 1.2)
    
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

print(f"\n{'='*60}")
if result['risk_level'] == 'MEDIUM':
    print("✅ CORRECT - Suspicious pattern properly detected as MEDIUM risk")
else:
    print(f"❌ WRONG - Should be MEDIUM, got {result['risk_level']}")
