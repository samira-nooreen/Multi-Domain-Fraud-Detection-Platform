# 💰 Loan Default Risk Prediction - Complete Theoretical Design

## Overview

Loan default risk prediction is a critical application of machine learning in financial services. Unlike fraud detection, this focuses on predicting the probability that a borrower will fail to repay a loan based on their financial profile and credit history. This system combines traditional statistical methods (Logistic Regression), gradient boosting (XGBoost/CatBoost), and neural networks to provide accurate risk assessments.

---

## A. Algorithms - Theoretical Foundation

### 1. Logistic Regression (Baseline) 📊

**Theory:**
Logistic Regression is a statistical model that predicts the probability of a binary outcome (default/no default) using a logistic function (sigmoid).

**Mathematical Foundation:**
```
P(default) = 1 / (1 + e^-(β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ))

Where:
- P(default) = Probability of loan default
- β₀ = Intercept
- β₁, β₂, ..., βₙ = Coefficients for features
- x₁, x₂, ..., xₙ = Feature values
```

**How It Works:**
1. Linear combination of features: z = β₀ + Σ(βᵢ × xᵢ)
2. Apply sigmoid function: P = 1 / (1 + e^(-z))
3. Output probability between 0 and 1
4. Classify: default if P > threshold (typically 0.5)

**Why Baseline:**
- **Interpretable:** Coefficients show feature importance
- **Fast:** Quick training and inference
- **Probabilistic:** Provides calibrated probabilities
- **Regulatory Compliance:** Explainable for credit decisions
- **Industry Standard:** Widely used in traditional credit scoring

**Feature Coefficients Interpretation:**
- Positive coefficient: Increases default risk
- Negative coefficient: Decreases default risk
- Magnitude: Strength of relationship

**Example:**
```
log(odds) = -2.5 + 0.8×debt_to_income - 0.3×credit_score + 0.5×delinquencies

Interpretation:
- debt_to_income: +0.8 → Higher DTI increases default risk
- credit_score: -0.3 → Higher score decreases default risk
- delinquencies: +0.5 → More delinquencies increase risk
```

**Regularization:**
- **L1 (Lasso):** Feature selection, sparse models
- **L2 (Ridge):** Prevents overfitting, shrinks coefficients
- **Elastic Net:** Combination of L1 and L2

**Expected Performance:**
- **Accuracy:** 70-75%
- **AUC-ROC:** 0.70-0.75
- **Precision:** 60-70%
- **Recall:** 65-75%
- **Training Time:** Very fast (seconds)

**Use Cases:**
- Baseline model for comparison
- Regulatory reporting (explainable)
- Quick risk assessment
- Feature importance analysis

---

### 2. XGBoost / CatBoost (Primary Model) ⭐

**Theory:**
Gradient boosting builds an ensemble of decision trees sequentially, where each tree corrects errors of previous trees.

**XGBoost (Extreme Gradient Boosting):**

**How It Works:**
1. Start with initial prediction (mean default rate)
2. Calculate residuals (errors)
3. Build decision tree to predict residuals
4. Add tree to ensemble with learning rate
5. Update predictions
6. Repeat for N iterations

**Key Features:**
- **Regularization:** L1 and L2 to prevent overfitting
- **Tree Pruning:** Max depth, min child weight
- **Column/Row Sampling:** Reduces overfitting
- **Parallel Processing:** Fast training
- **Handles Missing Values:** Built-in missing value handling

**Hyperparameters:**
```
n_estimators: 100-500 (number of trees)
max_depth: 3-8 (tree depth)
learning_rate: 0.01-0.1 (shrinkage)
subsample: 0.8 (row sampling)
colsample_bytree: 0.8 (column sampling)
gamma: 0-5 (min split loss)
reg_alpha: 0-1 (L1 regularization)
reg_lambda: 1-10 (L2 regularization)
scale_pos_weight: (neg_samples / pos_samples)
```

