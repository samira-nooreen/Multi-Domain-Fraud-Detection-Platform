file_path = "ml_modules/insurance_fraud/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the model prediction section to use pure rule-based
old_model_section = '''        # -------------------------------------------------------------------------
        # MODEL PREDICTION (XGBoost)
        # -------------------------------------------------------------------------
        
        if self.model is not None:
            try:
                features = [
                    'age', 'policy_tenure', 'policy_amount', 'claim_amount', 'claim_ratio',
                    'past_claims', 'incident_hour', 'days_to_report', 'witness_present',
                    'police_report', 'linked_claims'
                ]
                
                df = pd.DataFrame([input_data])[features]
                X_scaled = self.scaler.transform(df)
                prob = self.model.predict_proba(X_scaled)[0][1]
            except Exception as e:
                print(f"Model prediction error: {e}")
                prob = 0.3  # Fallback to medium risk
        else:
            # No model loaded - use heuristic
            prob = 0.3'''

new_model_section = '''        # -------------------------------------------------------------------------
        # PURE RULE-BASED PREDICTION (No ML Model Interference)
        # -------------------------------------------------------------------------
        # Start from neutral baseline
        prob = 0.30  # Base probability (30% - neutral starting point)'''

content = content.replace(old_model_section, new_model_section)

# Now update the rules to be perfectly balanced from the 30% baseline
old_rules_start = '''        # Rule 1: PREVIOUS CLAIMS ANALYSIS (Balanced)
        if past_claims == 0:
            prob = min(prob, 0.15)  # First-time claimants are lower risk
            reasons.append("First-time claimant - lower risk profile")
        elif past_claims >= 6:
            prob = max(prob, 0.75)
            reasons.append(f"Excessive previous claims ({int(past_claims)}) - high frequency claimant")
        elif past_claims >= 4:
            prob = max(prob, 0.55)
            reasons.append(f"Multiple previous claims ({int(past_claims)}) - elevated risk")
        elif past_claims >= 2:
            prob = max(prob, 0.35)
            reasons.append(f"Several previous claims ({int(past_claims)}) - moderate risk")
        elif past_claims >= 1:
            prob = max(prob, 0.25)
            reasons.append(f"Has previous claim history ({int(past_claims)} claim)")'''

new_rules_start = '''        # Rule 1: PREVIOUS CLAIMS ANALYSIS (Perfectly Balanced)
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
            reasons.append(f"Has previous claim history ({int(past_claims)} claim)")'''

content = content.replace(old_rules_start, new_rules_start)

# Fix claim frequency rules
old_freq = '''        # Rule 2: High Claim Frequency (> 3 per year is concerning)
        if claim_frequency > 5:
            prob = max(prob, 0.85)
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob = max(prob, 0.65)
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")'''

new_freq = '''        # Rule 2: High Claim Frequency
        if claim_frequency > 5:
            prob += 0.40  # Major risk factor
            reasons.append(f"Very high claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 3:
            prob += 0.25
            reasons.append(f"High claim frequency ({claim_frequency:.1f} claims/year)")
        elif claim_frequency > 2:
            prob += 0.10
            reasons.append(f"Moderate claim frequency ({claim_frequency:.1f} claims/year)")'''

content = content.replace(old_freq, new_freq)

# Fix normalized claim amount rules
old_claim = '''        # Rule 3: Normalized Claim Amount (Balanced thresholds)
        if normalized_claim_ratio > 5:
            prob = max(prob, 0.80)
            reasons.append(f"Extremely high claim amount ({normalized_claim_ratio:.1f}x average for {claim_type})")
        elif normalized_claim_ratio > 3:
            prob = max(prob, 0.60)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average for {claim_type}")
        elif normalized_claim_ratio > 2:
            prob = max(prob, 0.45)
            reasons.append(f"Claim amount {normalized_claim_ratio:.1f}x higher than average")
        elif normalized_claim_ratio < 0.5:
            prob = min(prob, 0.20)  # Small claims are lower risk
            reasons.append("Claim amount below average - lower risk")'''

