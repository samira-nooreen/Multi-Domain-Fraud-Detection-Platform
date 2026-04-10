"""
Test credit card fraud detection endpoint
"""
import requests

# Test the endpoint
url = "http://127.0.0.1:5000/detect_credit"

# Test data
test_data = {
    "amount": 1000000,
    "location": "Hyderabad",
    "transaction_type": "Online",
    "card_present": 0
}

print("Testing Credit Card Fraud Detection Endpoint...")
print("=" * 60)
print(f"URL: {url}")
print(f"Data: {test_data}")
print("=" * 60)

try:
    response = requests.post(url, json=test_data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("\n✅ Endpoint is working correctly!")
            print(f"Fraud Probability: {result['result']['fraud_probability']:.2%}")
            print(f"Risk Level: {result['result']['risk_level']}")
            print(f"Recommendation: {result['result']['recommendation']}")
        else:
            print(f"\n❌ Error: {result.get('message')}")
    else:
        print(f"\n❌ Request failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to server. Is it running?")
except Exception as e:
    print(f"\n❌ Error: {e}")
