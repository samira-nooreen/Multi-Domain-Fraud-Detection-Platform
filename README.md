# 🛡️ Multi-Domain Fraud Detection Platform (MDFDP)

MDFDP is a Flask-based web platform that brings multiple fraud and risk detection modules into one unified system. It combines machine learning models, rule-based logic, and a web dashboard to help analyze suspicious activity across financial transactions, social profiles, content, and more.

## 🌐 Live Website
[https://multi-domain-fraud-detection-platform-e2f0e9g2hha4axcm.southeastasia-01.azurewebsites.net/](https://multi-domain-fraud-detection-platform-e2f0e9g2hha4axcm.southeastasia-01.azurewebsites.net/)

## 🔍 Core Modules

The platform includes **11 major analysis modules**:

1. 💸 UPI Fraud Detection
2. 💳 Credit Card Fraud Detection
3. 🏦 Loan Default Risk Prediction
4. 🏥 Insurance Fraud Detection
5. 🖱️ Click Fraud Detection
6. 📰 Fake News Detection
7. 📧 Spam Email Detection
8. 🔗 Phishing URL Detection
9. 🤖 Fake Profile / Bot Detection
10. 📄 Document Forgery Detection
11. ™️ Brand Abuse Detection

## 🧰 Tech Stack

| Layer | Tools |
|-------|-------|
| 🔙 Backend | Flask, Flask-SocketIO, Flask-CORS |
| 🤖 ML/Data | scikit-learn, XGBoost, NumPy, pandas |
| 📦 Model Serving | Pickle/joblib-based model loading with module-level predictors |
| 🗄️ Database | SQLite |
| 🎨 Frontend | Jinja templates, HTML/CSS/JS |
| ☁️ Deployment | Azure App Service + GitHub Actions |

## 📁 Project Structure

```
├── app.py                          # 🚀 Main Flask application and routes
├── database.py                     # 🗃️ SQLite setup and data-access helpers
├── ml_modules/                     # 🧠 Detection modules and model logic
├── templates/                      # 🖼️ Frontend pages
├── static/                         # 🎨 CSS/JS/assets
└── .github/workflows/
    └── azure-webapp.yml            # ⚙️ Azure deployment workflow
```

## Local Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables (locally via terminal or `.env`).
5. Run the app:

```bash
python app.py
```

6. Open:

```text
http://127.0.0.1:5000
```

## Required Environment Variables

Set these for production:

- `SECRET_KEY`
- `EMAIL_SENDER`
- `EMAIL_PASSWORD`
- `EMAIL_RECIPIENT`
- `FLASK_DEBUG` (use `false` in production)
- `SOCKETIO_ASYNC_MODE` (recommended: `threading`)
- `SCM_DO_BUILD_DURING_DEPLOYMENT` (recommended: `true` on Azure)

## Azure Deployment Notes

The repository is prepared for Azure App Service deployment using GitHub Actions.

- Workflow file: `.github/workflows/azure-webapp.yml`
- Required GitHub repository secrets:
  - `AZURE_WEBAPP_NAME`
  - `AZURE_WEBAPP_PUBLISH_PROFILE`

## Disclaimer

This project is intended for educational, research, and demonstration purposes. For high-stakes production use, add stronger monitoring, security hardening, model governance, and audit controls.
