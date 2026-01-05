# 🖱️ Click Fraud Detection Module

## Overview
Advanced click fraud detection system using multiple machine learning algorithms with ensemble voting to detect bot and fraudulent click patterns.

## 🧠 Implemented Algorithms

### 1. **CatBoost (Gradient Boosting)** - Best for Categorical ⭐
- **Type**: Gradient Boosting optimized for categorical features
- **Accuracy**: ~90-93% (expected)
- **Weight in Ensemble**: 35%
- **Strengths**: 
  - Excellent for categorical data (IPs, user agents)
  - Fast training and inference
  - Handles missing values well
  - Built-in categorical feature support
- **Use Case**: Primary model for production

### 2. **Wide & Deep Network**
- **Type**: Deep Learning (combines linear and neural network)
- **Accuracy**: ~88-91% (expected)
- **Weight in Ensemble**: 25%
- **Strengths**:
  - Memorization (wide) + generalization (deep)
  - Good for both sparse and dense features
  - Captures complex patterns
- **Use Case**: Deep learning baseline

### 3. **Autoencoder (Anomaly Detection)**
- **Type**: Unsupervised neural network
- **Accuracy**: ~85-88% (expected)
- **Weight in Ensemble**: 20%
- **Strengths**:
  - Detects unusual bot patterns
  - Unsupervised learning
  - Good for new fraud types
- **Use Case**: Anomaly detection for bots

### 4. **Logistic Regression**
- **Type**: Classical ML
- **Accuracy**: ~82-85% (expected)
- **Weight in Ensemble**: 20%
- **Strengths**:
  - Fast, interpretable
  - Robust baseline
  - Low computational cost
- **Use Case**: Fast baseline predictions

## 📊 Ensemble Strategy

The system uses **weighted voting** where:
- Each model contributes a probability score
- Scores are weighted by model reliability
- Final prediction is weighted average
- Risk level based on probability threshold

```
Final Score = (0.35 × CatBoost) + (0.25 × Wide&Deep) + 
              (0.20 × Autoencoder) + (0.20 × LogReg)
```

## 🚀 Usage

### Training
```bash
# Install dependencies
pip install catboost torch scikit-learn pandas numpy

# Generate dataset
python generate_data.py

# Train all models
python train.py
```

### Prediction
```python
from predict import ClickFraudDetector

detector = ClickFraudDetector()

# Click sequence: [time_diff, x, y, ip_change, ua_change, hour, is_weekend, velocity]
clicks = [
    [0.1, 500, 300, 0, 0, 14, 0, 50],  # Fast, bot-like
    [0.12, 502, 301, 0, 0, 14, 0, 52],
]

# Ensemble prediction (recommended)
result = detector.predict(clicks, use_ensemble=True)

print(result)
# {
#   'is_fraud': True,
#   'fraud_probability': 0.87,
#   'risk_level': 'HIGH',
#   'confidence': 'HIGH',
#   'models_used': ['CatBoost', 'Wide&Deep', 'Autoencoder', 'LogReg'],
#   'individual_predictions': {...}
# }
```

## 📁 File Structure

```
click_fraud/
├── generate_data.py      # Dataset generation
├── train.py              # Multi-model training
├── predict.py            # Ensemble prediction
├── requirements.txt      # Dependencies
├── README.md             # This file
├── click_data.csv        # Training data (tabular)
├── click_X_sequential.npy # Sequential data
├── click_y.npy           # Labels
└── models/               # Trained models
    ├── catboost_model.pkl    # CatBoost
    ├── widedeep_model.pth    # Wide & Deep
    ├── autoencoder_model.pth # Autoencoder
    └── logreg_model.pkl      # Logistic Regression
```

## 🎯 Performance Metrics

Expected performance on validation set:

| Model | Accuracy | AUC-ROC | Speed | Use Case |
|-------|----------|---------|-------|----------|
| Logistic Regression | 82-85% | 0.85 | ⚡⚡⚡ | Fast baseline |
| Autoencoder | 85-88% | 0.87 | ⚡⚡ | Anomaly detection |
| Wide & Deep | 88-91% | 0.90 | ⚡⚡ | Deep learning |
| CatBoost | 90-93% | 0.92 | ⚡⚡⚡ | Best single model |
| **Ensemble** | **91-94%** | **0.93** | ⚡⚡ | **Production (Best)** |

## 🔍 Click Fraud Indicators

The models detect:

1. **Bot Behavior Patterns**
   - Very fast clicks (< 0.5s between clicks)
   - Consistent timing (low variance)
   - Concentrated click areas
   - No IP/user agent changes

2. **Unusual Patterns**
   - High click velocity (> 30 clicks/min)
   - Clicks at unusual hours
   - No weekend/weekday pattern
   - Repetitive coordinates

3. **Anomalies**
   - Deviation from normal user behavior
   - Unusual feature combinations
   - Reconstruction errors (Autoencoder)

## 💡 Why These Algorithms?

### CatBoost - Best for Categorical Data ⭐
- **Reason**: Click fraud has many categorical features (IP, user agent, etc.)
- **Advantage**: Native categorical support, fast, accurate
- **Performance**: 90-93% accuracy expected

### Wide & Deep - Memorization + Generalization
- **Reason**: Combines linear (wide) and neural (deep) components
- **Advantage**: Learns both simple rules and complex patterns
- **Performance**: 88-91% accuracy expected

### Autoencoder - Anomaly Detection
- **Reason**: Detects unusual bot behavior patterns
- **Advantage**: Unsupervised, finds new fraud types
- **Performance**: 85-88% accuracy expected

### Logistic Regression - Fast Baseline
- **Reason**: Quick, interpretable predictions
- **Advantage**: Low latency, explainable
- **Performance**: 82-85% accuracy expected

## 🛠️ Customization

### Adjust Ensemble Weights

Edit `predict.py`:
```python
predictions.append((lr_pred['fraud_probability'], 0.20, 'Logistic Regression'))
predictions.append((cb_pred['fraud_probability'], 0.35, 'CatBoost'))
predictions.append((ae_pred['fraud_probability'], 0.20, 'Autoencoder'))
predictions.append((wd_pred['fraud_probability'], 0.25, 'Wide & Deep'))
```

### Add More Features

Edit `generate_data.py` to add features like:
- Device type
- Browser fingerprint
- Geographic location
- Referrer URL

## 📈 Feature Importance

Key features for click fraud detection:

1. **avg_time_diff** - Average time between clicks
2. **std_time_diff** - Consistency of clicks
3. **avg_click_velocity** - Clicks per minute
4. **total_ip_changes** - IP address changes
5. **std_click_x/y** - Click position variance

## 🔗 Integration with Flask App

The module integrates with the main Flask application:
```python
# In app.py
from ml_modules.click_fraud.predict import ClickFraudDetector

detector = ClickFraudDetector()
result = detector.predict(click_sequence)
```

## 📚 References

- **CatBoost**: [Official Documentation](https://catboost.ai/)
- **Wide & Deep**: [Google Research Paper](https://arxiv.org/abs/1606.07792)
- **Autoencoders**: [Deep Learning Book](https://www.deeplearningbook.org/)

## 📄 License

Part of the ML Fraud Detection System