**CatBoost (Categorical Boosting):**

**Advantages over XGBoost:**
- **Native Categorical Support:** No need for one-hot encoding
- **Ordered Boosting:** Reduces overfitting
- **Symmetric Trees:** Faster inference
- **Robust to Overfitting:** Better default parameters

**Key Features:**
- **Ordered Target Encoding:** Prevents target leakage
- **Oblivious Trees:** Balanced, fast prediction
- **GPU Acceleration:** Faster training
- **Automatic Categorical Handling:** Processes categories directly

**Hyperparameters:**
```
iterations: 100-1000
depth: 4-10
learning_rate: 0.01-0.1
l2_leaf_reg: 1-10 (L2 regularization)
border_count: 32-255 (feature quantization)
auto_class_weights: Balanced (for imbalanced data)
```

**Why for Loan Default:**
- **High Accuracy:** 80-88% typical
- **Handles Non-Linear Relationships:** Captures complex patterns
- **Feature Interactions:** Automatically learns interactions
- **Missing Data:** Handles missing values natively
- **Imbalanced Data:** Class weighting support
- **Feature Importance:** Identifies key risk factors

**Feature Importance:**
- Gain: Total improvement from feature
- Split: Number of times feature used
- Cover: Number of samples affected

**Expected Performance:**
- **Accuracy:** 80-88%
- **AUC-ROC:** 0.85-0.92
- **Precision:** 75-85%
- **Recall:** 70-82%
- **Training Time:** Moderate (minutes)

**Comparison:**
- **XGBoost:** Slightly higher accuracy, more tuning needed
- **CatBoost:** Better with categorical features, less tuning
- **Recommendation:** Use CatBoost for loan data (many categorical features)

---

### 3. Neural Networks (For Richer Data) 🧠

**Theory:**
Neural networks learn complex non-linear patterns through multiple layers of interconnected neurons.

**Architecture for Loan Default:**

**Simple Feedforward Network:**
```
Input Layer: n features (e.g., 50)
    ↓
Hidden Layer 1: 128 neurons, ReLU activation
Dropout: 0.3
    ↓
Hidden Layer 2: 64 neurons, ReLU activation
Dropout: 0.3
    ↓
Hidden Layer 3: 32 neurons, ReLU activation
    ↓
Output Layer: 1 neuron, Sigmoid activation
```

**Deep Neural Network (For Rich Data):**
```
Input Layer: n features
    ↓
Dense(256) + BatchNorm + ReLU + Dropout(0.3)
    ↓
Dense(128) + BatchNorm + ReLU + Dropout(0.3)
    ↓
Dense(64) + BatchNorm + ReLU + Dropout(0.2)
    ↓
Dense(32) + BatchNorm + ReLU + Dropout(0.2)
    ↓
Dense(1) + Sigmoid
```

**Components:**

**1. Activation Functions:**
- **ReLU:** f(x) = max(0, x) - Prevents vanishing gradients
- **Sigmoid:** f(x) = 1/(1+e^(-x)) - Output layer for probability
- **Tanh:** f(x) = (e^x - e^(-x))/(e^x + e^(-x)) - Alternative to ReLU

**2. Regularization:**
- **Dropout:** Randomly drops neurons during training
  - Prevents overfitting
  - Typical rates: 0.2-0.5
- **L2 Regularization:** Penalizes large weights
- **Early Stopping:** Stop when validation loss stops improving

**3. Batch Normalization:**
- Normalizes layer inputs
- Accelerates training
- Reduces internal covariate shift
- Acts as regularization

**4. Optimization:**
- **Adam:** Adaptive learning rate, momentum
  - Learning rate: 0.001-0.01
- **SGD with Momentum:** Classical approach
- **RMSprop:** Good for RNNs

**Training Process:**
```
1. Initialize weights randomly
2. Forward pass: Compute predictions
3. Calculate loss (binary cross-entropy)
4. Backward pass: Compute gradients
5. Update weights using optimizer
6. Repeat for epochs
```

