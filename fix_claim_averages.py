file_path = "ml_modules/insurance_fraud/predict.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the average claim amounts to be more realistic
old_averages = '''        # 1. NORMALIZED CLAIM AMOUNT (Claim Ratio)
        # Average claim amounts by type (industry benchmarks)
        claim_type_averages = {
            'accident': 5000,
            'theft': 3000,
            'health': 8000,
            'fire': 15000,
            'other': 5000
        }'''

new_averages = '''        # 1. NORMALIZED CLAIM AMOUNT (Claim Ratio)
        # Average claim amounts by type (industry benchmarks in INR)
        claim_type_averages = {
            'accident': 100000,  # ₹1 Lakh average for accident
            'theft': 150000,     # ₹1.5 Lakhs for theft
            'health': 75000,     # ₹75K for health
            'fire': 250000,      # ₹2.5 Lakhs for fire
            'other': 100000      # ₹1 Lakh default
        }'''

content = content.replace(old_averages, new_averages)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed average claim amounts to realistic INR values:")
print("   - Accident: ₹1,00,000")
print("   - Theft: ₹1,50,000")
print("   - Health: ₹75,000")
print("   - Fire: ₹2,50,000")
print("   - Other: ₹1,00,000")
