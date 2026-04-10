file_path = "ml_modules/insurance_fraud/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix field mapping to match frontend inputs
old_mapping = '''        # Extract core inputs
        claim_amount = get_float('claim_amount', 0)
        past_claims = get_float('past_claims', 0)
        policy_tenure = get_float('policy_tenure', 5)  # Years
        policy_amount = get_float('policy_amount', 50000)
        days_to_report = get_float('days_to_report', 1)'''

new_mapping = '''        # Extract core inputs - Map frontend fields to model fields
        claim_amount = get_float('claim_amount', 0)
        
        # Map previous_claim_count (frontend) to past_claims (model)
        past_claims = get_float('previous_claim_count', get_float('past_claims', 0))
        
        # Use reasonable defaults for missing fields
        policy_tenure = get_float('policy_tenure', 5)  # Years
        policy_amount = get_float('policy_amount', max(claim_amount * 1.5, 50000))
        days_to_report = get_float('days_to_report', 1)'''

content = content.replace(old_mapping, new_mapping)

# Fix incident description field mapping
old_incident = '''        incident_desc = data.get('incident', '').lower()
        incident_severity = 1  # Default'''

new_incident = '''        # Map incident_description (frontend) to incident (model)
        incident_desc = data.get('incident_description', data.get('incident', '')).lower()
        incident_severity = 1  # Default'''

content = content.replace(old_incident, new_incident)

# Improve risk classification thresholds
old_thresholds = '''        # -------------------------------------------------------------------------
        # RISK CLASSIFICATION (User Thresholds)
        # -------------------------------------------------------------------------
        # < 10%: LOW -> Approve
        # 10-20%: MEDIUM -> Manual Review
        # 20-80%: HIGH -> Manual Review / Decline
        # > 80%: VERY_HIGH -> Decline
        
        if prob < 0.10:
            risk_level = "LOW"
            recommendation = "Approve"
        elif prob < 0.20:
            risk_level = "MEDIUM"
            recommendation = "Manual Review"
        elif prob < 0.80:
            risk_level = "HIGH"
            recommendation = "Manual Review / Possibly Decline"
        else:
            risk_level = "VERY_HIGH"
            recommendation = "Decline"
        
        is_fraud = prob > 0.20  # Flag for manual review threshold'''

new_thresholds = '''        # -------------------------------------------------------------------------
        # RISK CLASSIFICATION (User Thresholds)
        # -------------------------------------------------------------------------
        # < 20%: LOW -> Approve
        # 20-50%: MEDIUM -> Manual Review
        # 50-80%: HIGH -> Decline
        # > 80%: VERY_HIGH -> Decline
        
        if prob < 0.20:
            risk_level = "LOW"
            recommendation = "Approve Claim"
        elif prob < 0.50:
            risk_level = "MEDIUM"
            recommendation = "Manual Review Required"
        elif prob < 0.80:
            risk_level = "HIGH"
            recommendation = "Decline - High Fraud Risk"
        else:
            risk_level = "VERY_HIGH"
            recommendation = "Decline - Critical Fraud Indicators"
        
        is_fraud = prob > 0.50  # Flag for high risk threshold'''

content = content.replace(old_thresholds, new_thresholds)

# Add input validation and better error handling
old_predict_start = '''    def predict(self, data):
        """
        XGBoost-based Insurance Fraud Detection with Advanced Feature Engineering
        """
        # -------------------------------------------------------------------------
        # FEATURE ENGINEERING & RISK ASSESSMENT
        # -------------------------------------------------------------------------'''

new_predict_start = '''    def predict(self, data):
        """
        XGBoost-based Insurance Fraud Detection with Advanced Feature Engineering
        """
        # INPUT VALIDATION
        try:
            claim_amount = float(data.get('claim_amount', 0))
            if claim_amount <= 0:
                raise ValueError("Claim amount must be greater than 0")
            
            previous_claims = int(data.get('previous_claim_count', data.get('past_claims', 0)))
            if previous_claims < 0:
                raise ValueError("Previous claim count cannot be negative")
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Input validation failed: {e}")
        
        # -------------------------------------------------------------------------
        # FEATURE ENGINEERING & RISK ASSESSMENT
        # -------------------------------------------------------------------------'''

content = content.replace(old_predict_start, new_predict_start)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed field mapping (previous_claim_count -> past_claims)")
print("✅ Fixed incident description mapping")
print("✅ Improved risk thresholds:")
print("   - LOW: < 20%")
print("   - MEDIUM: 20-50%")
print("   - HIGH: 50-80%")
print("   - VERY_HIGH: > 80%")
print("✅ Added input validation")
