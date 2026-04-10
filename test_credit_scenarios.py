"""
Test credit card fraud detection with different scenarios
"""
from ml_modules.credit_card.predict import CreditCardFraudDetector

# Initialize detector
detector = CreditCardFraudDetector()

test_cases = [
    {
        'name': 'Small Safe Transaction',
        'data': {
            'amount': 5000,
            'location': 'Hyderabad',
            'transaction_type': 'POS',
            'card_present': 1
        }
    },
    {
        'name': 'Medium Online Transaction',
        'data': {
            'amount': 50000,
            'location': 'Mumbai',
            'transaction_type': 'Online',
            'card_present': 0
        }
    },
    {
        'name': 'Large Online No Card',
        'data': {
            'amount': 500000,
            'location': 'Delhi',
            'transaction_type': 'Online',
            'card_present': 0
        }
    },
    {
        'name': 'Very Large Online No Card',
        'data': {
            'amount': 1000000,
            'location': 'Bangalore',
            'transaction_type': 'Online',
            'card_present': 0
        }
    }
]

print("="*80)
print("CREDIT CARD FRAUD DETECTION - TEST RESULTS")
print("="*80)

for test in test_cases:
    print(f"\n{test['name']}:")
    print(f"  Amount: ₹{test['data']['amount']:,}")
    print(f"  Type: {test['data']['transaction_type']}")
    print(f"  Card Present: {'Yes' if test['data']['card_present'] else 'No'}")
    
    result = detector.predict(test['data'])
    
    print(f"  ➤ Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"  ➤ Risk Level: {result['risk_level']}")
    print(f"  ➤ Recommendation: {result['recommendation']}")
    
    if 'risk_factors' in result:
        print(f"  ➤ Risk Factors:")
        for factor in result['risk_factors']:
            print(f"     - {factor}")

print("\n" + "="*80)
