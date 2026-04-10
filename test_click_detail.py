
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import joblib, numpy as np

data = joblib.load('ml_modules/click_fraud/click_model.pkl')
print('type:', type(data))
if isinstance(data, dict):
    print('keys:', data.keys())
    model = data.get('model')
    print('model:', type(model))
    if hasattr(model, 'n_features_in_'):
        print('n_features:', model.n_features_in_)
    if hasattr(model, 'classes_'):
        print('classes:', model.classes_)
else:
    print('direct model type:', type(data))
    if hasattr(data, 'n_features_in_'):
        print('n_features:', data.n_features_in_)
    if hasattr(data, 'classes_'):
        print('classes:', data.classes_)
    # Try predict on simple data
    for n_feat in [1, 2, 4, 8, 10]:
        try:
            X = np.zeros((1, n_feat))
            pred = data.predict(X)
            print(f'predict with {n_feat} features: {pred}')
            if hasattr(data, 'predict_proba'):
                print(f'proba: {data.predict_proba(X)[0]}')
            break
        except Exception as e:
            print(f'{n_feat} features failed: {e}')
