"""
Test the exact scenarios provided by user
"""
from ml_modules.loan_default.predict import LoanDefaultPredictor

predictor = LoanDefaultPredictor()

test_cases = [
    {
        'name': '🔴 HIGH DEFAULT (must detect)',
        'data': {
            'loan_amount': 800000,
            'monthly_income': 20000,
            'credit_score': 450,
            'loan_duration': 12
        },
        'expected': 'HIGH'
    },
    {
        'name': '🟢 LOW DEFAULT (safe)',
        'data': {
            'loan_amount': 200000,
            'monthly_income': 90000,
            'credit_score': 780,
            'loan_duration': 36
        },
        'expected': 'LOW'
    },
    {
        'name': '🟡 MEDIUM DEFAULT',
        'data': {
            'loan_amount': 300000,
            'monthly_income': 40000,
            'credit_score': 650,
            'loan_duration': 24
        },
        'expected': 'MEDIUM'
    },
    {
        'name': '💣 EXTREME CASE',
        'data': {
            'loan_amount': 1200000,
            'monthly_income': 15000,
            'credit_score': 350,
            'loan_duration': 6
        },
        'expected': 'VERY_HIGH'
    }
]

print("="*80)
print("LOAN DEFAULT PREDICTION - USER SCENARIOS")
print("="*80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    
    data = test['data']
    print(f"\nInputs:")
    print(f"  Loan Amount: ₹{data['loan_amount']:,}")
    print(f"  Monthly Income: ₹{data['monthly_income']:,}")
    print(f"  Credit Score: {data['credit_score']}")
    print(f"  Duration: {data['loan_duration']} months")
    
    # Calculate metrics
    dti = data['loan_amount'] / data['monthly_income']
    emi = data['loan_amount'] / data['loan_duration']
    emi_ratio = emi / data['monthly_income']
    
    print(f"\nCalculated Metrics:")
    print(f"  DTI Ratio: {dti:.1f}x")
    print(f"  Monthly EMI: ₹{emi:,.0f}")
    print(f"  EMI/Income: {emi_ratio:.0%}")
    
    print(f"\nExpected: {test['expected']}")
    print("-"*80)
    
    try:
        result = predictor.predict(test['data'])
        
        print(f"\n✅ ACTUAL RESULT:")
        print(f"  Default Probability: {result['default_probability']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Decision: {result['decision']}")
        print(f"  Recommendation: {result['recommendation']}")
        
        if result['risk_level'] == test['expected']:
            print(f"\n✅✅✅ PASS - Matches expected!")
        else:
            print(f"\n⚠️  Expected {test['expected']}, got {result['risk_level']}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

print(f"\n{'='*80}")
print("TESTING COMPLETE")
print(f"{'='*80}")
