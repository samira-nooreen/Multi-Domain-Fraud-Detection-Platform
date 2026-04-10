"""
Test the enhanced credit card fraud detection system
"""
from ml_modules.credit_card.predict import CreditCardFraudDetector

def test_enhanced_fraud_detection():
    print("=" * 70)
    print("ENHANCED CREDIT CARD FRAUD DETECTION SYSTEM - TEST RESULTS")
    print("=" * 70)
    
    # Initialize detector
    detector = CreditCardFraudDetector()
    
    # Test Case 1: Normal transaction (should be APPROVED)
    print("\n📝 TEST CASE 1: Normal Low-Value Transaction")
    print("-" * 50)
    normal_tx = {
        'amount': 123,
        'location': 'Hyderabad',
        'transaction_type': 'POS',
        'card_present': 1
    }
    
    result1 = detector.predict(normal_tx)
    print(f"Amount: ₹{normal_tx['amount']}")
    print(f"Location: {normal_tx['location']}")
    print(f"Type: {normal_tx['transaction_type']}")
    print(f"Card Present: {'Yes' if normal_tx['card_present'] else 'No'}")
    print(f"Fraud Probability: {result1['fraud_probability']:.2%}")
    print(f"Risk Level: {result1['risk_level']}")
    print(f"Recommendation: {result1['recommendation']}")
    if 'risk_factors' in result1 and result1['risk_factors']:
        print("Risk Factors:", result1['risk_factors'])
    
    # Test Case 2: High-value transaction (should be flagged)
    print("\n📝 TEST CASE 2: High-Value Transaction")
    print("-" * 50)
    high_value_tx = {
        'amount': 750000,
        'location': 'Hyderabad',
        'transaction_type': 'POS',
        'card_present': 1
    }
    
    result2 = detector.predict(high_value_tx)
    print(f"Amount: ₹{high_value_tx['amount']:,}")
    print(f"Location: {high_value_tx['location']}")
    print(f"Type: {high_value_tx['transaction_type']}")
    print(f"Card Present: {'Yes' if high_value_tx['card_present'] else 'No'}")
    print(f"Fraud Probability: {result2['fraud_probability']:.2%}")
    print(f"Risk Level: {result2['risk_level']}")
    print(f"Recommendation: {result2['recommendation']}")
    if 'risk_factors' in result2 and result2['risk_factors']:
        print("Risk Factors:", result2['risk_factors'])
    
    # Test Case 3: Online transaction without card (HIGH RISK)
    print("\n📝 TEST CASE 3: High-Risk Online Transaction")
    print("-" * 50)
    online_risk_tx = {
        'amount': 60000,
        'location': 'Unknown',
        'transaction_type': 'Online',
        'card_present': 0
    }
    
    result3 = detector.predict(online_risk_tx)
    print(f"Amount: ₹{online_risk_tx['amount']:,}")
    print(f"Location: {online_risk_tx['location']}")
    print(f"Type: {online_risk_tx['transaction_type']}")
    print(f"Card Present: {'Yes' if online_risk_tx['card_present'] else 'No'}")
    print(f"Fraud Probability: {result3['fraud_probability']:.2%}")
    print(f"Risk Level: {result3['risk_level']}")
    print(f"Recommendation: {result3['recommendation']}")
    if 'risk_factors' in result3 and result3['risk_factors']:
        print("Risk Factors:", result3['risk_factors'])
    
    # Test Case 4: Very high amount (CRITICAL RISK)
    print("\n📝 TEST CASE 4: Critical Risk - Very High Amount")
    print("-" * 50)
    critical_tx = {
        'amount': 1500000,
        'location': 'Foreign',
        'transaction_type': 'Online',
        'card_present': 0
    }
    
    result4 = detector.predict(critical_tx)
    print(f"Amount: ₹{critical_tx['amount']:,}")
    print(f"Location: {critical_tx['location']}")
    print(f"Type: {critical_tx['transaction_type']}")
    print(f"Card Present: {'Yes' if critical_tx['card_present'] else 'No'}")
    print(f"Fraud Probability: {result4['fraud_probability']:.2%}")
    print(f"Risk Level: {result4['risk_level']}")
    print(f"Recommendation: {result4['recommendation']}")
    if 'risk_factors' in result4 and result4['risk_factors']:
        print("Risk Factors:", result4['risk_factors'])
    
    print("\n" + "=" * 70)
    print("FRAUD DETECTION SYSTEM VERIFICATION")
    print("=" * 70)
    
    # Verify the system is working correctly
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Normal transaction should be approved
    if result1['fraud_probability'] < 0.15 and result1['recommendation'] == 'APPROVE':
        print("✅ Test 1 PASSED: Normal transaction correctly approved")
        tests_passed += 1
    else:
        print("❌ Test 1 FAILED: Normal transaction not handled correctly")
    
    # Test 2: High-value transaction should be flagged
    if result2['fraud_probability'] > 0.3 and result2['risk_level'] in ['MEDIUM', 'HIGH']:
        print("✅ Test 2 PASSED: High-value transaction properly flagged")
        tests_passed += 1
    else:
        print("❌ Test 2 FAILED: High-value transaction not flagged correctly")
    
    # Test 3: High-risk online transaction should be blocked/reviewed
    if result3['fraud_probability'] > 0.5 and result3['recommendation'] in ['STEP-UP AUTHENTICATION', 'BLOCK TRANSACTION']:
        print("✅ Test 3 PASSED: High-risk transaction properly identified")
        tests_passed += 1
    else:
        print("❌ Test 3 FAILED: High-risk transaction not handled correctly")
    
    # Test 4: Critical risk transaction should be blocked
    if result4['fraud_probability'] > 0.7 and result4['recommendation'] == 'BLOCK TRANSACTION':
        print("✅ Test 4 PASSED: Critical risk transaction correctly blocked")
        tests_passed += 1
    else:
        print("❌ Test 4 FAILED: Critical risk transaction not blocked")
    
    print(f"\n🎯 FINAL RESULT: {tests_passed}/{total_tests} tests passed")
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - Fraud detection system is working correctly!")
        print("✅ Normal transactions are approved")
        print("✅ Suspicious transactions are flagged")
        print("✅ High-risk transactions are blocked")
        print("✅ Detailed risk factors are provided")
    else:
        print("⚠️  Some tests failed - System needs adjustment")
    
    print("=" * 70)

if __name__ == "__main__":
    test_enhanced_fraud_detection()