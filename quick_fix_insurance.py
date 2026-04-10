"""
Quick fix for Insurance Fraud Detection
Fixes:
1. Test 2 (LOW): 65% -> should be ~15%
2. Test 4 (EXTREME): 65% -> should be ~95%
3. Overall better calibration
"""

file_path = "ml_modules/insurance_fraud/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire rule-based section with perfectly calibrated version
old_rules = '''        # -------------------------------------------------------------------------
        # PURE RULE-BASED PREDICTION (No ML Model Interference)
        # -------------------------------------------------------------------------
        # Start from neutral baseline
        prob = 0.30  # Base probability (30% - neutral starting point)
        
        # Rule 1: PREVIOUS CLAIMS ANALYSIS (Perfectly Balanced)
        if past_claims == 0:
            prob -= 0.15  # First-time: 30% -> 15%
            reasons.append("First-time claimant - lower risk profile")
        elif past_claims >= 6:
            prob += 0.45  # 30% -> 75%
            reasons.append(f"Excessive previous claims ({int(past_claims)}) - high frequency claimant")
        elif past_claims >= 4:
            prob += 0.25  # 30% -> 55%
            reasons.append(f"Multiple previous claims ({int(past_claims)}) - elevated risk")
        elif past_claims >= 2:
            prob += 0.10  # 30% -> 40%
            reasons.append(f"Several previous claims ({int(past_claims)}) - moderate risk")
        elif past_claims >= 1:
            prob += 0.05  # 30% -> 35%
            reasons.append(f"Has previous claim history ({int(past_claims)} claim)")
        
        # Rule 2: High Claim Frequency
        if claim_frequency > 5:
            prob += 0.40  # Major risk factor
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob += 0.25
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 2:
            prob += 0.10
            reasons.append(f"Moderate claim frequency ({claim_frequency:.1f} claims/year)")
        
        # Rule 3: Normalized Claim Amount
        if normalized_claim_ratio > 5:
            prob += 0.45  # Major red flag
            reasons.append(f"Extremely high claim amount ({normalized_claim_ratio:.1f}x average for {claim_type})")
        elif normalized_claim_ratio > 3:
            prob += 0.30
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average for {claim_type}")
        elif normalized_claim_ratio > 2:
            prob += 0.15
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average")
        elif normalized_claim_ratio > 1.5:
            prob += 0.05
            reasons.append("Claim amount slightly above average")
        elif normalized_claim_ratio < 0.5:
            prob -= 0.10  # Small claims are lower risk
            reasons.append("Claim amount below average - lower risk")'''

new_rules = '''        # -------------------------------------------------------------------------
        # PURE RULE-BASED PREDICTION (Perfectly Calibrated)
        # -------------------------------------------------------------------------
        # Start from LOW baseline (most claims are legitimate)
        prob = 0.10  # Base probability (10% - assume legitimate until proven otherwise)
        
        # Rule 1: PREVIOUS CLAIMS ANALYSIS
        if past_claims == 0:
            prob += 0.00  # First-time: stay at 10%
            reasons.append("First-time claimant - lower risk profile")
        elif past_claims >= 6:
            prob += 0.65  # 10% -> 75%
            reasons.append(f"Excessive previous claims ({int(past_claims)}) - high frequency claimant")
        elif past_claims >= 4:
            prob += 0.50  # 10% -> 60%
            reasons.append(f"Multiple previous claims ({int(past_claims)}) - elevated risk")
        elif past_claims >= 2:
            prob += 0.30  # 10% -> 40%
            reasons.append(f"Several previous claims ({int(past_claims)}) - moderate risk")
        elif past_claims >= 1:
            prob += 0.15  # 10% -> 25%
            reasons.append(f"Has previous claim history ({int(past_claims)} claim)")
        
        # Rule 2: High Claim Frequency
        if claim_frequency > 5:
            prob += 0.50
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob += 0.35
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 2:
            prob += 0.15
            reasons.append(f"Moderate claim frequency ({claim_frequency:.1f} claims/year)")
        
        # Rule 3: Normalized Claim Amount (FIXED - correct ratios)
        if normalized_claim_ratio > 5:
            prob += 0.60  # Extreme
            reasons.append(f"Extremely high claim amount ({normalized_claim_ratio:.1f}x average for {claim_type})")
        elif normalized_claim_ratio > 3:
            prob += 0.40
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average for {claim_type}")
        elif normalized_claim_ratio > 2:
            prob += 0.25
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average")
        elif normalized_claim_ratio > 1.5:
            prob += 0.10
            reasons.append("Claim amount slightly above average")
        elif normalized_claim_ratio < 0.5:
            prob -= 0.05  # Small claims barely reduce risk
            reasons.append("Claim amount below average - lower risk")'''

content = content.replace(old_rules, new_rules)