**Loss Function:**
```
Binary Cross-Entropy:
L = -[y×log(ŷ) + (1-y)×log(1-ŷ)]

Where:
- y = actual label (0 or 1)
- ŷ = predicted probability
```

**Why for Loan Default:**
- **Complex Patterns:** Learns intricate relationships
- **Feature Interactions:** Automatic feature engineering
- **Non-Linear:** Captures non-linear risk patterns
- **Scalable:** Handles large datasets
- **Rich Data:** Excels with many features

**When to Use Neural Networks:**
- Large dataset (>100K samples)
- Many features (>50)
- Complex relationships
- Rich data sources (transaction history, behavioral data)

**Expected Performance:**
- **Accuracy:** 82-90% (with rich data)
- **AUC-ROC:** 0.87-0.94
- **Precision:** 78-88%
- **Recall:** 75-85%
- **Training Time:** Slow (hours for large data)

**Challenges:**
- Requires more data than tree-based models
- Less interpretable (black box)
- Longer training time
- Hyperparameter tuning complex

---

## B. train.py - Theoretical Training Process

### Step 1: Load Application + Repayment History

**Data Sources:**

**1. Loan Application Data:**
```
- applicant_id: Unique identifier
- loan_amount: Requested amount
- loan_purpose: Home, auto, education, business
- employment_type: Salaried, self-employed, unemployed
- annual_income: Yearly income
- employment_length: Years at current job
- home_ownership: Own, rent, mortgage
- address_state: Geographic location
```

**2. Credit History:**
```
- credit_score: FICO/CIBIL score (300-850)
- credit_history_length: Years of credit history
- number_of_credit_lines: Total credit accounts
- revolving_balance: Credit card balances
- revolving_utilization: Balance / Credit limit
- total_accounts: All financial accounts
- derogatory_marks: Negative items on credit report
```

**3. Repayment History:**
```
- delinquencies_2yrs: Late payments in last 2 years
- months_since_last_delinquency: Time since last late payment
- public_records: Bankruptcies, liens, judgments
- inquiries_6months: Hard credit inquiries
- accounts_opened_24months: New accounts recently
```

**4. Loan Performance (Target):**
```
- loan_status: Current, Fully Paid, Default, Charged Off
- default: Binary (1 if defaulted, 0 otherwise)
```

**Data Loading:**
```python
# Conceptual loading
applications = load_csv('loan_applications.csv')
credit_history = load_csv('credit_history.csv')
repayment = load_csv('repayment_history.csv')

# Join tables
data = applications.merge(credit_history, on='applicant_id')
data = data.merge(repayment, on='applicant_id')
```

**Initial Exploration:**
- Dataset size: Typically 10K-1M loans
- Default rate: Usually 10-20%
- Feature count: 30-100 features
- Missing values: Common in financial data

---

### Step 2: Handle Missing Data

**Missing Data Patterns:**

**1. Missing Completely at Random (MCAR):**
- No pattern to missingness
- Safe to delete or impute

**2. Missing at Random (MAR):**
- Missingness depends on other variables
- Can impute using other features

**3. Missing Not at Random (MNAR):**
- Missingness is informative
- Example: High-risk applicants don't report income
- Create "missing" indicator feature

**Strategies:**

**A. Deletion:**
```
# Remove rows with missing target
data = data.dropna(subset=['default'])

# Remove columns with >50% missing
threshold = 0.5
data = data.dropna(thresh=len(data)*threshold, axis=1)
```

**B. Simple Imputation:**
```
# Numerical: Median (robust to outliers)
median_income = data['annual_income'].median()
data['annual_income'].fillna(median_income, inplace=True)

# Categorical: Mode (most frequent)
mode_employment = data['employment_type'].mode()[0]
data['employment_type'].fillna(mode_employment, inplace=True)

# Constant: Fill with specific value
data['months_since_delinquency'].fillna(999, inplace=True)
```

