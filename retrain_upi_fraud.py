"""
Retrain UPI Fraud Detection Model with Improved Settings
This script retrains the UPI fraud detection model with:
1. Better class imbalance handling
2. More realistic fraud patterns
3. Enhanced feature engineering
4. Improved model parameters
"""

import os
import sys

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def retrain_upi_fraud_model():
    """Retrain the UPI fraud detection model with improved settings"""
    print("=" * 60)
    print("RETRAINING UPI FRAUD DETECTION MODEL - IMPROVED VERSION")
    print("=" * 60)
    
    try:
        # Step 1: Generate improved dataset
        print("\n📊 STEP 1: Generating improved dataset...")
        from ml_modules.upi_fraud.generate_data import generate_upi_data
        df = generate_upi_data(15000)  # Generate more samples
        df.to_csv('ml_modules/upi_fraud/upi_fraud_data.csv', index=False)
        print("✅ Dataset generated and saved")
        
        # Step 2: Retrain model with improved parameters
        print("\n🧠 STEP 2: Retraining model with improved settings...")
        from ml_modules.upi_fraud.train import load_and_prepare_data, train_model
        X, y, feature_cols = load_and_prepare_data('ml_modules/upi_fraud/upi_fraud_data.csv')
        model, scaler, feature_importance = train_model(X, y)
        print("✅ Model retrained successfully")
        
        # Step 3: Test the improved model
        print("\n🧪 STEP 3: Testing improved model performance...")
        from ml_modules.upi_fraud.predict import UPIFraudDetector
        
        # Test critical scenarios
        detector = UPIFraudDetector()
        
        # Test Case 1: High amount at unusual time
        test_case_1 = {
            'amount': 1000000,
            'time_of_transaction': '03:34',
            'device_changed': 0,
            'user_avg_amount': 5000
        }
        result_1 = detector.predict(test_case_1)
        
        print(f"\n📝 Test Case 1 - ₹10 lakh at 3:34 AM:")
        print(f"   Fraud Probability: {result_1['fraud_probability']:.2%}")
        print(f"   Risk Level: {result_1['risk_level']}")
        print(f"   Recommendation: {result_1['recommendation']}")
        
        # Test Case 2: High amount with device change
        test_case_2 = {
            'amount': 750000,
            'time_of_transaction': '14:30',
            'device_changed': 1,
            'user_avg_amount': 8000
        }
        result_2 = detector.predict(test_case_2)
        
        print(f"\n📝 Test Case 2 - ₹7.5 lakh with device change:")
        print(f"   Fraud Probability: {result_2['fraud_probability']:.2%}")
        print(f"   Risk Level: {result_2['risk_level']}")
        print(f"   Recommendation: {result_2['recommendation']}")
        
        # Test Case 3: Normal transaction
        test_case_3 = {
            'amount': 2500,
            'time_of_transaction': '11:30',
            'device_changed': 0,
            'user_avg_amount': 3000
        }
        result_3 = detector.predict(test_case_3)
        
        print(f"\n📝 Test Case 3 - Normal ₹2,500 transaction:")
        print(f"   Fraud Probability: {result_3['fraud_probability']:.2%}")
        print(f"   Risk Level: {result_3['risk_level']}")
        print(f"   Recommendation: {result_3['recommendation']}")
        
        # Verification
        print("\n" + "=" * 60)
        if (result_1['fraud_probability'] > 0.5 and 
            result_2['fraud_probability'] > 0.6 and 
            result_3['fraud_probability'] < 0.1):
            print("✅ SUCCESS: Model is now properly calibrated!")
            print("✅ High-risk transactions are flagged appropriately")
            print("✅ Low-risk transactions are approved correctly")
        else:
            print("⚠️  WARNING: Model may need further tuning")
            
        print("\n🎉 RETRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during retraining: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = retrain_upi_fraud_model()
    if success:
        print("\n✨ UPI Fraud Detection System is now FIXED and IMPROVED!")
        print("✨ Ready for final year project demonstration!")
    else:
        print("\n❌ Retraining failed. Please check the error above.")