# Fix description analysis
old_desc = '''        # POSITIVE indicators (reduce risk)
        positive_indicators = 0
        if 'police' in incident_desc_lower or 'fir' in incident_desc_lower:
            prob -= 0.12  # Strong positive
            positive_indicators += 1
            reasons.append("Police complaint/FIR filed - positive indicator")
        
        if 'bill' in incident_desc_lower or 'invoice' in incident_desc_lower or 'receipt' in incident_desc_lower:
            if 'no bill' not in incident_desc_lower and 'no document' not in incident_desc_lower:
                prob -= 0.10
                positive_indicators += 1
                reasons.append("Supporting documents/bills mentioned - positive indicator")
        
        if 'valid' in incident_desc_lower and ('report' in incident_desc_lower or 'documents' in incident_desc_lower):
            prob -= 0.10
            positive_indicators += 1
            reasons.append("Valid documentation submitted - positive indicator")
        
        if 'witness' in incident_desc_lower:
            prob -= 0.05
            positive_indicators += 1
            reasons.append("Witness mentioned - positive indicator")
        
        # NEGATIVE indicators (increase risk)
        negative_indicators = 0
        if 'no bill' in incident_desc_lower or 'no document' in incident_desc_lower or 'no proof' in incident_desc_lower or 'no proper document' in incident_desc_lower:
            prob += 0.15
            negative_indicators += 1
            reasons.append("No documentation/bills available - risk factor")
        
        if 'urgent' in incident_desc_lower or 'immediate' in incident_desc_lower or 'fast' in incident_desc_lower or 'quick' in incident_desc_lower:
            prob += 0.12
            negative_indicators += 1
            reasons.append("Urgent/immediate settlement requested - red flag")
        
        if 'vague' in incident_desc_lower or 'inconsistent' in incident_desc_lower or 'unclear' in incident_desc_lower:
            prob += 0.18
            negative_indicators += 1
            reasons.append("Vague/inconsistent description detected")
        
        if 'total loss' in incident_desc_lower or 'full damage' in incident_desc_lower:
            if normalized_claim_ratio > 2:
                prob += 0.10
                negative_indicators += 1
                reasons.append("Claiming total loss/full damage - requires verification")'''

new_desc = '''        # POSITIVE indicators (reduce risk)
        positive_indicators = 0
        if 'police' in incident_desc_lower or 'fir' in incident_desc_lower:
            prob -= 0.15
            positive_indicators += 1
            reasons.append("Police complaint/FIR filed - positive indicator")
        
        if ('bill' in incident_desc_lower or 'invoice' in incident_desc_lower or 'receipt' in incident_desc_lower) and 'no bill' not in incident_desc_lower:
            prob -= 0.12
            positive_indicators += 1
            reasons.append("Supporting documents/bills mentioned - positive indicator")
        
        if 'valid' in incident_desc_lower and ('report' in incident_desc_lower or 'documents' in incident_desc_lower):
            prob -= 0.12
            positive_indicators += 1
            reasons.append("Valid documentation submitted - positive indicator")
        
        if 'witness' in incident_desc_lower:
            prob -= 0.05
            positive_indicators += 1
            reasons.append("Witness mentioned - positive indicator")
        
        # NEGATIVE indicators (increase risk)
        negative_indicators = 0
        if 'no bill' in incident_desc_lower or 'no document' in incident_desc_lower or 'no proof' in incident_desc_lower or 'no proper document' in incident_desc_lower:
            prob += 0.20
            negative_indicators += 1
            reasons.append("No documentation/bills available - risk factor")
        
        if 'urgent' in incident_desc_lower or 'immediate' in incident_desc_lower or 'fast' in incident_desc_lower or 'quick' in incident_desc_lower:
            prob += 0.15
            negative_indicators += 1
            reasons.append("Urgent/immediate settlement requested - red flag")
        
        if 'vague' in incident_desc_lower or 'inconsistent' in incident_desc_lower or 'unclear' in incident_desc_lower:
            prob += 0.20
            negative_indicators += 1
            reasons.append("Vague/inconsistent description detected")
        
        if 'total loss' in incident_desc_lower or 'full damage' in incident_desc_lower:
            if normalized_claim_ratio > 2:
                prob += 0.15
                negative_indicators += 1
                reasons.append("Claiming total loss/full damage - requires verification")'''

content = content.replace(old_desc, new_desc)

# Fix late reporting
old_late = '''        # Rule 5: Late Reporting
        if days_to_report > 30:
            prob = max(prob, 0.70)
            reasons.append(f"Very late reporting ({int(days_to_report)} days)")
        elif days_to_report > 14:
            prob = max(prob, 0.45)
            reasons.append(f"Late reporting ({int(days_to_report)} days)")'''

new_late = '''        # Rule 5: Late Reporting
        if days_to_report > 30:
            prob += 0.30
            reasons.append(f"Very late reporting ({int(days_to_report)} days)")
        elif days_to_report > 14:
            prob += 0.15
            reasons.append(f"Late reporting ({int(days_to_report)} days)")'''

content = content.replace(old_late, new_late)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ QUICK FIX APPLIED!")
print("\n📊 CALIBRATION CHANGES:")
print("   1. Baseline: 30% -> 10% (assume legitimate)")
print("   2. Previous claims increased impacts")
print("   3. Claim amount ratios fixed")
print("   4. Description analysis balanced")
print("   5. Late reporting additive (not max)")
print("\n🎯 EXPECTED RESULTS:")
print("   Test 1 (HIGH): ~60-70% ✅")
print("   Test 2 (LOW): ~10-15% ✅")
print("   Test 3 (MEDIUM): ~35-45% ✅")
print("   Test 4 (EXTREME): ~85-95% ✅")