**C. Advanced Imputation:**
```
# KNN Imputation: Use similar samples
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
data_imputed = imputer.fit_transform(data)

# Iterative Imputation: Predict missing values
from sklearn.impute import IterativeImputer
imputer = IterativeImputer(max_iter=10)
data_imputed = imputer.fit_transform(data)
```

**D. Missing Indicator:**
```
# Create binary flag for missingness
data['income_missing'] = data['annual_income'].isna().astype(int)

# Then impute
data['annual_income'].fillna(median_income, inplace=True)
```

**Best Practices:**
- Analyze missing patterns first
- Use domain knowledge
- Create missing indicators for important features
- Validate imputation doesn't introduce bias

---

### Step 3: Compute Risk Features

**A. Income Stability:**

**1. Employment Features:**
```
# Employment length score
employment_score = min(employment_length_years / 10, 1.0)

# Employment type risk
employment_risk = {
    'salaried': 0.2,
    'self_employed': 0.5,
    'unemployed': 1.0,
    'retired': 0.3
}

# Income variability (if historical data available)
income_std = std(last_12_months_income)
income_stability = 1 - (income_std / mean_income)
```

**2. Income-Related Features:**
```
# Income percentile (compared to population)
income_percentile = percentile_rank(annual_income)

# Income growth (if historical)
income_growth = (current_income - income_1yr_ago) / income_1yr_ago

# Multiple income sources
has_multiple_income = (num_income_sources > 1)
```

**B. Debt-to-Income Ratio (DTI):**

**Definition:**
```
DTI = Total Monthly Debt Payments / Gross Monthly Income

Where:
- Total Debt = Mortgage + Car Loan + Credit Cards + Other Loans
- Gross Income = Before-tax monthly income
```

**Calculation:**
```
monthly_income = annual_income / 12

monthly_debt = (
    mortgage_payment +
    auto_loan_payment +
    credit_card_min_payment +
    other_loan_payments +
    proposed_loan_payment  # Include new loan
)

dti_ratio = monthly_debt / monthly_income
```

**DTI Thresholds:**
```
dti < 0.36: Low risk (excellent)
0.36 ≤ dti < 0.43: Moderate risk (acceptable)
0.43 ≤ dti < 0.50: High risk (caution)
dti ≥ 0.50: Very high risk (likely reject)
```

**DTI-Related Features:**
```
# DTI category
dti_category = categorize(dti_ratio)

# DTI with new loan
dti_with_loan = (monthly_debt + new_loan_payment) / monthly_income

# DTI change
dti_increase = dti_with_loan - dti_ratio

# Back-end ratio (housing only)
housing_ratio = (mortgage + insurance + taxes) / monthly_income

# Front-end ratio (all debt)
total_debt_ratio = dti_ratio
```

**C. Delinquency History:**

**1. Delinquency Count Features:**
```
# Recent delinquencies (strong predictor)
delinquencies_last_2yrs = count(late_payments in last 2 years)

# Severity
delinquencies_30days = count(30-59 days late)
delinquencies_60days = count(60-89 days late)
delinquencies_90plus = count(90+ days late)

# Weighted delinquency score
delinquency_score = (
    1.0 × delinquencies_30days +
    2.0 × delinquencies_60days +
    3.0 × delinquencies_90plus
)
```

**2. Recency Features:**
```
# Time since last delinquency
months_since_last_delinquency = current_date - last_delinquency_date

# Recency score (more recent = higher risk)
if months_since_last_delinquency < 6:
    recency_risk = 1.0
elif months_since_last_delinquency < 12:
    recency_risk = 0.7
elif months_since_last_delinquency < 24:
    recency_risk = 0.4
else:
    recency_risk = 0.1
```

