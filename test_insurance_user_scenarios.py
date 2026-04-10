"""
Test Insurance Fraud with User's Scenarios
"""
from ml_modules.insurance_fraud.predict import InsuranceFraudDetector

detector = InsuranceFraudDetector()

test_cases = [
    {
        'name': '🔴 HIGH FRAUD (must detect)',
        'data': {
            'claim_amount': 250000,
            'claim_type': 'Accident',
            'incident_description': 'Minor accident but claiming total vehicle loss, no proper documents.',
            'previous_claim_count': 4
        },
        'expected': 'HIGH'
    },
    {
        'name': '🟢 LOW FRAUD (safe)',
        'data': {
            'claim_amount': 20000,
            'claim_type': 'Medical',
            'incident_description': 'Hospital bills submitted with valid reports and prescriptions.',
            'previous_claim_count': 0
        },
        'expected': 'LOW'
    },
    {
        'name': '🟡 MEDIUM FRAUD (your test case)',
        'data': {
            'claim_amount': 60000,
            'claim_type': 'Theft',
            'incident_description': 'Phone stolen, no bill available but police complaint filed.',
            'previous_claim_count': 2
        },
        'expected': 'MEDIUM'
    },
    {
        'name': '💣 EXTREME FRAUD TEST',
        'data': {
            'claim_amount': 500000,
            'claim_type': 'Accident',
            'incident_description': 'Claiming full damage, vague description, urgent request, inconsistent details.',
            'previous_claim_count': 6
        },
        'expected': 'VERY_HIGH'
    }
]

print("="*80)
print("INSURANCE FRAUD DETECTION - USER SCENARIOS")
print("="*80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    
    data = test['data']
    print(f"\nInputs:")
    print(f"  Claim Amount: ₹{data['claim_amount']:,}")
    print(f"  Type: {data['claim_type']}")
    print(f"  Previous Claims: {data['previous_claim_count']}")
    print(f"  Description: {data['incident_description'][:60]}...")
    
    print(f"\nExpected: {test['expected']}")
    print("-"*80)
    
    try:
        result = detector.predict(test['data'])
        
        print(f"\n✅ ACTUAL RESULT:")
        print(f"  Fraud Probability: {result['fraud_probability']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Recommendation: {result['recommendation']}")
        
        if 'reasons' in result:
            print(f"\n  Key Factors:")
            for reason in result['reasons'][:4]:
                print(f"    • {reason}")
        
        if result['risk_level'] == test['expected']:
            print(f"\n✅✅✅ PERFECT MATCH!")
        else:
            print(f"\n⚠️  Expected {test['expected']}, got {result['risk_level']}")
            print(f"   (May still be acceptable depending on scenario)")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*80}")
print("TESTING COMPLETE")
print(f"{'='*80}")
