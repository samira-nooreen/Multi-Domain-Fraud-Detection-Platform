import re

file_path = "ml_modules/loan_default/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add input validation at the start of predict method
old_start = '''    def predict(self, data):
        """
        Predict loan default risk
        data: dict containing loan application details
        """
        # Convert dict to DataFrame
        df = pd.DataFrame([data])'''

new_start = '''    def predict(self, data):
        """
        Predict loan default risk
        data: dict containing loan application details
        """
        # INPUT VALIDATION
        try:
            loan_amount = float(data.get('loan_amount', 0))
            monthly_income = float(data.get('monthly_income', 0))
            credit_score = float(data.get('credit_score', 0))
            loan_duration = float(data.get('loan_duration', 0))
            
            # Validate ranges
            if loan_amount <= 0:
                raise ValueError(f"Invalid loan amount: {loan_amount}. Must be greater than 0.")
            if monthly_income <= 0:
                raise ValueError(f"Invalid monthly income: {monthly_income}. Must be greater than 0.")
            if credit_score < 300 or credit_score > 850:
                raise ValueError(f"Invalid credit score: {credit_score}. Must be between 300-850.")
            if loan_duration <= 0 or loan_duration > 360:
                raise ValueError(f"Invalid loan duration: {loan_duration}. Must be between 1-360 months.")
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Input validation failed: {e}")
        
        # Convert dict to DataFrame
        df = pd.DataFrame([data])'''

content = content.replace(old_start, new_start)

# Adjust risk thresholds to better match expectations
old_thresholds = '''        # Decision Engine (User Thresholds)
        # < 20% -> LOW -> Approve
        # 20-50% -> MEDIUM -> Manual Review
        # 50-80% -> HIGH -> Decline
        # > 80% -> VERY_HIGH -> Decline
        
        if prob < 0.20:
            decision = "APPROVE"
            risk_level = "LOW"
            recommendation = "Approve Application"
        elif prob < 0.50:
            decision = "MANUAL_REVIEW"
            risk_level = "MEDIUM"
            recommendation = "Refer to underwriter for manual review."
        elif prob < 0.80:
            decision = "REJECT" # User says Decline for HIGH
            risk_level = "HIGH"
            if len(reasons) > 0:
                recommendation = f"Decline: {'; '.join(reasons)}"
            else:
                recommendation = "Decline application due to high default risk."
        else:
            decision = "REJECT"
            risk_level = "VERY_HIGH"
            if len(reasons) > 0:
                recommendation = f"Decline: {'; '.join(reasons)}"
            else:
                recommendation = "Decline application due to critical default risk."'''

new_thresholds = '''        # Decision Engine (User Thresholds)
        # < 20% -> LOW -> Approve
        # 20-40% -> MEDIUM -> Manual Review
        # 40-70% -> HIGH -> Decline
        # > 70% -> VERY_HIGH -> Decline
        
        if prob < 0.20:
            decision = "APPROVE"
            risk_level = "LOW"
            recommendation = "Approve Application"
        elif prob < 0.40:
            decision = "MANUAL_REVIEW"
            risk_level = "MEDIUM"
            recommendation = "Refer to underwriter for manual review."
        elif prob < 0.70:
            decision = "REJECT"
            risk_level = "HIGH"
            if len(reasons) > 0:
                recommendation = f"Decline: {'; '.join(reasons)}"
            else:
                recommendation = "Decline application due to high default risk."
        else:
            decision = "REJECT"
            risk_level = "VERY_HIGH"
            if len(reasons) > 0:
                recommendation = f"Decline: {'; '.join(reasons)}"
            else:
                recommendation = "Decline application due to critical default risk."'''

content = content.replace(old_thresholds, new_thresholds)

# Adjust the HIGH DTI rule to not force to 35% (which is now MEDIUM)
old_dti_rule = '''        # HIGH DTI RATIO CHECK (Loan amount vs Income)
        if dti_ratio > 7:
            reasons.append(f"Very High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 7x monthly income")
            if prob < 0.25:
                prob = 0.35  # Force to MEDIUM risk range (25-50%)
                reasons.append("Risk elevated to MEDIUM due to excessive DTI")
        elif dti_ratio > 5:
            reasons.append(f"High DTI Ratio ({dti_ratio:.1f}x) - Loan exceeds 5x monthly income")
            if prob < 0.20:
                prob = 0.25  # Push to low end of MEDIUM
                reasons.append("Risk adjusted for high DTI")'''

new_dti_rule = '''        # HIGH DTI RATIO CHECK (Loan amount vs Income)
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

content = content.replace(old_dti_rule, new_dti_rule)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added input validation!")
print("✅ Adjusted risk thresholds:")
print("   - LOW: < 20%")
print("   - MEDIUM: 20-40%")
print("   - HIGH: 40-70%")
print("   - VERY_HIGH: > 70%")
print("✅ Improved DTI ratio handling")