**3. Public Records:**
```
# Bankruptcies
bankruptcy_count = count(bankruptcies)
months_since_bankruptcy = current_date - bankruptcy_date

# Liens and judgments
public_record_count = count(liens + judgments + tax_liens)

# Severity score
public_record_score = (
    10.0 × bankruptcy_count +
    5.0 × lien_count +
    3.0 × judgment_count
)
```

**D. Credit Utilization:**

**Definition:**
```
Credit Utilization = Total Revolving Balance / Total Credit Limit
```

**Calculation:**
```
total_balance = sum(all_credit_card_balances)
total_limit = sum(all_credit_card_limits)

utilization_ratio = total_balance / total_limit
```

**Utilization Thresholds:**
```
utilization < 0.30: Excellent (low risk)
0.30 ≤ utilization < 0.50: Good (moderate risk)
0.50 ≤ utilization < 0.75: Fair (high risk)
utilization ≥ 0.75: Poor (very high risk)
```

**Utilization Features:**
```
# Overall utilization
overall_utilization = total_balance / total_limit

# Per-card utilization
max_card_utilization = max(balance_i / limit_i for each card)
avg_card_utilization = mean(balance_i / limit_i for each card)

# Number of maxed-out cards
maxed_cards = count(cards where utilization > 0.9)

# Available credit
available_credit = total_limit - total_balance
```

**E. Credit History Length:**

**Features:**
```
# Total credit history
credit_history_years = (current_date - oldest_account_date) / 365

# Average account age
avg_account_age = mean(current_date - account_open_date for each account)

# Newest account age
newest_account_age = current_date - most_recent_account_date

# Credit mix
num_credit_cards = count(credit card accounts)
num_installment_loans = count(auto, mortgage, personal loans)
num_other_accounts = count(other account types)
```

**F. Inquiry and New Credit:**

**Features:**
```
# Hard inquiries (credit applications)
inquiries_6months = count(hard inquiries in last 6 months)
inquiries_12months = count(hard inquiries in last 12 months)

# New accounts
accounts_opened_24months = count(accounts opened in last 2 years)

# Credit shopping behavior
inquiry_rate = inquiries_6months / 6  # Per month

# Multiple inquiries (red flag)
has_multiple_inquiries = (inquiries_6months > 3)
```

**G. Loan-Specific Features:**

**Features:**
```
# Loan amount relative to income
loan_to_income = loan_amount / annual_income

# Loan amount relative to collateral (if secured)
loan_to_value = loan_amount / collateral_value

# Loan purpose risk
purpose_risk = {
    'debt_consolidation': 0.6,
    'credit_card': 0.7,
    'home_improvement': 0.4,
    'major_purchase': 0.5,
    'medical': 0.8,
    'car': 0.3,
    'business': 0.7,
    'vacation': 0.9
}

# Loan term
loan_term_months = loan_term_years × 12

# Monthly payment
monthly_payment = loan_amount × (interest_rate / 12) / (1 - (1 + interest_rate/12)^(-loan_term_months))

# Payment to income ratio
payment_to_income = monthly_payment / monthly_income
```

**H. Derived Interaction Features:**

**Features:**
```
# DTI × Credit Score
dti_credit_interaction = dti_ratio × (1 - credit_score/850)

# Income × Employment Length
income_stability = annual_income × employment_length

# Delinquencies × Utilization
risk_compound = delinquencies_2yrs × utilization_ratio

# Loan Amount × DTI
loan_risk = loan_amount × dti_ratio
```

**Feature Scaling:**
```
# Standardization (for neural networks)
feature_scaled = (feature - mean) / std

# Min-Max scaling
feature_scaled = (feature - min) / (max - min)

# Log transformation (for skewed features like income)
feature_log = log(1 + feature)
```

---

### Step 4: Train CatBoost

**Training Process:**

**1. Data Preparation:**
```
# Split features and target
X = data.drop(['default', 'applicant_id'], axis=1)
y = data['default']

# Identify categorical features
categorical_features = ['employment_type', 'home_ownership', 'loan_purpose', 'address_state']

# Train-test split (temporal if possible)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**2. Model Configuration:**
```
from catboost import CatBoostClassifier

