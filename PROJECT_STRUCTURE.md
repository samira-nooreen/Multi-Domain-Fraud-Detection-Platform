# 🏗️ MDFDP - Project Structure

## 🎯 Overview
This document outlines the file and directory structure of the **Multi-Domain Fraud Detection Platform (MDFDP)**.

## 📁 Root Directory

```
New folder/
├── 📄 app.py                    # Main Flask application entry point
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Main project documentation
├── 📄 LICENSE                   # MIT License
├── 📄 users.json               # Local user database (JSON)
├── 📄 currency_config.py        # Currency formatting utilities
├── 📄 risk_engine.py            # Risk calculation engine
├── 📄 security_config.py        # Security configuration settings
│
├── 📂 templates/               # HTML Templates (Frontend)
│   ├── index.html              # Main dashboard
│   ├── login.html              # Login page
│   ├── signup.html             # Signup page
│   ├── verify_2fa.html         # 2FA verification
│   ├── verify_login.html       # Login verification
│   ├── profile.html            # User profile
│   ├── analytics_dashboard.html # Analytics dashboard
│   ├── security_dashboard.html  # Security settings
│   ├── chatbot_test.html       # Chatbot testing
│   ├── neon_demo.html          # UI effects demo
│   │
│   ├── [Modules]
│   ├── upi_fraud.html
│   ├── credit_card.html
│   ├── loan_default.html
│   ├── insurance_fraud.html
│   ├── click_fraud.html
│   ├── fake_news.html
│   ├── spam_email.html
│   ├── phishing_url.html
│   ├── fake_profile.html
│   └── document_forgery.html
│
├── 📂 static/                  # Static Assets
│   ├── css/
│   │   ├── style.css           # Main stylesheet
│   │   ├── neon-effects.css    # Neon UI effects
│   │   └── chatbot.css         # Chatbot widget styles
│   ├── js/
│   │   ├── script.js           # Main JavaScript logic
│   │   ├── chatbot.js          # Chatbot functionality
│   │   └── analytics.js        # Analytics charts
│   └── images/                 # Project images
│
├── 📂 ml_modules/              # Machine Learning Modules
│   ├── chatbot.py              # MDFDP Bot (AI Assistant)
│   ├── utils.py                # Shared ML utilities
│   │
│   ├── 📂 upi_fraud/           # UPI Fraud (XGBoost)
│   ├── 📂 credit_card/         # Credit Card Fraud (Isolation Forest)
│   ├── 📂 loan_default/        # Loan Default (Random Forest)
│   ├── 📂 insurance_fraud/     # Insurance Fraud (Autoencoder)
│   ├── 📂 click_fraud/         # Click Fraud (LSTM + Ensemble)
│   ├── 📂 fake_news/           # Fake News (Naive Bayes + Rules)
│   ├── 📂 spam_email/          # Spam Email (Naive Bayes)
│   ├── 📂 phishing_url/        # Phishing URL (XGBoost)
│   ├── 📂 fake_profile/        # Bot Detection (GNN + XGBoost)
│   └── 📂 document_forgery/    # Document Forgery (CNN)
│
├── 📂 tests/                   # Test Suite
│   ├── test_detection_modules.py
│   ├── test_api.py
│   └── [various test scripts]
│
├── 📂 docs/                    # Documentation
│   ├── ALGORITHM_ALIGNMENT.md
│   ├── SECURITY_IMPLEMENTATION_SUMMARY.md
│   ├── ANALYTICS_QUICK_START.md
│   └── [other docs]
│
├── 📂 scripts/                 # Utility Scripts
│   ├── train_all_models.py    # Master training script
│   └── train_all.bat           # Windows batch training
│
└── 📂 logs/                    # Application Logs
```

## 📊 Detection Modules Detail

| Directory | Module | Key Files |
|-----------|--------|-----------|
| `upi_fraud/` | UPI Fraud | `train.py`, `predict.py`, `upi_fraud_model.pkl` |
| `credit_card/` | Credit Card | `train.py`, `predict.py`, `credit_card_model.pkl` |
| `loan_default/` | Loan Default | `train.py`, `predict.py`, `loan_model.pkl` |
| `insurance_fraud/` | Insurance | `train.py`, `predict.py`, `autoencoder_model.pth` |
| `click_fraud/` | Click Fraud | `train.py`, `predict.py`, `lstm_model.pth` |
| `fake_news/` | Fake News | `train.py`, `predict.py`, `nb_model.pkl` |
| `spam_email/` | Spam Email | `train.py`, `predict.py`, `spam_model.pkl` |
| `phishing_url/` | Phishing URL | `train.py`, `predict.py`, `phishing_model.pkl` |
| `fake_profile/` | Fake Profile | `train.py`, `predict.py`, `gnn_model.pth` |
| `document_forgery/` | Document Forgery | `train.py`, `predict.py`, `cnn_model.h5` |

---

**Last Updated**: 2025-11-30
**Version**: 1.0.0
