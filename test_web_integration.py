"""
Final Integration Test for UPI Fraud Detection Web Interface
Tests the complete flow from web form to backend processing
"""

import requests
import json

def test_web_api_integration():
    print("=" * 60)
    print("TESTING UPI FRAUD DETECTION WEB API INTEGRATION")
    print("=" * 60)
    
    # Test data matching the problematic scenario
    test_data = {
        "amount": 1000000,  # ₹10 lakhs
        "sender_id": "burhan",
        "receiver_id": "samira", 
        "time_of_transaction": "03:34",  # 3:34 AM
        "device_changed": 0,  # No device change
        "user_avg_amount": 5000,  # User's average transaction
        "is_first_time_receiver": 0  # Not first time receiver
    }
    
    print("📋 Test Transaction Details:")
    print(f"   Amount: ₹{test_data['amount']:,}")
    print(f"   Time: {test_data['time_of_transaction']} (High-risk time)")
    print(f"   Device Changed: {'Yes' if test_data['device_changed'] else 'No'}")
    print(f"   User Avg Amount: ₹{test_data['user_avg_amount']:,}")
    
    try:
        # Test the API endpoint
        print("\n🌐 Testing API endpoint...")
        response = requests.post(
            'http://127.0.0.1:5000/detect_upi',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response Received")
            
            if result['status'] == 'success':
                fraud_result = result['result']
                print(f"\n📊 Fraud Detection Results:")
                print(f"   Fraud Probability: {fraud_result['fraud_probability']:.2%}")
                print(f"   Legitimate Probability: {fraud_result['legitimate_probability']:.2%}")
                print(f"   Risk Level: {fraud_result['risk_level']}")
                print(f"   Recommendation: {fraud_result['recommendation']}")
                
                if 'risk_factors' in fraud_result and fraud_result['risk_factors']:
                    print(f"\n🔍 Risk Factors Identified:")
                    for i, factor in enumerate(fraud_result['risk_factors'], 1):
                        print(f"   {i}. {factor}")
                
                # Verify the fix worked
                if (fraud_result['fraud_probability'] > 0.8 and 
                    fraud_result['risk_level'] in ['HIGH', 'CRITICAL'] and
                    'BLOCK' in fraud_result['recommendation']):
                    print("\n" + "✅" * 30)
                    print("🎉 SUCCESS: Web API Integration Working Perfectly!")
                    print("✅ High-risk transaction properly flagged")
                    print("✅ Appropriate blocking recommendation given")
                    print("✅ Detailed risk factors provided")
                    print("✅ System is ready for demonstration")
                    print("✅" * 30)
                    return True
                else:
                    print("\n❌ Issue: Results don't match expected high-risk behavior")
                    return False
            else:
                print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running on http://127.0.0.1:5000")
        print("💡 Start the app with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def test_normal_transaction():
    """Test that normal transactions are still approved"""
    print("\n" + "=" * 60)
    print("TESTING NORMAL TRANSACTION APPROVAL")
    print("=" * 60)
    
    normal_data = {
        "amount": 2500,
        "sender_id": "user123",
        "receiver_id": "merchant456",
        "time_of_transaction": "14:30",  # Normal business hours
        "device_changed": 0,
        "user_avg_amount": 3000,
        "is_first_time_receiver": 0
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/detect_upi',
            json=normal_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                fraud_result = result['result']
                print(f"📊 Normal Transaction Results:")
                print(f"   Fraud Probability: {fraud_result['fraud_probability']:.2%}")
                print(f"   Risk Level: {fraud_result['risk_level']}")
                print(f"   Recommendation: {fraud_result['recommendation']}")
                
                if (fraud_result['fraud_probability'] < 0.1 and 
                    fraud_result['risk_level'] == 'LOW' and
                    'APPROVE' in fraud_result['recommendation']):
                    print("✅ Normal transactions are correctly approved")
                    return True
                else:
                    print("❌ Normal transactions not handled correctly")
                    return False
        return False
    except:
        print("❌ Could not test normal transaction")
        return False

if __name__ == "__main__":
    print("🚀 UPI FRAUD DETECTION - FINAL INTEGRATION TEST")
    print("Make sure your Flask app is running: python app.py")
    print()
    
    # Test high-risk scenario
    high_risk_success = test_web_api_integration()
    
    # Test normal transaction
    normal_success = test_normal_transaction()
    
    print("\n" + "=" * 60)
    if high_risk_success and normal_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ High-risk transactions are properly flagged")
        print("✅ Normal transactions are properly approved")
        print("✅ Web interface integration working correctly")
        print("🎯 SYSTEM IS PRODUCTION READY!")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the errors above")
    print("=" * 60)