model = CatBoostClassifier(
    iterations=500,
    depth=6,
    learning_rate=0.05,
    l2_leaf_reg=3,
    loss_function='Logloss',
    eval_metric='AUC',
    auto_class_weights='Balanced',  # Handle imbalance
    cat_features=categorical_features,
    random_seed=42,
    verbose=50
)
```

**3. Training:**
```
# Train with validation set
model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    early_stopping_rounds=50,
    plot=True
)
```

**4. Feature Importance:**
```
# Get feature importance
feature_importance = model.get_feature_importance()

# Sort by importance
importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

# Top 10 features
print(importance_df.head(10))
```

**Expected Top Features:**
1. Credit score
2. DTI ratio
3. Delinquencies (last 2 years)
4. Credit utilization
5. Annual income
6. Employment length
7. Loan amount
8. Public records
9. Inquiries (6 months)
10. Credit history length

---

### Step 5: Evaluate with AUC

**Evaluation Metrics:**

**A. AUC-ROC (Area Under ROC Curve):**

**Theory:**
- ROC curve plots True Positive Rate vs. False Positive Rate
- AUC measures overall model performance
- Range: 0.5 (random) to 1.0 (perfect)

**Interpretation:**
```
AUC = 0.50: Random guessing
AUC = 0.60-0.70: Poor
AUC = 0.70-0.80: Fair
AUC = 0.80-0.90: Good
AUC = 0.90-1.00: Excellent
```

**Calculation:**
```python
from sklearn.metrics import roc_auc_score, roc_curve

# Predict probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate AUC
auc = roc_auc_score(y_test, y_pred_proba)
print(f"AUC-ROC: {auc:.4f}")

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
```

**B. Precision-Recall AUC:**

**Why Important:**
- Better for imbalanced data (loan defaults are rare)
- Focuses on positive class (defaults)

**Calculation:**
```python
from sklearn.metrics import average_precision_score, precision_recall_curve

# PR-AUC
pr_auc = average_precision_score(y_test, y_pred_proba)
print(f"PR-AUC: {pr_auc:.4f}")

# PR curve
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
```

**C. Confusion Matrix:**

```
                Predicted
              No Default  Default
Actual No Default   TN      FP
       Default      FN      TP
```

**Metrics:**
```
Precision = TP / (TP + FP)  # Of predicted defaults, % actually default
Recall = TP / (TP + FN)     # Of actual defaults, % detected
F1 = 2 × (Precision × Recall) / (Precision + Recall)
Accuracy = (TP + TN) / Total
```

**D. Business Metrics:**

**Cost-Based Evaluation:**
```
# Define costs
cost_FN = loan_amount × (1 - recovery_rate)  # Missed default (loss)
cost_FP = opportunity_cost  # Rejected good loan (lost profit)

# Total cost
total_cost = (FN × cost_FN) + (FP × cost_FP)

# Profit
profit_TP = loan_amount × interest_rate × loan_term
profit_TN = 0  # Correctly rejected, no profit

# Total profit
total_profit = (TP × profit_TP) - total_cost
```

**Threshold Selection:**
```
# Find optimal threshold
best_threshold = 0.5
best_profit = -inf

for threshold in np.linspace(0, 1, 100):
    y_pred = (y_pred_proba > threshold).astype(int)
    profit = calculate_profit(y_test, y_pred)
    
    if profit > best_profit:
        best_profit = profit
        best_threshold = threshold
