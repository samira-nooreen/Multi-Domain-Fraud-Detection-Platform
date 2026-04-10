"""
Test loan default prediction with user's inputs
"""
from ml_modules.loan_default.predict import LoanDefaultPredictor

# Initialize predictor
predictor = LoanDefaultPredictor()

# Test case from user
test_data = {
    'loan_amount': 300000,
    'monthly_income': 40000,
    'credit_score': 650,
    'loan_duration': 24
}

print("="*70)
print("TESTING LOAN DEFAULT PREDICTION")
print("="*70)
print(f"\nInput Data:")
print(f"  Loan Amount: ₹{test_data['loan_amount']:,}")
print(f"  Monthly Income: ₹{test_data['monthly_income']:,}")
print(f"  Credit Score: {test_data['credit_score']}")
print(f"  Loan Duration: {test_data['loan_duration']} months")

# Calculate expected metrics
dti = test_data['loan_amount'] / test_data['monthly_income']
monthly_emi = test_data['loan_amount'] / test_data['loan_duration']
affordability = test_data['monthly_income'] / monthly_emi

print(f"\nCalculated Metrics:")
print(f"  DTI Ratio: {dti:.2f} (Loan is {dti:.1f}x monthly income)")
print(f"  Monthly EMI: ₹{monthly_emi:,.0f}")
print(f"  Affordability Index: {affordability:.2f}")

print(f"\nExpected: MEDIUM RISK (DTI is high at {dti:.1f}, but affordability is good)")
print("-"*70)

# Get prediction
result = predictor.predict(test_data)

print(f"\nACTUAL PREDICTION:")
print(f"  Default Probability: {result['default_probability']:.2%}")
print(f"  Risk Level: {result['risk_level']}")
print(f"  Decision: {result['decision']}")
print(f"  Recommendation: {result['recommendation']}")
print(f"  Risk Score: {result['risk_score']}/1000")

print("\n" + "="*70)

# Verify if it matches expected
if result['risk_level'] == 'MEDIUM':
    print("✅ SUCCESS! Prediction matches expected MEDIUM RISK")
elif result['risk_level'] == 'LOW':
    print("⚠️  Still showing LOW - DTI weighting might need adjustment")
elif result['risk_level'] in ['HIGH', 'VERY_HIGH']:
    print("🔴 Showing higher than expected - may be too conservative")
else:
    print(f"❓ Unexpected risk level: {result['risk_level']}")

print("="*70)
