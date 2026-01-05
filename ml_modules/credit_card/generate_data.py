"""
Credit Card Fraud Detection - Dataset Generator
Generates realistic synthetic credit card transaction data with minimal inputs
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

def generate_credit_card_data(n_samples=15000):
    """Generate synthetic credit card transaction data with minimal inputs"""
    
    data = []
    
    for i in range(n_samples):
        # Minimal inputs from user
        amount = np.random.lognormal(4, 2)
        
        # Generate derived features from minimal inputs
        # Time features (would normally come from system time)
        hour = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Card features (would normally come from user profile)
        card_age_days = np.random.randint(30, 3650)
        credit_limit = np.random.choice([50000, 100000, 200000, 500000])
        available_credit = credit_limit - np.random.uniform(0, credit_limit * 0.8)
        
        # Transaction patterns (derived)
        transactions_last_24h = np.random.poisson(2)
        transactions_last_week = np.random.poisson(10)
        avg_transaction_amount = np.random.lognormal(3.5, 1.5)
        
        # Location and merchant (would come from user input or geolocation)
        distance_from_home = np.random.exponential(10)
        distance_from_last_transaction = np.random.exponential(5)
        merchant_category = np.random.choice(['retail', 'online', 'gas', 'restaurant', 'travel', 'other'])
        
        # Transaction type features (from user input)
        is_online = np.random.choice([0, 1], p=[0.6, 0.4])
        is_international = np.random.choice([0, 1], p=[0.9, 0.1])
        
        # Security features (from user input)
        pin_entered = np.random.choice([0, 1], p=[0.3, 0.7])
        chip_used = np.random.choice([0, 1], p=[0.2, 0.8])
        
        # Velocity features
        amount_last_24h = transactions_last_24h * avg_transaction_amount
        
        # Calculate fraud score
        fraud_score = 0
        
        # High amount
        if amount > credit_limit * 0.5:
            fraud_score += 0.3
        
        # Unusual time
        if hour >= 23 or hour <= 4:
            fraud_score += 0.15
        
        # High velocity
        if transactions_last_24h > 5:
            fraud_score += 0.25
        
        # Large distance
        if distance_from_last_transaction > 100:
            fraud_score += 0.2
        
        # International transaction
        if is_international:
            fraud_score += 0.2
        
        # No PIN/chip
        if not pin_entered and not chip_used:
            fraud_score += 0.25
        
        # Online transaction with high amount
        if is_online and amount > 20000:
            fraud_score += 0.2
        
        # Low available credit
        if available_credit < credit_limit * 0.1:
            fraud_score += 0.15
        
        # Determine fraud
        is_fraud = 1 if fraud_score > 0.55 + np.random.normal(0, 0.1) else 0
        
        data.append({
            'transaction_id': f'CC{i:06d}',
            'amount': round(amount, 2),
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'card_age_days': card_age_days,
            'credit_limit': credit_limit,
            'available_credit': round(available_credit, 2),
            'transactions_last_24h': transactions_last_24h,
            'transactions_last_week': transactions_last_week,
            'avg_transaction_amount': round(avg_transaction_amount, 2),
            'distance_from_home': round(distance_from_home, 2),
            'distance_from_last_transaction': round(distance_from_last_transaction, 2),
            'merchant_category': merchant_category,
            'is_online': is_online,
            'is_international': is_international,
            'pin_entered': pin_entered,
            'chip_used': chip_used,
            'is_fraud': is_fraud
        })
    
    df = pd.DataFrame(data)
    
    # One-hot encode merchant category
    df = pd.get_dummies(df, columns=['merchant_category'], prefix='merchant')
    
    fraud_count = df['is_fraud'].sum()
    print(f"Generated {len(df)} transactions")
    print(f"Fraud cases: {fraud_count} ({fraud_count/len(df)*100:.2f}%)")
    
    return df

if __name__ == "__main__":
    df = generate_credit_card_data(15000)
    df.to_csv('credit_card_data.csv', index=False)
    print("Dataset saved to credit_card_data.csv")
    print("\nSample data:")
    print(df.head())