"""
Test the credit card fraud detection with INR currency formatting
"""
import requests
import json

def test_credit_card_inr():
    print("=" * 50)
    print("TESTING CREDIT CARD FRAUD DETECTION - INR FORMAT")
    print("=" * 50)
    
    # Test data
    test_data = {
        "amount": 123,
        "location": "Hyderabad",
        "transaction_type": "POS",
        "card_present": 1
    }
    
    print("📋 Test Transaction Details:")
    print(f"   Amount: ₹{test_data['amount']}")
    print(f"   Location: {test_data['location']}")
    print(f"   Transaction Type: {test_data['transaction_type']}")
    print(f"   Card Present: {'Yes' if test_data['card_present'] else 'No'}")
    
    try:
        # Test the API endpoint
        print("\n🌐 Testing API endpoint...")
        response = requests.post(
            'http://127.0.0.1:5000/detect_credit',
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
                print(f"   Risk Level: {fraud_result['risk_level']}")
                print(f"   Recommendation: {fraud_result['recommendation']}")
                if 'formatted_amount' in fraud_result:
                    print(f"   Formatted Amount: {fraud_result['formatted_amount']}")
                
                # Verify the fix worked
                if 'formatted_amount' in fraud_result and '₹' in fraud_result['formatted_amount']:
                    print("\n✅ SUCCESS: Amount is now displayed in Indian Rupees!")
                    print(f"   Display: {fraud_result['formatted_amount']}")
                    return True
                else:
                    print("\n❌ Issue: Amount not formatted in INR")
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

if __name__ == "__main__":
    print("🚀 CREDIT CARD FRAUD DETECTION - CURRENCY FIX TEST")
    print("Make sure your Flask app is running: python app.py")
    print()
    
    success = test_credit_card_inr()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST PASSED!")
        print("✅ Credit card transactions now display amounts in ₹ (INR)")
        print("✅ System is working correctly")
    else:
        print("❌ TEST FAILED")
        print("Please check the errors above")
    print("=" * 50)