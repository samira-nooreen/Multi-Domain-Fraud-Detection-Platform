"""
Insurance Claim Fraud - Enhanced Dataset Generator
Generates synthetic insurance claims data with graph-like connections and rich features
"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)

def generate_insurance_data(n_samples=5000):
    """Generate synthetic insurance claim data with rich features"""
    data = []
    
    # Simulate groups for graph connections
    groups = [f"GRP_{i}" for i in range(1, 100)]
    
    for i in range(n_samples):
        # Policy details
        policy_tenure = np.random.randint(1, 30)
        age = np.random.randint(18, 80)
        policy_type = np.random.choice(['Comprehensive', 'Third Party'], p=[0.7, 0.3])
        policy_amount = np.random.choice([10000, 25000, 50000, 100000, 200000])
        
        # Claim details
        claim_amount = np.random.lognormal(9, 1)
        past_claims = np.random.poisson(0.5)
        
        # Incident details
        incident_hour = np.random.randint(0, 24)
        days_since_inception = np.random.randint(10, 3650)
        days_to_report = np.random.exponential(2)
        
        # Risk factors
        witness_present = np.random.choice([0, 1], p=[0.2, 0.8])
        police_report = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # Graph/Network features (Simulated)
        # Shared address or phone number with other claimants
        shared_info = np.random.choice([0, 1], p=[0.9, 0.1]) 
        group_id = random.choice(groups) if shared_info else f"IND_{i}"
        linked_claims = np.random.randint(1, 10) if shared_info else 0
        
        # Derived features
        claim_ratio = claim_amount / policy_amount
        
        # Fraud logic (Anomaly generation)
        is_fraud = 0
        fraud_score = 0
        
        if days_to_report > 14: fraud_score += 0.3
        if claim_ratio > 0.8: fraud_score += 0.4
        if past_claims > 3: fraud_score += 0.3
        if incident_hour < 5: fraud_score += 0.2
        if days_since_inception < 30: fraud_score += 0.25
        if linked_claims > 3: fraud_score += 0.35 # Graph feature impact
        
        if fraud_score > 0.7:
            is_fraud = 1
            # Make fraudulent claims look anomalous
            claim_amount *= 1.2
            days_to_report += 10
            
        data.append({
            'age': age,
            'policy_tenure': policy_tenure,
            'policy_amount': policy_amount,
            'claim_amount': round(claim_amount, 2),
            'claim_ratio': round(claim_ratio, 2),
            'past_claims': past_claims,
            'incident_hour': incident_hour,
            'days_to_report': round(days_to_report, 1),
            'witness_present': witness_present,
            'police_report': police_report,
            'linked_claims': linked_claims, # Graph feature
            'is_fraud': is_fraud
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_insurance_data()
    df.to_csv('insurance_data.csv', index=False)
    print("Saved to insurance_data.csv")
