
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import joblib, numpy as np, pandas as pd

model = joblib.load('ml_modules/click_fraud/click_model.pkl')
print('n_features:', model.n_features_in_)
# Try with correct feature names from generate_data.py
# The 16-feature set is:
# avg_time_diff, std_time_diff, min_time_diff, max_time_diff,
# avg_click_x, std_click_x, avg_click_y, std_click_y,
# total_ip_changes, total_ua_changes, avg_hour, weekend_ratio,
# avg_click_velocity, std_click_velocity, avg_referrer_entropy, total_clicks

# Model wants 10, so maybe it uses the first 10 or specific subset
# Let's check by varying and testing
# Normal human: slow, varied clicks, moderate velocity
X_normal_16 = np.array([[
    2.5,    # avg_time_diff
    1.0,    # std_time_diff
    0.5,    # min_time_diff
    6.0,    # max_time_diff
    500.0,  # avg_click_x
    200.0,  # std_click_x
    400.0,  # avg_click_y
    150.0,  # std_click_y
    0.0,    # total_ip_changes
    0.0,    # total_ua_changes
]])  # 10 features
print('normal 10f:', model.predict_proba(X_normal_16)[0])

X_bot_10 = np.array([[
    0.1,    # avg_time_diff (fast!)
    0.02,   # std_time_diff (very consistent)
    0.02,   # min_time_diff
    0.2,    # max_time_diff
    500.0,  # avg_click_x (concentrated)
    5.0,    # std_click_x (very small std!)
    300.0,  # avg_click_y
    5.0,    # std_click_y
    0.0,    # total_ip_changes
    0.0,    # total_ua_changes
]])
print('bot 10f:', model.predict_proba(X_bot_10)[0])
