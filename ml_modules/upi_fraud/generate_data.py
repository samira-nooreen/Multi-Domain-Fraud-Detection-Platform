"""
UPI Fraud Detection - Dataset Generator
Generates realistic synthetic UPI transaction data for training with minimal inputs
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_upi_data(n_samples=10000):
    """Generate synthetic UPI transaction data with minimal inputs"""
    
    data = []
    
    for i in range(n_samples):
        # Minimal inputs from user
        amount = np.random.lognormal(5, 2)  # Log-normal distribution for amounts
        
        # Generate derived features from minimal inputs
        # Time features (derived from time_of_transaction)
        hour = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)
        
        # User behavior features (derived from sender_id and receiver_id)
        transaction_frequency = np.random.poisson(5)  # Average transactions per day
        avg_transaction_amount = np.random.lognormal(4.5, 1.5)
        account_age_days = np.random.randint(1, 3650)
        
        # Device features (direct from device_changed input)
        device_change = np.random.choice([0, 1], p=[0.95, 0.05])
        
        # Other derived features
        location_change = np.random.choice([0, 1], p=[0.90, 0.10])
        transactions_last_hour = np.random.poisson(0.5)
        transactions_last_day = np.random.poisson(3)
        merchant_risk_score = np.random.uniform(0, 1)
        new_merchant = np.random.choice([0, 1], p=[0.80, 0.20])
        failed_attempts = np.random.poisson(0.2)
        
        # Determine fraud based on risk factors
        fraud_score = 0
        
        # High amount transactions
        if amount > 50000:
            fraud_score += 0.3
        
        # Unusual hours (late night)
        if hour >= 23 or hour <= 5:
            fraud_score += 0.2
        
        # High transaction frequency
        if transactions_last_hour > 3:
            fraud_score += 0.25
        
        # Device/location changes
        if device_change == 1:
            fraud_score += 0.15
        if location_change == 1:
            fraud_score += 0.15
        
        # High merchant risk
        if merchant_risk_score > 0.7:
            fraud_score += 0.2
        
        # Failed attempts
        if failed_attempts > 2:
            fraud_score += 0.25
        
        # New account with high amount
        if account_age_days < 30 and amount > 10000:
            fraud_score += 0.3
        
        # Determine fraud label (with some randomness)
        is_fraud = 1 if fraud_score > 0.5 + np.random.normal(0, 0.1) else 0
        
        data.append({
            'transaction_id': f'UPI{i:06d}',
            'amount': round(amount, 2),
            'hour': hour,
            'day_of_week': day_of_week,
            'transaction_frequency': transaction_frequency,
            'avg_transaction_amount': round(avg_transaction_amount, 2),
            'account_age_days': account_age_days,
            'device_change': device_change,
            'location_change': location_change,
            'transactions_last_hour': transactions_last_hour,
            'transactions_last_day': transactions_last_day,
            'merchant_risk_score': round(merchant_risk_score, 3),
            'new_merchant': new_merchant,
            'failed_attempts': failed_attempts,
            'is_fraud': is_fraud
        })
    
    df = pd.DataFrame(data)
    
    # Balance the dataset slightly (ensure we have enough fraud cases)
    fraud_count = df['is_fraud'].sum()
    print(f"Generated {len(df)} transactions")
    print(f"Fraud cases: {fraud_count} ({fraud_count/len(df)*100:.2f}%)")
    
    return df

if __name__ == "__main__":
    # Generate training data
    df = generate_upi_data(10000)
    df.to_csv('upi_fraud_data.csv', index=False)
    print("Dataset saved to upi_fraud_data.csv")
    
    # Display sample
    print("\nSample data:")
    print(df.head(10))
    print("\nDataset statistics:")
    print(df.describe())