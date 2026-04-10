file_path = "ml_modules/insurance_fraud/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add more aggressive rule-based boosting for different scenarios
old_rules = '''        # Rule 1: Excessive Previous Claims
        if past_claims > 10:
            prob = max(prob, 0.85)
            reasons.append(f"Excessive previous claims ({int(past_claims)})")
        
        # Rule 2: High Claim Frequency (> 5 per year)
        if claim_frequency > 5:
            prob = max(prob, 0.90)
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob = max(prob, 0.65)
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")
        
        # Rule 3: Normalized Claim Amount (>> Average)
        if normalized_claim_ratio > 3:
            prob = max(prob, 0.75)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average for {claim_type}")
        elif normalized_claim_ratio > 2:
            prob = max(prob, 0.50)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average")
        
        # Rule 4: Late Reporting
        if days_to_report > 30:
            prob = max(prob, 0.70)
            reasons.append(f"Very late reporting ({int(days_to_report)} days)")
        elif days_to_report > 14:
            prob = max(prob, 0.45)
            reasons.append(f"Late reporting ({int(days_to_report)} days)")'''

new_rules = '''        # Rule 1: NO PREVIOUS CLAIMS - Low Risk Indicator
        if past_claims == 0:
            prob = min(prob, 0.15)  # Cap at 15% for first-time claimants
            reasons.append("First-time claimant - lower risk")
        
        # Rule 2: Excessive Previous Claims
        if past_claims > 10:
            prob = max(prob, 0.85)
            reasons.append(f"Excessive previous claims ({int(past_claims)})")
        elif past_claims > 5:
            prob = max(prob, 0.60)
            reasons.append(f"Multiple previous claims ({int(past_claims)})")
        elif past_claims > 3:
            prob = max(prob, 0.40)
            reasons.append(f"Several previous claims ({int(past_claims)})")
        
        # Rule 3: High Claim Frequency (> 5 per year)
        if claim_frequency > 5:
            prob = max(prob, 0.90)
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob = max(prob, 0.65)
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")
        
        # Rule 4: Normalized Claim Amount (>> Average)
        if normalized_claim_ratio > 5:
            prob = max(prob, 0.85)
            reasons.append(f"Extremely high claim amount ({normalized_claim_ratio:.1f}x average for {claim_type})")
        elif normalized_claim_ratio > 3:
            prob = max(prob, 0.65)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average for {claim_type}")
        elif normalized_claim_ratio > 2:
            prob = max(prob, 0.45)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average")
        elif normalized_claim_ratio < 0.5:
            prob = min(prob, 0.20)  # Small claims are lower risk
            reasons.append("Claim amount below average - lower risk")
        
        # Rule 5: Late Reporting
        if days_to_report > 30:
            prob = max(prob, 0.70)
            reasons.append(f"Very late reporting ({int(days_to_report)} days)")
        elif days_to_report > 14:
            prob = max(prob, 0.45)
            reasons.append(f"Late reporting ({int(days_to_report)} days)")'''

content = content.replace(old_rules, new_rules)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added more granular risk rules:")
print("   - First-time claimants capped at 15%")
print("   - Multiple claims (5+) boosted to 60%")
print("   - Extreme claim amounts (5x) boosted to 85%")
print("   - Small claims capped at 20%")
print("✅ Better differentiation between risk levels")
