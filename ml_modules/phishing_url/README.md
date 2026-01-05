# Phishing URL Detection Module

This module implements a Phishing URL detection system using Machine Learning.

## Algorithms
The system is designed to support a multi-modal approach:
1.  **XGBoost (Implemented)**: Uses URL-based features (Length, Special Characters, Whois Age, Token Entropy).
2.  **CNN (Theory)**: Can be used on website screenshots to detect visual similarity to known brands.
3.  **BERT (Theory)**: Can be used on scraped HTML text to detect semantic anomalies or phishing language.

## Implementation Details (XGBoost)
The current implementation focuses on the URL feature-based approach using XGBoost.

### Features
-   **Length**: Length of the URL.
-   **Special Characters**: Count of non-alphanumeric characters.
-   **Whois Age**: Age of the domain (Simulated for this module).
-   **Token Entropy**: Shannon entropy of the URL characters.

### Files
-   `train.py`: Generates synthetic data, extracts features, trains an XGBoost model, and saves it.
-   `predict.py`: Loads the model and performs real-time prediction on new URLs.
-   `phishing_data.csv`: Dataset used for training.
-   `phishing_model.pkl`: Saved XGBoost model.

## Usage
1.  **Train the model**:
    ```bash
    python ml_modules/phishing_url/train.py
    ```
2.  **Run the web app**:
    The module is integrated into the main Flask application. Go to the "Phishing URL Detection" section to test it.
