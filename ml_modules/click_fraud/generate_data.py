"""
Click Fraud Detection - Enhanced Dataset Generator
Generates realistic clickstream data with bot and human patterns
"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

def generate_click_data(n_sequences=2000, seq_length=20):
    """
    Generate sequences of click data with realistic patterns.
    Each sequence represents a user session with multiple clicks.
    
    Features per click:
    - time_diff: Time since last click (seconds)
    - click_x, click_y: Click coordinates
    - ip_change: Whether IP changed
    - user_agent_change: Whether user agent changed
    - hour_of_day: Hour when click occurred (0-23)
    - is_weekend: Weekend indicator
    - click_velocity: Clicks per minute
    """
    data = []
    labels = []
    
    for session_id in range(n_sequences):
        # 70% normal users, 30% bots/fraud
        is_fraud = np.random.choice([0, 1], p=[0.7, 0.3])
        
        sequence = []
        cumulative_time = 0
        
        for t in range(seq_length):
            if is_fraud:
                # BOT BEHAVIOR PATTERNS:
                # 1. Very fast, consistent clicks
                time_diff = np.random.exponential(0.15)  # Very fast (0.15s avg)
                
                # 2. Clicks concentrated in small area (automated)
                click_x = np.random.normal(500, 10)  # Concentrated
                click_y = np.random.normal(300, 10)
                
                # 3. Rarely changes IP (same bot)
                ip_change = np.random.choice([0, 1], p=[0.98, 0.02])
                
                # 4. Never changes user agent (automated)
                user_agent_change = 0
                
                # 5. Uniform distribution across hours (bots don't sleep)
                hour_of_day = np.random.randint(0, 24)
                
                # 6. No weekend pattern
                is_weekend = np.random.choice([0, 1], p=[0.5, 0.5])
                
                # 7. Very high click velocity
                click_velocity = np.random.uniform(30, 60)  # 30-60 clicks/min
                
                # 8. Low referrer entropy (always same source or empty)
                referrer_entropy = np.random.uniform(0, 0.5)
                
            else:
                # HUMAN BEHAVIOR PATTERNS:
                # 1. Slower, more varied clicks
                time_diff = np.random.exponential(2.5)  # Slower (2.5s avg)
                
                # 2. Clicks spread across screen (natural browsing)
                click_x = np.random.uniform(0, 1000)
                click_y = np.random.uniform(0, 800)
                
                # 3. Occasional IP changes (mobile networks, VPN)
                ip_change = np.random.choice([0, 1], p=[0.95, 0.05])
                
                # 4. Rare user agent changes
                user_agent_change = np.random.choice([0, 1], p=[0.98, 0.02])
                
                # 5. Peak hours: 9-11am, 2-5pm, 8-10pm
                peak_hours = [9, 10, 11, 14, 15, 16, 17, 20, 21, 22]
                if np.random.rand() < 0.6:
                    hour_of_day = np.random.choice(peak_hours)
                else:
                    hour_of_day = np.random.randint(0, 24)
                
                # 6. More activity on weekdays
                is_weekend = np.random.choice([0, 1], p=[0.7, 0.3])
                
                # 7. Normal click velocity
                click_velocity = np.random.uniform(2, 15)  # 2-15 clicks/min
                
                # 8. High referrer entropy (varied sources)
                referrer_entropy = np.random.uniform(1.5, 3.0)
            
            cumulative_time += time_diff
            
            # Create feature vector for this click
            click_features = [
                time_diff,
                click_x,
                click_y,
                ip_change,
                user_agent_change,
                hour_of_day,
                is_weekend,
                click_velocity,
                referrer_entropy
            ]
            
            sequence.append(click_features)
        
        data.append(sequence)
        labels.append(is_fraud)
    
    return np.array(data), np.array(labels)

def generate_tabular_data(n_samples=2000):
    """
    Generate aggregated tabular data (for non-sequential models)
    Each row represents a user session with aggregated statistics
    """
    X, y = generate_click_data(n_sequences=n_samples, seq_length=20)
    
    # Aggregate sequence features
    features = []
    for sequence in X:
        seq_array = np.array(sequence)
        
        # Statistical features from sequence
        agg_features = [
            np.mean(seq_array[:, 0]),  # avg_time_diff
            np.std(seq_array[:, 0]),   # std_time_diff
            np.min(seq_array[:, 0]),   # min_time_diff
            np.max(seq_array[:, 0]),   # max_time_diff
            np.mean(seq_array[:, 1]),  # avg_click_x
            np.std(seq_array[:, 1]),   # std_click_x
            np.mean(seq_array[:, 2]),  # avg_click_y
            np.std(seq_array[:, 2]),   # std_click_y
            np.sum(seq_array[:, 3]),   # total_ip_changes
            np.sum(seq_array[:, 4]),   # total_ua_changes
            np.mean(seq_array[:, 5]),  # avg_hour
            np.mean(seq_array[:, 6]),  # weekend_ratio
            np.mean(seq_array[:, 7]),  # avg_click_velocity
            np.std(seq_array[:, 7]),   # std_click_velocity
            np.mean(seq_array[:, 8]),  # avg_referrer_entropy
            len(sequence),             # total_clicks
        ]
        
        features.append(agg_features)
    
    return np.array(features), y

if __name__ == "__main__":
    # Generate sequential data
    print("Generating sequential click data...")
    X_seq, y = generate_click_data(2000, seq_length=20)
    np.save('click_X_sequential.npy', X_seq)
    np.save('click_y.npy', y)
    print(f"✓ Generated {len(X_seq)} sequences")
    print(f"  - Normal: {np.sum(y==0)} ({np.sum(y==0)/len(y)*100:.1f}%)")
    print(f"  - Fraud: {np.sum(y==1)} ({np.sum(y==1)/len(y)*100:.1f}%)")
    print("✓ Saved to click_X_sequential.npy and click_y.npy")
    
    # Generate tabular data
    print("\nGenerating tabular click data...")
    X_tab, y_tab = generate_tabular_data(2000)
    df = pd.DataFrame(X_tab, columns=[
        'avg_time_diff', 'std_time_diff', 'min_time_diff', 'max_time_diff',
        'avg_click_x', 'std_click_x', 'avg_click_y', 'std_click_y',
        'total_ip_changes', 'total_ua_changes', 'avg_hour', 'weekend_ratio',
        'avg_click_velocity', 'std_click_velocity', 'avg_referrer_entropy', 'total_clicks'
    ])
    df['is_fraud'] = y_tab
    df.to_csv('click_data.csv', index=False)
    print(f"✓ Generated {len(df)} tabular samples")
    print("✓ Saved to click_data.csv")