```

---

### Step 6: Save Model

**Model Artifacts:**
```
models/
├── catboost_model.cbm          # CatBoost model
├── logistic_regression.pkl     # Logistic Regression
├── neural_network.h5           # Neural Network weights
├── feature_scaler.pkl          # StandardScaler
├── feature_names.pkl           # Feature list
├── categorical_encoders.pkl    # Label encoders
└── metadata.json               # Training metadata
```

**Metadata:**
```json
{
  "training_date": "2024-01-15",
  "model_type": "CatBoostClassifier",
  "dataset_size": 50000,
  "default_rate": 0.15,
  "features": ["credit_score", "dti_ratio", ...],
  "categorical_features": ["employment_type", ...],
  "performance": {
    "auc_roc": 0.87,
    "pr_auc": 0.72,
    "precision": 0.78,
    "recall": 0.75,
    "f1": 0.76
  },
  "optimal_threshold": 0.42,
  "feature_importance": [...],
  "hyperparameters": {...}
}
```

---

## C. Real-Time Inference - Theoretical Design

### Architecture

```
Loan Application
    ↓
[Data Validation]
    ↓
[Feature Engineering]
    ↓
[Model Inference]
    ↓
[Risk Scoring]
    ↓
[Decision Engine]
    ↓
Approve / Reject / Manual Review
```

**Latency Target:** <500ms

---

### Step 1: Loan Application Input

**Application Data:**
```json
{
  "applicant_id": "APP_123456",
  "loan_amount": 250000,
  "loan_purpose": "home_improvement",
  "loan_term_years": 5,
  "interest_rate": 0.12,
  "annual_income": 800000,
  "employment_type": "salaried",
  "employment_length_years": 5,
  "home_ownership": "own",
  "address_state": "Maharashtra",
  "credit_score": 720,
  "delinquencies_2yrs": 0,
  "revolving_balance": 50000,
  "revolving_utilization": 0.35,
  "inquiries_6months": 1,
  "public_records": 0
}
```

**Validation:**
- Required fields present
- Data types correct
- Value ranges valid
- Business rules (e.g., loan_amount > 0)

---

### Step 2: Feature Engineering (Real-Time)

**Compute Risk Features:**

```python
# DTI Ratio
monthly_income = annual_income / 12
monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term_years)
dti_ratio = monthly_payment / monthly_income

# Loan-to-Income
loan_to_income = loan_amount / annual_income

# Credit Score Category
if credit_score >= 750:
    credit_category = 'excellent'
elif credit_score >= 700:
    credit_category = 'good'
elif credit_score >= 650:
    credit_category = 'fair'
else:
    credit_category = 'poor'

# Risk Flags
high_utilization = (revolving_utilization > 0.5)
recent_delinquency = (delinquencies_2yrs > 0)
multiple_inquiries = (inquiries_6months > 3)
has_public_records = (public_records > 0)

# Composite Scores
income_stability_score = employment_length_years / 10
debt_burden_score = dti_ratio + revolving_utilization

# Feature Vector
features = [
    credit_score,
    dti_ratio,
    annual_income,
    loan_amount,
    employment_length_years,
    delinquencies_2yrs,
    revolving_utilization,
    inquiries_6months,
    public_records,
    loan_to_income,
    # ... all engineered features
]
```

---

### Step 3: Model Inference

**Load Model:**
```python
# Load pre-trained model
model = load_model('catboost_model.cbm')
scaler = load_scaler('feature_scaler.pkl')
```

**Predict:**
```python
# Scale features (if needed)
features_scaled = scaler.transform([features])

# Predict probability
default_probability = model.predict_proba(features_scaled)[0][1]
```

**Latency:** <100ms

---

### Step 4: Risk Scoring

**Risk Score Calculation:**
```python
# Convert probability to risk score (0-1000)
risk_score = int(default_probability * 1000)

# Risk Grade
if risk_score < 200:
    risk_grade = 'A'  # Excellent
elif risk_score < 400:
    risk_grade = 'B'  # Good
elif risk_score < 600:
    risk_grade = 'C'  # Fair
elif risk_score < 800:
    risk_grade = 'D'  # Poor
else:
    risk_grade = 'E'  # Very Poor

