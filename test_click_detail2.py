
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import joblib, numpy as np

model = joblib.load('ml_modules/click_fraud/click_model.pkl')

# Test with zeros (neutral input)
X_zeros = np.zeros((1, 10))
print('zeros proba:', model.predict_proba(X_zeros)[0])

# Normal human: avg 2s between clicks, 10 clicks
X_normal = np.array([[10, 2.0, 1.0, 0.5, 20, 20, 0, 0.5, 0, 0]])
print('normal human proba:', model.predict_proba(X_normal)[0])

# Bot: avg 0.05s between clicks, 50 clicks
X_bot = np.array([[50, 0.05, 0.01, 0.01, 5, 5, 0, 100.0, 0, 0]])
print('bot proba:', model.predict_proba(X_bot)[0])

# Check model coefficients to understand feature importance
if hasattr(model, 'coef_'):
    print('coef:', model.coef_[0])
if hasattr(model, 'feature_names_in_'):
    print('features:', model.feature_names_in_)

# Check what data the model was trained on
X_data = np.load('ml_modules/click_fraud/click_X_sequential.npy', allow_pickle=True)
y_data = np.load('ml_modules/click_fraud/click_y.npy', allow_pickle=True)
print('X shape:', X_data.shape)
print('y shape:', y_data.shape)
print('y unique:', np.unique(y_data))
