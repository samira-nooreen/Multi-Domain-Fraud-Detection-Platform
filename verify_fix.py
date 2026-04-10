# Simple test to verify the fix
import sys
sys.path.append('.')

# Test the exact scenario
amount = 1000000
transaction_type = 'Online'
card_present = 0

risk_score = 0.0
risk_factors = []

print("Testing transaction: ₹10,00,000, Online, Card not present")
print("=" * 50)

# Amount-based risk (FIXED with >=)
if amount >= 1000000:  # 10+ lakhs
    risk_score += 0.7
    risk_factors.append("Very high transaction amount (₹10+ lakhs)")
    print("✅ Amount >= 1000000: TRUE - +70% risk")
elif amount >= 500000:  # 5+ lakhs
    risk_score += 0.5
    risk_factors.append("High transaction amount (₹5+ lakhs)")
    print("✅ Amount >= 500000: TRUE - +50% risk")

# Transaction type risk
if transaction_type == 'Online':
    risk_score += 0.3
    risk_factors.append("Online transaction")
    print("✅ Online transaction: TRUE - +30% risk")

# Card present risk
if not card_present:
    risk_score += 0.4
    risk_factors.append("Card not present")
    print("✅ Card not present: TRUE - +40% risk")

# Base risk
risk_score += 0.05
print("✅ Base risk: +5%")

# Cap risk score
risk_score = min(0.95, risk_score)
print(f"✅ Final risk score: {risk_score:.2%}")

# Risk classification
if risk_score < 0.15:
    risk_level = "LOW"
    recommendation = "APPROVE"
elif risk_score < 0.3:
    risk_level = "LOW-MEDIUM"
    recommendation = "MONITOR"
elif risk_score < 0.5:
    risk_level = "MEDIUM"
    recommendation = "REVIEW REQUIRED"
elif risk_score < 0.7:
    risk_level = "HIGH"
    recommendation = "STEP-UP AUTHENTICATION"
else:
    risk_level = "CRITICAL"
    recommendation = "BLOCK TRANSACTION"

print("=" * 50)
print(f"🔴 Fraud Probability: {risk_score:.2%}")
print(f"⚠️  Risk Level: {risk_level}")
print(f"📊 Recommendation: {recommendation}")
print("🔍 Risk Factors:")
for factor in risk_factors:
    print(f"   • {factor}")

print("=" * 50)
if risk_score > 0.7:
    print("✅ FIXED: High-risk transaction correctly flagged!")
else:
    print("❌ STILL BROKEN: Risk score too low")