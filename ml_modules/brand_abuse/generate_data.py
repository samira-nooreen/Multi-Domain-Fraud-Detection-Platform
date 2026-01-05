"""
Brand Abuse Detection - Data Generation
"""
import pandas as pd
import numpy as np
from train import generate_brand_abuse_data

def generate_data():
    """Generate brand abuse data"""
    print("Generating brand abuse detection dataset...")
    df = generate_brand_abuse_data()
    return df

if __name__ == "__main__":
    df = generate_data()
    print(f"Generated {len(df)} samples")
    print(df.head())