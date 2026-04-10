from ml_modules.upi_fraud.predict import UPIFraudDetector

# Test the current behavior
detector = UPIFraudDetector()
result = detector.predict({
    'amount': 1000000,
    'time_of_transaction': '03:34',
    'device_changed': 0
})

print("=" * 50)
print("CURRENT UPI FRAUD DETECTION BEHAVIOR")
print("=" * 50)
print(f"Transaction Amount: ₹10,00,000")
print(f"Time: 03:34 AM (High-risk time)")
print(f"Device Changed: No")
print()
print(f"Fraud Probability: {result['fraud_probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendation: {result['recommendation']}")
if 'risk_factors' in result:
    print("Risk Factors:")
    for factor in result['risk_factors']:
        print(f"  • {factor}")
print("=" * 50)