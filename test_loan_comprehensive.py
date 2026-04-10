"""
Comprehensive Loan Default Prediction Test Suite
Tests all risk levels and edge cases
"""
from ml_modules.loan_default.predict import LoanDefaultPredictor

# Initialize predictor
predictor = LoanDefaultPredictor()

test_cases = [
    {
        'name': '🔴 HIGH RISK - Should Reject',
        'data': {
            'loan_amount': 500000,
            'monthly_income': 15000,
            'credit_score': 420,
            'loan_duration': 12
        },
        'expected': 'HIGH'
    },
    {
        'name': '🟢 LOW RISK - Safe',
        'data': {
            'loan_amount': 200000,
            'monthly_income': 80000,
            'credit_score': 750,
            'loan_duration': 36
        },
        'expected': 'LOW'
    },
    {
        'name': '🟡 MEDIUM RISK - Borderline',
        'data': {
            'loan_amount': 300000,
            'monthly_income': 40000,
            'credit_score': 650,
            'loan_duration': 24
        },
        'expected': 'MEDIUM'
    },
    {
        'name': '💣 EXTREME FRAUD TEST',
        'data': {
            'loan_amount': 1000000,
            'monthly_income': 10000,
            'credit_score': 350,
            'loan_duration': 6
        },
        'expected': 'VERY_HIGH'
    },
    {
        'name': '⚠️ BUG TEST - Invalid Inputs',
        'data': {
            'loan_amount': '',
            'monthly_income': -5000,
            'credit_score': 900,
            'loan_duration': 12
        },
        'expected': 'ERROR'
    }
]

print("="*80)
print("LOAN DEFAULT PREDICTION - COMPREHENSIVE TEST SUITE")
print("="*80)

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    print(f"\nInputs:")
    for key, value in test['data'].items():
        print(f"  {key}: {value}")
    
    print(f"\nExpected: {test['expected']} RISK")
    print("-"*80)
    
    try:
        result = predictor.predict(test['data'])
        
        print(f"\n✅ PREDICTION SUCCESS:")
        print(f"  Default Probability: {result['default_probability']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Decision: {result['decision']}")
        print(f"  Recommendation: {result['recommendation']}")
        print(f"  Risk Score: {result['risk_score']}/1000")
        
        # Check if matches expected
        if test['expected'] == result['risk_level']:
            print(f"\n✅ PASS - Risk level matches expected: {test['expected']}")
            passed += 1
        elif test['expected'] == 'ERROR':
            print(f"\n⚠️  WARNING - Should have thrown validation error")
            failed += 1
        else:
            print(f"\n❌ FAIL - Expected {test['expected']}, got {result['risk_level']}")
            failed += 1
            
    except Exception as e:
        if test['expected'] == 'ERROR':
            print(f"\n✅ PASS - Correctly caught validation error: {e}")
            passed += 1
        else:
            print(f"\n❌ FAIL - Unexpected error: {e}")
            failed += 1

print(f"\n{'='*80}")
print(f"TEST SUMMARY")
print(f"{'='*80}")
print(f"\nTotal Tests: {len(test_cases)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
print(f"\n{'='*80}")