# Risk Level
if default_probability < 0.10:
    risk_level = 'LOW'
elif default_probability < 0.25:
    risk_level = 'MEDIUM'
elif default_probability < 0.50:
    risk_level = 'HIGH'
else:
    risk_level = 'VERY_HIGH'
```

---

### Step 5: Decision Engine

**Decision Rules:**

**AUTO-APPROVE (Low Risk):**
```
Conditions:
- default_probability < 0.10
- credit_score >= 700
- dti_ratio < 0.36
- delinquencies_2yrs == 0
- public_records == 0

Action: Approve immediately
Interest Rate: Prime rate
Loan Terms: Standard
```

**MANUAL REVIEW (Medium Risk):**
```
Conditions:
- 0.10 ≤ default_probability < 0.30
- 650 ≤ credit_score < 700
- 0.36 ≤ dti_ratio < 0.43
- delinquencies_2yrs ≤ 2

Action: Send to underwriter
Required: Additional documentation
Timeline: 2-5 business days
```

**AUTO-REJECT (High Risk):**
```
Conditions:
- default_probability ≥ 0.50
- credit_score < 600
- dti_ratio ≥ 0.50
- delinquencies_2yrs > 3
- public_records > 0

Action: Reject application
Reason: High default risk
Alternative: Suggest credit counseling
```

**CONDITIONAL APPROVAL (Medium-High Risk):**
```
Conditions:
- 0.25 ≤ default_probability < 0.40
- 600 ≤ credit_score < 700

Action: Approve with conditions
Conditions:
  - Higher interest rate (+2-5%)
  - Shorter loan term
  - Require co-signer
  - Lower loan amount
```

---

### Step 6: Response

**Response Format:**
```json
{
  "applicant_id": "APP_123456",
  "decision": "APPROVE",
  "risk_score": 150,
  "risk_grade": "A",
  "risk_level": "LOW",
  "default_probability": 0.08,
  "confidence": 0.92,
  "approved_amount": 250000,
  "interest_rate": 0.12,
  "loan_term_years": 5,
  "monthly_payment": 5565,
  "key_factors": [
    "Excellent credit score (720)",
    "Low DTI ratio (0.28)",
    "Stable employment (5 years)",
    "No delinquencies"
  ],
  "risk_factors": [
    "Moderate credit utilization (35%)"
  ],
  "processing_time_ms": 287,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**For Manual Review:**
```json
{
  "decision": "MANUAL_REVIEW",
  "risk_score": 420,
  "risk_grade": "C",
  "risk_level": "MEDIUM",
  "default_probability": 0.22,
  "review_priority": "STANDARD",
  "required_documents": [
    "Last 3 months bank statements",
    "Employment verification letter",
    "Tax returns (last 2 years)"
  ],
  "underwriter_notes": "Verify income stability and recent credit inquiries",
  "estimated_review_time": "2-3 business days"
}
```

---

## Expected System Performance

### Model Performance:
- **CatBoost AUC-ROC:** 0.85-0.92
- **Logistic Regression AUC-ROC:** 0.70-0.75
- **Neural Network AUC-ROC:** 0.87-0.94 (with rich data)

### Business Metrics:
- **Approval Rate:** 60-70%
- **Default Rate (Approved Loans):** 5-8%
- **False Positive Rate:** <15% (good loans rejected)
- **False Negative Rate:** <10% (bad loans approved)

### Processing:
- **Latency:** <500ms
- **Throughput:** 1000+ applications/minute
- **Availability:** 99.9%

---

## Conclusion

This Loan Default Risk Prediction system combines:
- **Logistic Regression** for interpretability and regulatory compliance
- **CatBoost** for high accuracy and production deployment
- **Neural Networks** for complex patterns in rich data

The real-time inference pipeline processes applications in <500ms, providing risk scores and automated decisions while maintaining high accuracy (85-92% AUC-ROC) and business profitability.

