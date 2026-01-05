"""
Test Cases for Insurance Fraud Detection Module
"""
import sys
import os
import json

# Add parent directory to path to import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_modules.insurance_fraud.predict import InsuranceFraudDetector

def run_tests():
    print("Loading model...")
    detector = InsuranceFraudDetector()
    
    # Case 1: Legit Claim
    case1 = {
        'age': 45,
        'policy_tenure': 10,
        'policy_amount': 50000,
        'claim_amount': 5000,
        'past_claims': 0,
        'incident_hour': 14,
        'days_to_report': 1,
        'witness_present': 1,
        'police_report': 1,
        'linked_claims': 0
    }
    
    print("\n✅ TEST CASE 1: LEGIT CLAIM")
    print(f"Input: {json.dumps(case1, indent=2)}")
    result1 = detector.predict(case1)
    print(f"Output: {json.dumps(result1, indent=2)}")
    
    # Case 2: Fraud Claim (High amount, late report, no witness, linked claims)
    case2 = {
        'age': 25,
        'policy_tenure': 1,
        'policy_amount': 50000,
        'claim_amount': 45000, # High ratio
        'past_claims': 4,
        'incident_hour': 2, # Late night
        'days_to_report': 20, # Late report
        'witness_present': 0,
        'police_report': 0,
        'linked_claims': 5 # Graph anomaly
    }
    
    print("\n❌ TEST CASE 2: FRAUD CLAIM")
    print(f"Input: {json.dumps(case2, indent=2)}")
    result2 = detector.predict(case2)
    print(f"Output: {json.dumps(result2, indent=2)}")

if __name__ == "__main__":
    run_tests()
