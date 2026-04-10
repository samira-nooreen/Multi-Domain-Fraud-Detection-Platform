"""
Demonstrate the credit card fraud detection fix - showing INR formatting
"""
from ml_modules.credit_card.predict import CreditCardFraudDetector
from currency_config import format_amount

def demonstrate_fix():
    print("=" * 60)
    print("CREDIT CARD FRAUD DETECTION - CURRENCY FIX DEMONSTRATION")
    print("=" * 60)
    
    # Initialize detector
    detector = CreditCardFraudDetector()
    
    # Test transaction data
    transaction_data = {
        'amount': 123,
        'location': 'Hyderabad',
        'transaction_type': 'POS',
        'card_present': 1
    }
    
    print("📋 Transaction Details:")
    print(f"   Amount: ₹{transaction_data['amount']}")
    print(f"   Location: {transaction_data['location']}")
    print(f"   Type: {transaction_data['transaction_type']}")
    print(f"   Card Present: {'Yes' if transaction_data['card_present'] else 'No'}")
    
    # Get prediction
    result = detector.predict(transaction_data)
    
    print(f"\n📊 Fraud Detection Results:")
    print(f"   Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Recommendation: {result['recommendation']}")
    
    # Show formatted amount with INR
    formatted_amount = format_amount(transaction_data['amount'], 'INR')
    print(f"   Formatted Amount: {formatted_amount}")
    
    print("\n" + "=" * 60)
    if '₹' in formatted_amount:
        print("✅ SUCCESS: Amount is correctly formatted in Indian Rupees!")
        print(f"   Before fix: $123.00")
        print(f"   After fix:  {formatted_amount}")
        print("✅ The currency display issue has been resolved")
    else:
        print("❌ Issue: Amount is not formatted in INR")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_fix()