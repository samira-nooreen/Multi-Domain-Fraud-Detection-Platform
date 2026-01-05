"""
Test Script for Loan Default Prediction
Run this to verify the model's behavior on specific cases.
"""
import sys
import os
import json

# Add root dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml_modules.loan_default.predict import LoanDefaultPredictor

def run_tests():
    print("Loading model...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'loan_model.pkl')
    
    try:
        predictor = LoanDefaultPredictor(model_path=model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Case 1: LEGIT / LOW-RISK
    case1 = {
        'loan_amount': 8000,
        'annual_income': 60000,
        'credit_score': 710,
        'employment_length': 5,
        'dti_ratio': 0.20,
        'home_ownership': 'RENT',
        'loan_grade': 'C',
        'loan_intent': 'DEBTCONSOLIDATION'
    }
    
    print("\n✅ TEST CASE 1: LEGIT APPLICANT")
    print(f"Input: {json.dumps(case1, indent=2)}")
    result1 = predictor.predict(case1)
    print(f"Output: {json.dumps(result1, indent=2)}")
    
    # Case 2: HIGH-RISK
    case2 = {
        'loan_amount': 25000,
        'annual_income': 32000,
        'credit_score': 580,
        'employment_length': 0.4,
        'dti_ratio': 0.48,
        'home_ownership': 'RENT',
        'loan_grade': 'E',
        'loan_intent': 'PERSONAL'
    }
    
    print("\n❌ TEST CASE 2: HIGH-RISK APPLICANT")
    print(f"Input: {json.dumps(case2, indent=2)}")
    result2 = predictor.predict(case2)
    print(f"Output: {json.dumps(result2, indent=2)}")

    # Case 3: STRING INPUTS (Robustness Test)
    case3 = {
        'loan_amount': "15000",
        'annual_income': "45000",
        'credit_score': "650",
        'employment_length': "3",
        'dti_ratio': "25.5",
        'home_ownership': 'RENT',
        'loan_grade': 'C',
        'loan_intent': 'MEDICAL'
    }
    
    print("\n⚠️ TEST CASE 3: STRING INPUTS")
    try:
        result3 = predictor.predict(case3)
        print(f"Output: {json.dumps(result3, indent=2)}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run_tests()
