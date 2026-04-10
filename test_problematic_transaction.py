from ml_modules.credit_card.predict import CreditCardFraudDetector

# Test the problematic transaction
detector = CreditCardFraudDetector()
result = detector.predict({
    'amount': 1000000,
    'location': 'Hyderabad',
    'transaction_type': 'Online',
    'card_present': 0
})

print("=" * 50)
print("CREDIT CARD FRAUD DETECTION - TEST CASE")
print("=" * 50)
print(f"Transaction Amount: ₹10,00,000")
print(f"Location: Hyderabad")
print(f"Transaction Type: Online")
print(f"Card Present: No")
print()
print(f"🔴 Fraud Probability: {result['fraud_probability']:.2%}")
print(f"🟢 Legitimate Probability: {result['legitimate_probability']:.2%}")
print(f"⚠️  Risk Level: {result['risk_level']}")
print(f"📊 Recommendation: {result['recommendation']}")
if 'risk_factors' in result and result['risk_factors']:
    print("🔍 Risk Factors:")
    for factor in result['risk_factors']:
        print(f"   • {factor}")
print("=" * 50)