from ml_modules.upi_fraud.predict import UPIFraudDetector

# Test the problematic transaction
detector = UPIFraudDetector()
result = detector.predict({
    'amount': 1000090,
    'time_of_transaction': '03:34',
    'device_changed': 0
})

print("=" * 50)
print("UPI FRAUD DETECTION - FIXED VERSION")
print("=" * 50)
print(f"Transaction Amount: ₹{1000090:,}")
print(f"Time: 03:34 AM")
print(f"Device Changed: No")
print()
print(f"Fraud Probability: {result['fraud_probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendation: {result['recommendation']}")
if 'risk_factors' in result and result['risk_factors']:
    print("Risk Factors:")
    for factor in result['risk_factors']:
        print(f"  • {factor}")
print("=" * 50)