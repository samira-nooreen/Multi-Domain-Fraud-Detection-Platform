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
    """Generate synthetic UPI transaction data with realistic fraud patterns"""
    
    data = []
    
    # Create more realistic fraud patterns
    fraud_patterns = [
        # High amount + unusual time
        {'amount_range': (500000, 2000000), 'hour_range': (0, 5), 'device_change': 0.3},
        # High amount + device change
        {'amount_range': (500000, 1500000), 'hour_range': (6, 23), 'device_change': 0.8},
        # Medium amount + unusual time + device change
        {'amount_range': (100000, 500000), 'hour_range': (0, 5), 'device_change': 0.7},
        # High frequency + failed attempts
        {'amount_range': (10000, 100000), 'hour_range': (0, 23), 'device_change': 0.2, 'high_frequency': True},
        # New account + high amount
        {'amount_range': (100000, 1000000), 'hour_range': (0, 23), 'device_change': 0.4, 'new_account': True}
    ]
    
    # Generate fraud samples
    n_fraud = int(n_samples * 0.15)  # 15% fraud (more realistic)
    fraud_per_pattern = n_fraud // len(fraud_patterns)
    
    for pattern in fraud_patterns:
        for _ in range(fraud_per_pattern):
            # Generate fraud transaction based on pattern
            amount = np.random.uniform(pattern['amount_range'][0], pattern['amount_range'][1])
            hour = np.random.randint(pattern['hour_range'][0], pattern['hour_range'][1] + 1)
            
            # User behavior features
            transaction_frequency = np.random.poisson(8) if pattern.get('high_frequency') else np.random.poisson(3)
            avg_transaction_amount = np.random.lognormal(4.0, 1.2)  # Lower avg for suspicious accounts
            account_age_days = np.random.randint(1, 90) if pattern.get('new_account') else np.random.randint(1, 3650)
            
            # Device features
            device_change = np.random.choice([0, 1], p=[1-pattern['device_change'], pattern['device_change']])
            
            # Other features
            location_change = np.random.choice([0, 1], p=[0.70, 0.30]) if pattern.get('high_frequency') else np.random.choice([0, 1], p=[0.85, 0.15])
            transactions_last_hour = np.random.poisson(3) if pattern.get('high_frequency') else np.random.poisson(0.8)
            transactions_last_day = np.random.poisson(8) if pattern.get('high_frequency') else np.random.poisson(2)
            merchant_risk_score = np.random.uniform(0.6, 1.0) if amount > 500000 else np.random.uniform(0, 0.7)
            new_merchant = np.random.choice([0, 1], p=[0.60, 0.40])
            failed_attempts = np.random.poisson(2) if pattern.get('high_frequency') else np.random.poisson(0.3)
            
            data.append({
                'transaction_id': f'UPI_FRAUD_{len(data):06d}',
                'amount': round(amount, 2),
                'hour': hour,
                'day_of_week': np.random.randint(0, 7),
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
                'is_fraud': 1
            })
    
    # Generate legitimate samples
    n_legit = n_samples - len(data)
    for i in range(n_legit):
        # Normal transaction patterns
        amount = np.random.lognormal(5, 1.8)  # More normal distribution
        hour = np.random.randint(6, 23)  # Business hours mostly
        day_of_week = np.random.randint(0, 7)
        
        # Normal user behavior
        transaction_frequency = np.random.poisson(3)
        avg_transaction_amount = np.random.lognormal(4.8, 1.0)
        account_age_days = np.random.randint(180, 3650)  # Established accounts
        
        # Low risk features
        device_change = np.random.choice([0, 1], p=[0.97, 0.03])
        location_change = np.random.choice([0, 1], p=[0.95, 0.05])
        transactions_last_hour = np.random.poisson(0.5)
        transactions_last_day = np.random.poisson(2)
        merchant_risk_score = np.random.uniform(0, 0.4)
        new_merchant = np.random.choice([0, 1], p=[0.85, 0.15])
        failed_attempts = np.random.poisson(0.1)
        
        data.append({
            'transaction_id': f'UPI_LEGIT_{len(data):06d}',
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
            'is_fraud': 0
        })
    
    df = pd.DataFrame(data)
    
    # Shuffle the data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Show distribution
    fraud_count = df['is_fraud'].sum()
    print(f"Generated {len(df)} transactions")
    print(f"Fraud cases: {fraud_count} ({fraud_count/len(df)*100:.2f}%)")
    print(f"Legitimate cases: {len(df)-fraud_count} ({(len(df)-fraud_count)/len(df)*100:.2f}%)")
    
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