new_claim = '''        # Rule 3: Normalized Claim Amount
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

content = content.replace(old_claim, new_claim)

# Fix description analysis to be more balanced
old_desc = '''        # POSITIVE indicators (reduce risk slightly, not too much)
        positive_indicators = 0
        if 'police' in incident_desc_lower or 'fir' in incident_desc_lower:
            prob = max(0.10, prob - 0.10)  # Police report helps but doesn't eliminate risk
            positive_indicators += 1
            reasons.append("Police complaint/FIR filed - positive indicator")
        
        if 'bill' in incident_desc_lower or 'invoice' in incident_desc_lower or 'receipt' in incident_desc_lower:
            if 'no bill' not in incident_desc_lower and 'no document' not in incident_desc_lower:
                prob = max(0.10, prob - 0.08)
                positive_indicators += 1
                reasons.append("Supporting documents/bills mentioned - positive indicator")
        
        if 'report' in incident_desc_lower or 'medical' in incident_desc_lower or 'doctor' in incident_desc_lower:
            if 'valid' in incident_desc_lower or 'submitted' in incident_desc_lower:
                prob = max(0.10, prob - 0.10)
                positive_indicators += 1
                reasons.append("Valid professional reports/documentation")
        
        if 'witness' in incident_desc_lower:
            prob = max(0.10, prob - 0.05)
            positive_indicators += 1
            reasons.append("Witness mentioned - positive indicator")
        
        # NEGATIVE indicators (increase risk)
        negative_indicators = 0
        if 'no bill' in incident_desc_lower or 'no document' in incident_desc_lower or 'no proof' in incident_desc_lower:
            prob = min(0.95, prob + 0.12)
            negative_indicators += 1
            reasons.append("No documentation/bills available - risk factor")
        
        if 'urgent' in incident_desc_lower or 'immediate' in incident_desc_lower or 'fast' in incident_desc_lower or 'quick' in incident_desc_lower:
            prob = min(0.95, prob + 0.12)
            negative_indicators += 1
            reasons.append("Urgent/immediate settlement requested - red flag")
        
        if 'vague' in incident_desc_lower or 'inconsistent' in incident_desc_lower or 'unclear' in incident_desc_lower:
            prob = min(0.95, prob + 0.15)
            negative_indicators += 1
            reasons.append("Vague/inconsistent description detected")
        
        if 'total loss' in incident_desc_lower or 'full damage' in incident_desc_lower:
            if normalized_claim_ratio > 2:
                prob = min(0.95, prob + 0.10)
                negative_indicators += 1
                reasons.append("Claiming total loss/full damage - requires verification")'''

new_desc = '''        # POSITIVE indicators (reduce risk)
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

content = content.replace(old_desc, new_desc)

# Clamp probability between 0.01 and 0.99
old_clamp = '''        # -------------------------------------------------------------------------
        # RISK CLASSIFICATION (Balanced Thresholds)'''

new_clamp = '''        # Ensure probability is within valid range
        prob = max(0.01, min(0.99, prob))
        
        # -------------------------------------------------------------------------
        # RISK CLASSIFICATION (Balanced Thresholds)'''

content = content.replace(old_clamp, new_clamp)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ SWITCHED TO PURE RULE-BASED PREDICTION!")
print("\n📊 NEW SYSTEM:")
print("   - Baseline: 30% (neutral)")
print("   - No XGBoost model interference")
print("   - Fully transparent and explainable")
print("\n🎯 HOW IT WORKS:")
print("   1. Start at 30%")
print("   2. Add/subtract based on rules")
print("   3. Clamp between 1% and 99%")
print("   4. Classify risk level")
print("\n✅ BENEFITS:")
print("   - Predictable results")
print("   - No model bias")
print("   - Easy to tune")
print("   - Fully explainable decisions")
