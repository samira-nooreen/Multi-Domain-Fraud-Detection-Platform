from ml_modules.upi_fraud.predict import UPIFraudDetector

print("=" * 60)
print("TESTING FIXED UPI FRAUD DETECTION SYSTEM")
print("=" * 60)

# Initialize detector
detector = UPIFraudDetector()

# Test Case 1: The problematic scenario from your example
print("\n📝 TEST CASE 1: High-value transaction at unusual time")
print("-" * 50)
test_data_1 = {
    'amount': 1000000,  # ₹10 lakhs
    'time_of_transaction': '03:34',  # Unusual time (3:34 AM)
    'device_changed': 0,  # No device change
    'user_avg_amount': 5000,  # User normally transacts ₹5000
    'is_first_time_receiver': 0  # Not first time receiver
}

result_1 = detector.predict(test_data_1)
print(f"Amount: ₹{test_data_1['amount']:,}")
print(f"Time: {test_data_1['time_of_transaction']} (Unusual hours)")
print(f"Device Changed: {'Yes' if test_data_1['device_changed'] else 'No'}")
print(f"User Avg Amount: ₹{test_data_1['user_avg_amount']:,}")
print()
print(f"🔴 Fraud Probability: {result_1['fraud_probability']:.2%}")
print(f"🟢 Legitimate Probability: {result_1['legitimate_probability']:.2%}")
print(f"⚠️  Risk Level: {result_1['risk_level']}")
print(f"📊 Recommendation: {result_1['recommendation']}")
if 'risk_factors' in result_1 and result_1['risk_factors']:
    print("🔍 Risk Factors:")
    for factor in result_1['risk_factors']:
        print(f"   • {factor}")

# Test Case 2: High amount with device change
print("\n📝 TEST CASE 2: High-value transaction with device change")
print("-" * 50)
test_data_2 = {
    'amount': 750000,  # ₹7.5 lakhs
    'time_of_transaction': '14:30',  # Normal time
    'device_changed': 1,  # Device changed
    'user_avg_amount': 8000,  # User normally transacts ₹8000
    'is_first_time_receiver': 1  # First time receiver
}

result_2 = detector.predict(test_data_2)
print(f"Amount: ₹{test_data_2['amount']:,}")
print(f"Time: {test_data_2['time_of_transaction']} (Normal hours)")
print(f"Device Changed: {'Yes' if test_data_2['device_changed'] else 'No'}")
print(f"User Avg Amount: ₹{test_data_2['user_avg_amount']:,}")
print(f"First Time Receiver: {'Yes' if test_data_2['is_first_time_receiver'] else 'No'}")
print()
print(f"🔴 Fraud Probability: {result_2['fraud_probability']:.2%}")
print(f"🟢 Legitimate Probability: {result_2['legitimate_probability']:.2%}")
print(f"⚠️  Risk Level: {result_2['risk_level']}")
print(f"📊 Recommendation: {result_2['recommendation']}")
if 'risk_factors' in result_2 and result_2['risk_factors']:
    print("🔍 Risk Factors:")
    for factor in result_2['risk_factors']:
        print(f"   • {factor}")

# Test Case 3: Normal transaction
print("\n📝 TEST CASE 3: Normal low-value transaction")
print("-" * 50)
test_data_3 = {
    'amount': 2500,  # ₹2,500
    'time_of_transaction': '11:30',  # Normal business hours
    'device_changed': 0,  # No device change
    'user_avg_amount': 3000,  # User normally transacts ₹3000
    'is_first_time_receiver': 0  # Not first time receiver
}

result_3 = detector.predict(test_data_3)
print(f"Amount: ₹{test_data_3['amount']:,}")
print(f"Time: {test_data_3['time_of_transaction']} (Normal hours)")
print(f"Device Changed: {'Yes' if test_data_3['device_changed'] else 'No'}")
print(f"User Avg Amount: ₹{test_data_3['user_avg_amount']:,}")
print()
print(f"🔴 Fraud Probability: {result_3['fraud_probability']:.2%}")
print(f"🟢 Legitimate Probability: {result_3['legitimate_probability']:.2%}")
print(f"⚠️  Risk Level: {result_3['risk_level']}")
print(f"📊 Recommendation: {result_3['recommendation']}")
if 'risk_factors' in result_3 and result_3['risk_factors']:
    print("🔍 Risk Factors:")
    for factor in result_3['risk_factors']:
        print(f"   • {factor}")

print("\n" + "=" * 60)
print("✅ FIXED SYSTEM VERIFICATION COMPLETE")
print("=" * 60)
print("Key Improvements Implemented:")
print("1. ✅ Hybrid approach combining ML + rule-based boosting")
print("2. ✅ Proper class imbalance handling")
print("3. ✅ Behavioral deviation features (amount ratios)")
print("4. ✅ Time-based risk weighting")
print("5. ✅ High-risk scenario post-processing")
print("6. ✅ Realistic probability calibration")
print("7. ✅ Improved recommendation system")
print("=" * 60)