file_path = "ml_modules/loan_default/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the ensemble logic to prioritize rule-based over ML model
old_ensemble = '''        # 3. Get Gradient Boosting (GB) Model Prediction
        try:
            # The loaded model is likely a GB or similar classifier
            p_gb = self.model.predict_proba(df)[0][1]
        except:
             # Fallback if model fails or columns mismatch
            p_gb = p_lr # Use LR as fallback
            
        # 4. Ensemble: Combine 50/50
        prob = 0.5 * p_lr + 0.5 * p_gb'''

new_ensemble = '''        # 3. Get Gradient Boosting (GB) Model Prediction (SECONDARY)
        try:
            # The loaded model is likely a GB or similar classifier
            p_gb = self.model.predict_proba(df)[0][1]
        except:
             # Fallback if model fails or columns mismatch
            p_gb = p_lr # Use LR as fallback
            
        # 4. Use LOGISTIC REGRESSION as primary (70%), ML model as secondary (30%)
        # This ensures our rule-based logic dominates
        prob = 0.7 * p_lr + 0.3 * p_gb'''

content = content.replace(old_ensemble, new_ensemble)

# Add EMI ratio and credit score rules after DTI rules
old_dti_end = '''        elif dti_ratio > 5:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to MEDIUM
                reasons.append("Slight risk adjustment for moderate DTI")'''

new_dti_end = '''        elif dti_ratio > 5:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to MEDIUM
                reasons.append("Slight risk adjustment for moderate DTI")
        
        # CREDIT SCORE RULE (VERY IMPORTANT)
        if credit_score < 500:
            if prob < 0.70:
                prob = 0.75  # Force HIGH risk for very poor credit
                reasons.append(f"Critical credit score ({credit_score:.0f}) - Very high default risk")
        elif credit_score < 600:
            if prob < 0.50:
                prob = 0.55  # Force MEDIUM-HIGH for poor credit
                reasons.append(f"Poor credit score ({credit_score:.0f}) - Elevated default risk")
        elif credit_score < 650:
            if prob < 0.35:
                prob = 0.40  # Push to MEDIUM for below-average credit
                reasons.append(f"Below-average credit score ({credit_score:.0f})")
        elif credit_score < 700:
            if prob < 0.20:
                prob = 0.25  # Slight boost for average credit
                reasons.append(f"Average credit score ({credit_score:.0f}) - Moderate risk")
        
        # EMI TO INCOME RATIO RULE (CRITICAL)
        emi_to_income_ratio = monthly_emi_approx / monthly_income if monthly_income > 0 else 100
        if emi_to_income_ratio > 0.50:  # EMI > 50% of income
            if prob < 0.70:
                prob = 0.75
                reasons.append(f"EMI burden too high ({emi_to_income_ratio:.0%} of income)")
        elif emi_to_income_ratio > 0.40:  # EMI > 40% of income
            if prob < 0.50:
                prob = 0.55
                reasons.append(f"High EMI burden ({emi_to_income_ratio:.0%} of income)")
        elif emi_to_income_ratio > 0.30:  # EMI > 30% of income
            if prob < 0.30:
                prob = 0.35
                reasons.append(f"Moderate EMI burden ({emi_to_income_ratio:.0%} of income)")
        
        # LOAN TO INCOME MULTIPLE RULE
        if loan_amount > 10 * monthly_income:
            if prob < 0.80:
                prob = 0.85
                reasons.append(f"Loan amount is {loan_amount/monthly_income:.0f}x monthly income (extreme)")
        elif loan_amount > 7 * monthly_income:
            if prob < 0.50:
                prob = 0.55
                reasons.append(f"Loan amount is {loan_amount/monthly_income:.0f}x monthly income (high)")
        elif loan_amount > 5 * monthly_income:
            if prob < 0.30:
                prob = 0.35
                reasons.append(f"Loan amount is {loan_amount/monthly_income:.0f}x monthly income (moderate)")'''

content = content.replace(old_dti_end, new_dti_end)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Changed ensemble weighting:")
print("   - Logistic Regression: 70% (dominant)")
print("   - ML Model (LightGBM): 30% (secondary)")
print("\n✅ Added critical risk rules:")
print("   1. Credit Score Rules:")
print("      - < 500: Forces 75% (HIGH)")
print("      - 500-599: Forces 55% (MEDIUM-HIGH)")
print("      - 600-649: Forces 40% (MEDIUM)")
print("      - 650-699: Forces 25% (low MEDIUM)")
print("\n   2. EMI to Income Ratio:")
print("      - > 50%: Forces 75% (HIGH)")
print("      - > 40%: Forces 55% (MEDIUM-HIGH)")
print("      - > 30%: Forces 35% (MEDIUM)")
print("\n   3. Loan to Income Multiple:")
print("      - > 10x: Forces 85% (VERY_HIGH)")
print("      - > 7x: Forces 55% (HIGH)")
print("      - > 5x: Forces 35% (MEDIUM)")
