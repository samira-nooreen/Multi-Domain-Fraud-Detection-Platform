"""
Comprehensive test of the fixed credit card fraud detection system
"""
from ml_modules.credit_card.predict import CreditCardFraudDetector

def test_fixed_system():
    print("=" * 70)
    print("COMPREHENSIVE CREDIT CARD FRAUD DETECTION TEST - AFTER FIX")
    print("=" * 70)
    
    detector = CreditCardFraudDetector()
    
    # Test cases that should be BLOCKED
    print("\n🚨 HIGH-RISK TRANSACTIONS (SHOULD BE BLOCKED):")
    print("-" * 50)
    
    # Test 1: ₹10,00,000 online without card
    test1 = {'amount': 1000000, 'location': 'Hyderabad', 'transaction_type': 'Online', 'card_present': 0}
    result1 = detector.predict(test1)
    print(f"1. ₹10,00,000 Online, No Card:")
    print(f"   Fraud Probability: {result1['fraud_probability']:.2%}")
    print(f"   Risk Level: {result1['risk_level']}")
    print(f"   Recommendation: {result1['recommendation']}")
    print(f"   Status: {'✅ CORRECT' if result1['fraud_probability'] > 0.7 else '❌ WRONG'}")
    
    # Test 2: ₹15,00,000 online from unknown location
    test2 = {'amount': 1500000, 'location': 'Unknown', 'transaction_type': 'Online', 'card_present': 0}
    result2 = detector.predict(test2)
    print(f"\n2. ₹15,00,000 Online, Unknown Location, No Card:")
    print(f"   Fraud Probability: {result2['fraud_probability']:.2%}")
    print(f"   Risk Level: {result2['risk_level']}")
    print(f"   Recommendation: {result2['recommendation']}")
    print(f"   Status: {'✅ CORRECT' if result2['fraud_probability'] > 0.7 else '❌ WRONG'}")
    
    # Test cases that should be flagged for review
    print("\n🟡 MEDIUM-RISK TRANSACTIONS (SHOULD BE REVIEWED):")
    print("-" * 50)
    
    # Test 3: ₹7,50,000 online
    test3 = {'amount': 750000, 'location': 'Hyderabad', 'transaction_type': 'Online', 'card_present': 1}
    result3 = detector.predict(test3)
    print(f"3. ₹7,50,000 Online:")
    print(f"   Fraud Probability: {result3['fraud_probability']:.2%}")
    print(f"   Risk Level: {result3['risk_level']}")
    print(f"   Recommendation: {result3['recommendation']}")
    print(f"   Status: {'✅ CORRECT' if 0.3 <= result3['fraud_probability'] <= 0.7 else '❌ WRONG'}")
    
    # Test cases that should be APPROVED
    print("\n✅ LOW-RISK TRANSACTIONS (SHOULD BE APPROVED):")
    print("-" * 50)
    
    # Test 4: ₹123 normal transaction
    test4 = {'amount': 123, 'location': 'Hyderabad', 'transaction_type': 'POS', 'card_present': 1}
    result4 = detector.predict(test4)
    print(f"4. ₹123 POS in Hyderabad:")
    print(f"   Fraud Probability: {result4['fraud_probability']:.2%}")
    print(f"   Risk Level: {result4['risk_level']}")
    print(f"   Recommendation: {result4['recommendation']}")
    print(f"   Status: {'✅ CORRECT' if result4['fraud_probability'] < 0.15 else '❌ WRONG'}")
    
    # Test 5: ₹2,500 normal transaction
    test5 = {'amount': 2500, 'location': 'Hyderabad', 'transaction_type': 'POS', 'card_present': 1}
    result5 = detector.predict(test5)
    print(f"\n5. ₹2,500 POS in Hyderabad:")
    print(f"   Fraud Probability: {result5['fraud_probability']:.2%}")
    print(f"   Risk Level: {result5['risk_level']}")
    print(f"   Recommendation: {result5['recommendation']}")
    print(f"   Status: {'✅ CORRECT' if result5['fraud_probability'] < 0.15 else '❌ WRONG'}")
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    correct = 0
    total = 5
    
    if result1['fraud_probability'] > 0.7: correct += 1
    if result2['fraud_probability'] > 0.7: correct += 1
    if 0.3 <= result3['fraud_probability'] <= 0.7: correct += 1
    if result4['fraud_probability'] < 0.15: correct += 1
    if result5['fraud_probability'] < 0.15: correct += 1
    
    print(f"✅ {correct}/{total} test cases working correctly")
    
    if correct == total:
        print("🎉 ALL TESTS PASSED - Fraud detection system is FIXED and WORKING!")
        print("✅ High-risk transactions are properly blocked")
        print("✅ Medium-risk transactions are flagged for review")
        print("✅ Normal transactions are approved")
    else:
        print("⚠️  Some issues remain - System needs further adjustment")
    
    print("=" * 70)

if __name__ == "__main__":
    test_fixed_system()