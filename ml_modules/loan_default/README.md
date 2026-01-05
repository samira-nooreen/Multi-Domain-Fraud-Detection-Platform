# Loan Default Risk Prediction Module

This module predicts the risk of loan default using advanced machine learning algorithms.

## Features
- **Multi-Model Training**: Logistic Regression, Gradient Boosting (XGBoost), Neural Networks.
- **Rich Feature Engineering**: DTI Ratio, Delinquency History, Credit Utilization, Income Stability.
- **Real-Time Inference**: <100ms latency with detailed risk scoring and decision explanation.

## Files
- `generate_data.py`: Generates synthetic loan application data with realistic risk patterns.
- `train.py`: Trains multiple models, evaluates them, and saves the best performer.
- `predict.py`: Handles real-time inference, risk scoring, and decision logic.
- `loan_model.pkl`: The trained model artifact.
- `loan_features.pkl`: List of features used by the model.

## Usage
1. **Train Model**:
   ```bash
   python ml_modules/loan_default/train.py
   ```
2. **Run Inference** (via App):
   The module is integrated into the main Flask app (`app.py`) at `/detect_loan`.

## Risk Scoring
- **0-100**: Low Risk (Auto-Approve)
- **100-300**: Medium Risk (Manual Review)
- **300-500**: High Risk (Conditional)
- **>500**: Very High Risk (Reject)
