MDFDP - Input Details Required Across All 11 Modules

1) UPI Fraud Detection
- Transaction Amount (INR)
- Sender ID
- Receiver ID
- Time of Transaction
- Device Changed? (Yes/No)

2) Credit Card Fraud Detection
- Transaction Amount
- Location
- Transaction Type
- Card Present? (Yes/No)
- Time of Transaction (optional)

3) Loan Default Detection
- Loan Amount
- Monthly Income
- Credit Score
- Loan Duration (months)

4) Insurance Fraud Detection
- Claim Amount
- Type of Claim
- Incident Description
- Previous Claim Count

5) Click Fraud Detection
- Number of Clicks
- Time Spent (seconds)
- Click Pattern
- IP Address Changes

6) Fake News Detection
- News Article Text
- News Source URL (optional)

7) Spam Email Detection
- Sender Email Address
- Email Content

8) Phishing URL Detection
- URL to Analyze

9) Fake Profile Detection
- Username
- Account Creation Date
- Follower Count
- Posts Count

10) Document Forgery Detection
- Document Image Upload

11) Brand Abuse Detection
- Seller Profile Link (URL)
- Brand Keywords (comma-separated)
- Seller/Page Name
- Listing Title (optional)
- Description/Post Text (optional)
- Image Upload(s) (optional)

----------------------------------------
Module to ML Algorithm Mapping (Current Code)
----------------------------------------

1) UPI Fraud Detection
- Isolation Forest or classifier model with predict_proba (e.g., XGBoost/RandomForest) + rule-based calibration

2) Credit Card Fraud Detection
- Ensemble: Isolation Forest + Random Forest (when saved model is dict), otherwise sklearn classifier + rule-based calibration

3) Loan Default Detection
- Hybrid scoring: Logistic Regression style formula + Gradient Boosting model probability (if model available)

4) Insurance Fraud Detection
- XGBoost model + rule-based risk engine (with heuristic fallback)

5) Click Fraud Detection
- LSTM (PyTorch) primary + heuristic/rule-based fallback and calibration

6) Fake News Detection
- Naive Bayes + TF-IDF + rule-based misinformation checks + source credibility/trusted-domain calibration

7) Spam Email Detection
- Naive Bayes + TF-IDF + rule-based enhancement (phishing phrase checks, shortened-link analysis, and sender-domain spoof validation)

8) Phishing URL Detection
- Heuristic rule-based detector (SVM path intentionally bypassed as unreliable) with domain normalization, brand-domain validation, typo-spoof checks, and shortened-URL risk analysis

9) Fake Profile Detection
- sklearn model (Random Forest style classifier) + rule-based correction (GNN optional only if available)

10) Document Forgery Detection
- sklearn classifier on image-extracted features (with heuristic fallback)

11) Brand Abuse Detection
- sklearn classifier on engineered URL/text/social features (with heuristic fallback)
