"""
Test Insurance Fraud Detection
"""
from ml_modules.insurance_fraud.predict import InsuranceFraudDetector

# Initialize detector
detector = InsuranceFraudDetector()

test_cases = [
    {
        'name': '🟢 LOW RISK - Legitimate Claim',
        'data': {
            'claim_amount': 50000,
            'claim_type': 'Accident',
            'incident_description': 'Car collision at intersection. Police report filed.',
            'previous_claim_count': 0
        }
    },
    {
        'name': '🟡 MEDIUM RISK - Somewhat Suspicious',
        'data': {
            'claim_amount': 200000,
            'claim_type': 'Accident',
            'incident_description': 'Minor scratch but claiming full damage. Urgent settlement needed.',
            'previous_claim_count': 5
        }
    },
    {
        'name': '🔴 HIGH RISK - Likely Fraud',
        'data': {
            'claim_amount': 1000000,
            'claim_type': 'Theft',
            'incident_description': 'Car stolen from parking lot. No police report. Need money fast.',
            'previous_claim_count': 10
        }
    }
]

print("="*80)
print("INSURANCE FRAUD DETECTION - TEST RESULTS")
print("="*80)

for test in test_cases:
    print(f"\n{test['name']}:")
    print(f"  Claim Amount: ₹{test['data']['claim_amount']:,}")
    print(f"  Claim Type: {test['data']['claim_type']}")
    print(f"  Previous Claims: {test['data']['previous_claim_count']}")
    print(f"  Description: {test['data']['incident_description'][:50]}...")
    
    try:
        result = detector.predict(test['data'])
        
        print(f"  ➤ Fraud Probability: {result.get('fraud_probability', result.get('default_probability', 0)):.2%}")
        print(f"  ➤ Risk Level: {result.get('risk_level', 'UNKNOWN')}")
        print(f"  ➤ Decision: {result.get('decision', result.get('recommendation', 'N/A'))}")
        
        if 'risk_factors' in result:
            print(f"  ➤ Risk Factors:")
            for factor in result['risk_factors'][:3]:
                print(f"     - {factor}")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
