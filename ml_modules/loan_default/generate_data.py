"""
Loan Default Prediction - Enhanced Dataset Generator
Generates realistic loan application data with detailed credit and repayment history
"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)

def generate_loan_data(n_samples=10000):
    """Generate synthetic loan data with rich features"""
    
    data = []
    
    for i in range(n_samples):
        # Applicant features
        income = np.random.lognormal(11, 0.5)  # Annual income
        age = np.random.randint(21, 65)
        employment_length = np.random.randint(0, 40)
        home_ownership = np.random.choice(['RENT', 'OWN', 'MORTGAGE'], p=[0.4, 0.1, 0.5])
        
        # Loan features
        loan_amount = np.random.randint(1000, 50000)
        loan_intent = np.random.choice(['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'])
        loan_grade = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        interest_rate = np.random.uniform(5, 25)
        
        # Credit History & Repayment Behavior (New Features)
        delinquencies_2yrs = np.random.poisson(0.3)  # Number of late payments
        revolving_utilization = np.random.beta(2, 5)  # Credit card utilization (0-1)
        total_accounts = np.random.randint(2, 30)
        inquiries_6months = np.random.poisson(0.5)
        public_records = np.random.choice([0, 1], p=[0.95, 0.05])
        
        # Derived Ratios
        monthly_income = income / 12
        # Approx monthly debt (simplified)
        monthly_debt = (income * np.random.uniform(0.1, 0.6)) / 12 
        dti_ratio = monthly_debt / monthly_income
        
        loan_percent_income = loan_amount / income
        
        # Determine default risk (Complex logic)
        risk_score = 0
        
        # Income & Debt factors
        if loan_percent_income > 0.4: risk_score += 0.3
        if dti_ratio > 0.43: risk_score += 0.25
        if income < 30000: risk_score += 0.2
        
        # Credit History factors
        if delinquencies_2yrs > 0: risk_score += 0.15 * delinquencies_2yrs
        if revolving_utilization > 0.7: risk_score += 0.2
        if inquiries_6months > 2: risk_score += 0.15
        if public_records > 0: risk_score += 0.3
        
        # Loan factors
        if interest_rate > 15: risk_score += 0.15
        if employment_length < 2: risk_score += 0.1
        if loan_grade in ['D', 'E', 'F', 'G']: risk_score += 0.2
        
        # Random noise
        risk_score += np.random.normal(0, 0.1)
        
        # Target
        loan_status = 1 if risk_score > 0.7 else 0
        
        data.append({
            'person_age': age,
            'person_income': round(income, 2),
            'person_home_ownership': home_ownership,
            'person_emp_length': employment_length,
            'loan_intent': loan_intent,
            'loan_grade': loan_grade,
            'loan_amnt': loan_amount,
            'loan_int_rate': round(interest_rate, 2),
            'loan_percent_income': round(loan_percent_income, 2),
            'cb_person_default_on_file': 'Y' if delinquencies_2yrs > 0 else 'N', # Legacy field
            'cb_person_cred_hist_length': np.random.randint(2, 30),
            
            # New Rich Features
            'dti_ratio': round(dti_ratio, 2),
            'delinquencies_2yrs': delinquencies_2yrs,
            'revolving_utilization': round(revolving_utilization, 2),
            'total_accounts': total_accounts,
            'inquiries_6months': inquiries_6months,
            'public_records': public_records,
            
            'loan_status': loan_status
        })
        
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} loan records")
    print(f"Default rate: {df['loan_status'].mean():.2%}")
    
    return df

if __name__ == "__main__":
    df = generate_loan_data()
    df.to_csv('loan_data.csv', index=False)
    print("Saved to loan_data.csv")
