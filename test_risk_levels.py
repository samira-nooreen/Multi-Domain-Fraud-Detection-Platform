from ml_modules.click_fraud.predict import ClickFraudDetector
import numpy as np

detector = ClickFraudDetector(model_dir='ml_modules/click_fraud')

def test_case(name, clicks, time_spent, pattern, ip_changes):
    """Test a specific case"""
    np.random.seed(42)
    
    avg_time = time_spent / clicks
    velocity = (clicks / time_spent) * 60
    
    seq = []
    for _ in range(clicks):
        if pattern == 'normal':
            time_diff = avg_time + np.random.uniform(-avg_time*0.25, avg_time*0.25)
            click_x = np.random.uniform(100, 900)
            click_y = np.random.uniform(100, 700)
            referrer_entropy = np.random.uniform(1.5, 3.0)
        elif pattern == 'fast':
            time_diff = avg_time * (0.85 + np.random.random() * 0.3)
            click_x = 400 + np.random.uniform(-20, 20)
            click_y = 300 + np.random.uniform(-20, 20)
            referrer_entropy = np.random.uniform(0, 0.5)
        else:  # suspicious
            time_diff = avg_time * (0.5 + np.random.random())
            click_x = 400 + np.random.uniform(-50, 50)
            click_y = 300 + np.random.uniform(-50, 50)
            referrer_entropy = np.random.uniform(0.3, 1.2)  # Lower entropy for more suspicious
        
        seq.append([
            max(0.01, time_diff),
            max(0, click_x),
            max(0, click_y),
            0, 0, 14, 0,
            max(0, velocity),
            max(0, referrer_entropy)
        ])
    
    result = detector.predict(seq)
    
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Input: {clicks} clicks, {time_spent}s, {pattern}")
    print(f"Fraud: {result['fraud_probability']*100:.1f}%")
    print(f"Risk: {result['risk_level']}")
    print(f"Is Fraud: {result['is_fraud']}")
    print(f"Recommendation: {result['recommendation']}")
    
    return result

print("\n" + "="*60)
print("TESTING ALL RISK LEVELS")
print("="*60)

# LOW RISK
r1 = test_case("LOW RISK - Normal User", 5, 300, 'normal', 0)

# MEDIUM RISK - This is the problematic one
r2 = test_case("MEDIUM RISK - Suspicious Pattern", 25, 90, 'suspicious', 0)

# HIGH RISK
r3 = test_case("HIGH RISK - Automated Bot", 60, 40, 'fast', 0)

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"LOW:    {r1['risk_level']} ({r1['fraud_probability']*100:.1f}%) - {'✅' if r1['risk_level'] == 'LOW' else '❌'}")
print(f"MEDIUM: {r2['risk_level']} ({r2['fraud_probability']*100:.1f}%) - {'✅' if r2['risk_level'] == 'MEDIUM' else '❌'}")
print(f"HIGH:   {r3['risk_level']} ({r3['fraud_probability']*100:.1f}%) - {'✅' if r3['risk_level'] in ['HIGH', 'CRITICAL'] else '❌'}")
