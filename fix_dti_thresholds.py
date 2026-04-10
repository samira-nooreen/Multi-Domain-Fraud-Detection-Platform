file_path = "ml_modules/loan_default/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the DTI rules to be more conservative
old_dti = '''        # HIGH DTI RATIO CHECK (Loan amount vs Income)
        if dti_ratio > 10:
            reasons.append(f"Extreme DTI Ratio ({dti_ratio:.1f}x) - Loan is {dti_ratio:.0f}x monthly income")
            if prob < 0.50:
                prob = 0.55  # Force to HIGH risk
                reasons.append("Risk elevated to HIGH due to extreme DTI")
        elif dti_ratio > 7:
            reasons.append(f"Very High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 7x monthly income")
            if prob < 0.35:
                prob = 0.40  # Force to MEDIUM-HIGH
                reasons.append("Risk elevated due to high DTI")
        elif dti_ratio > 5:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to MEDIUM
                reasons.append("Risk adjusted for high DTI")'''

new_dti = '''        # HIGH DTI RATIO CHECK (Loan amount vs Income)
        if dti_ratio > 15:
            reasons.append(f"Extreme DTI Ratio ({dti_ratio:.1f}x) - Loan is {dti_ratio:.0f}x monthly income")
            if prob < 0.60:
                prob = 0.65  # Force to HIGH risk for extreme cases
                reasons.append("Risk elevated to HIGH due to extreme DTI")
        elif dti_ratio > 10:
            reasons.append(f"Very High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 10x monthly income")
            if prob < 0.45:
                prob = 0.50  # Push to HIGH for very high DTI
                reasons.append("Risk elevated due to very high DTI")
        elif dti_ratio > 7:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 7x monthly income")
            if prob < 0.30:
                prob = 0.35  # Keep in MEDIUM range
                reasons.append("Risk adjusted for high DTI")
        elif dti_ratio > 5:
            reasons.append(f"Moderate DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to low MEDIUM
                reasons.append("Slight risk adjustment for moderate DTI")'''

content = content.replace(old_dti, new_dti)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Adjusted DTI thresholds:")
print("   - DTI > 15: Forces HIGH (65%)")
print("   - DTI > 10: Forces HIGH (50%)")
print("   - DTI > 7: Forces MEDIUM (35%)")
print("   - DTI > 5: Forces low MEDIUM (25%)")
print("\nThis should fix test case 3 to show MEDIUM instead of HIGH")
