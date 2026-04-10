import re

file_path = "ml_modules/loan_default/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add hard rules for high DTI after the ensemble calculation
old_section = '''        # Override for specific edge cases (Hard Rules)
        reasons = []
        
        # Critical Affordability Check
        if affordability_index < 1.0:'''

new_section = '''        # Override for specific edge cases (Hard Rules)
        reasons = []
        
        # HIGH DTI RATIO CHECK (Loan amount vs Income)
        if dti_ratio > 7:
            reasons.append(f"Very High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 7x monthly income")
            if prob < 0.25:
                prob = 0.35  # Force to MEDIUM risk range (25-50%)
                reasons.append("Risk elevated to MEDIUM due to excessive DTI")
        elif dti_ratio > 5:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to low end of MEDIUM
                reasons.append("Risk adjusted for high DTI")
        
        # Critical Affordability Check
        if affordability_index < 1.0:'''

content = content.replace(old_section, new_section)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added hard rules for high DTI ratios!")
print("✅ DTI > 7x will now force MEDIUM risk (35% probability)")
print("✅ DTI > 5x will now push to lower MEDIUM risk (25% probability)")
