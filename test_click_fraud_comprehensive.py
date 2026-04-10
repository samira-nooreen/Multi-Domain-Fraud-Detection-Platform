"""
Click Fraud Detection - Comprehensive Test Suite
Tests all 8 scenarios with expected outcomes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from ml_modules.click_fraud.predict import ClickFraudDetector
import numpy as np

def build_sequence(clicks, time_spent, pattern, ip_changes):
    """Build realistic click sequence based on parameters"""
    seq = []
    avg_time = time_spent / clicks
    velocity = (clicks / time_spent) * 60
    hour = 14
    is_weekend = 0
    
    for i in range(clicks):
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
            referrer_entropy = np.random.uniform(0.5, 1.5)
        
        ip_change = 1 if (i == 0 and ip_changes > 0) else 0
        ua_change = 1 if (ip_changes > 3 and np.random.random() < 0.3) else 0
        
        seq.append([
            max(0.01, time_diff),
            max(0, click_x),
            max(0, click_y),
            ip_change,
            ua_change,
            hour,
            is_weekend,
            max(0, velocity),
            max(0, referrer_entropy)
        ])
    
    return seq

def run_test(test_num, name, clicks, time_spent, pattern, ip_changes, expected_risk):
    """Run a single test case"""
    detector = ClickFraudDetector(model_dir='ml_modules/click_fraud')
    seq = build_sequence(clicks, time_spent, pattern, ip_changes)
    result = detector.predict(seq)
    
    prob = result['fraud_probability'] * 100
    risk = result['risk_level']
    
    # Color coding
    if expected_risk in risk:
        status = "✅ PASS"
    elif (expected_risk == 'LOW' and risk in ['LOW']) or \
         (expected_risk == 'MEDIUM' and risk in ['MEDIUM', 'LOW']) or \
         (expected_risk in ['HIGH', 'CRITICAL'] and risk in ['HIGH', 'CRITICAL', 'MEDIUM']):
        status = "⚠️ CLOSE"
    else:
        status = "❌ FAIL"
    
    print(f"\n{'='*60}")
    print(f"TEST {test_num}: {name}")
    print(f"{'='*60}")
    print(f"Input: {clicks} clicks, {time_spent}s, {pattern}, {ip_changes} IP changes")
    print(f"Expected: {expected_risk}")
    print(f"Got:      {risk} ({prob:.1f}%)")
    print(f"Status:   {status}")
    if 'indicators' in result:
        print(f"Indicators: {', '.join(result['indicators'][:3])}")
    
    return status

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CLICK FRAUD DETECTION - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        (1, "NORMAL USER", 5, 300, 'normal', 0, 'LOW'),
        (2, "HEAVY BUT LEGIT", 40, 1200, 'normal', 0, 'LOW'),
        (3, "SLIGHTLY SUSPICIOUS", 25, 90, 'suspicious', 0, 'MEDIUM'),
        (4, "FAST USER", 30, 80, 'fast', 0, 'HIGH'),  # Automated = HIGH
        (5, "AUTOMATED BOT", 60, 40, 'fast', 0, 'HIGH'),
        (6, "BOT + IP CHANGE", 80, 30, 'fast', 3, 'CRITICAL'),
        (7, "CLICK FARM", 120, 60, 'suspicious', 5, 'CRITICAL'),
        (8, "EDGE CASE", 10, 20, 'suspicious', 0, 'MEDIUM'),
    ]
    
    results = []
    for test in tests:
        result = run_test(*test)
        results.append(result)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = results.count('✅ PASS')
    close = results.count('⚠️ CLOSE')
    failed = results.count('❌ FAIL')
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Close:  {close}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if passed >= 6:
        print("\n🎉 Module is industry-level ready!")
    elif passed >= 4:
        print("\n⚠️ Module needs minor tuning")
    else:
        print("\n❌ Module needs significant improvements")
