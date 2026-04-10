"""
Test the simplified UPI fraud detection system (without user_avg_amount and first_time_receiver fields)
"""

from ml_modules.upi_fraud.predict import UPIFraudDetector

def test_simplified_system():
    print("=" * 60)
    print("TESTING SIMPLIFIED UPI FRAUD DETECTION SYSTEM")
    print("=" * 60)
    
    # Initialize detector
    detector = UPIFraudDetector()
    
    # Test Case 1: The problematic scenario (simplified inputs)
    print("\n📝 TEST CASE 1: High-value transaction at unusual time")
    print("-" * 50)
    test_data_1 = {
        'amount': 1000000,  # ₹10 lakhs
        'time_of_transaction': '03:34',  # Unusual time (3:34 AM)
        'device_changed': 0,  # No device change
        # Note: user_avg_amount and is_first_time_receiver fields removed
    }

    result_1 = detector.predict(test_data_1)
    print(f"Amount: ₹{test_data_1['amount']:,}")
    print(f"Time: {test_data_1['time_of_transaction']} (Unusual hours)")
    print(f"Device Changed: {'Yes' if test_data_1['device_changed'] else 'No'}")
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
    }

    result_2 = detector.predict(test_data_2)
    print(f"Amount: ₹{test_data_2['amount']:,}")
    print(f"Time: {test_data_2['time_of_transaction']} (Normal hours)")
    print(f"Device Changed: {'Yes' if test_data_2['device_changed'] else 'No'}")
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
    }

    result_3 = detector.predict(test_data_3)
    print(f"Amount: ₹{test_data_3['amount']:,}")
    print(f"Time: {test_data_3['time_of_transaction']} (Normal hours)")
    print(f"Device Changed: {'Yes' if test_data_3['device_changed'] else 'No'}")
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
    print("✅ SIMPLIFIED SYSTEM VERIFICATION COMPLETE")
    print("=" * 60)
    
    # Verify the system is working correctly
    success = (
        result_1['fraud_probability'] > 0.5 and  # High-risk transaction flagged
        result_2['fraud_probability'] > 0.5 and  # High-risk transaction flagged
        result_3['fraud_probability'] < 0.1 and  # Normal transaction approved
        result_1['risk_level'] in ['HIGH', 'CRITICAL'] and
        result_3['risk_level'] == 'LOW'
    )
    
    if success:
        print("🎉 SUCCESS: Simplified system is working correctly!")
        print("✅ High-risk transactions are properly flagged")
        print("✅ Normal transactions are properly approved")
        print("✅ System functions without the removed fields")
    else:
        print("❌ Some issues detected with the simplified system")
    
    print("=" * 60)

if __name__ == "__main__":
    test_simplified_system()