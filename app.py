import streamlit as st
import pandas as pd
import joblib
from background_icons import add_local_background_icons

# FIRST: add icons
add_local_background_icons()

# SECOND: apply custom style.css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# THIRD: extra inline styles (optional)
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #281A0D ;  
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True
)

# Load ML model
model = joblib.load("logreg_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# App title
st.title("🏦 Loan Prediction App")

st.write("Enter customer details below and click **Predict** to check loan approval status.")
col1, col2, col3 = st.columns(3)

# Input fields
def get_numeric_input(label):
    val = st.text_input(label)
    if val.strip() == "":
        return None
    try:
        return float(val)
    except:
        return None
    
# Collect form inputs
with col1:
    name = st.text_input("Customer Name")
    income = get_numeric_input("Annual Income")
    avg_bal = get_numeric_input("Average Balance in Account")
    gender = st.selectbox("Customer Gender", ["", "Male", "Female", "Prefer not to say"])
    risk_type = st.selectbox("Risk Type", ["", "Low", "Medium", "High"])
    aadhaar_option = st.selectbox("Have Aadhaar?", ["", "Yes", "No"])

with col2:
    mobile_no = st.text_input("Mobile No")
    disbursement = get_numeric_input("Disbursement Amount")
    emi = get_numeric_input("EMI Amount")
    marital_status = st.selectbox("Marital Status", ["", "Single", "Married"])
    kyc = st.selectbox("KYC Complete?", ["", "Yes", "No"])
    pan_option = st.selectbox("Have PAN?", ["", "Yes", "No"])

with col3:
    age = get_numeric_input("Customer Age")
    liabilities = get_numeric_input("Current Liabilities Amount")
    interest = get_numeric_input("Interest Rate")
    education = st.selectbox("Education", ["", "Student", "Graduate", "Professional", "Other"])
    account_type = st.selectbox("Account Type", ["", "Savings", "Current", "Fixed Deposit"])

# Button
if st.button("Predict"):

    # Step 1: Check Aadhaar and PAN
    if aadhaar_option != "Yes" or pan_option != "Yes":
        st.error("Application Rejected: Aadhaar or PAN not provided.")
        st.stop()

    # Step 2: Check critical values
    missing_fields = []
    if not age or age <= 0:
        missing_fields.append("Customer Age")
    if not income or income <= 0:
        missing_fields.append("Annual Income")
    if not disbursement or disbursement <= 0:
        missing_fields.append("Disbursement Amount")
    if not interest or interest <= 0:
        missing_fields.append("Interest Rate")
    if not liabilities or liabilities <= 0:
        missing_fields.append("Current Liabilities")
    if not avg_bal or avg_bal <= 0:
        missing_fields.append("Average Balance in Account")
    if not emi or emi <= 0:
        missing_fields.append("EMI Amount")
    if name == "" or name is None:
        missing_fields.append('Customer Name')
    if not mobile_no or mobile_no <=0:
        missing_fields.append('Mobile No')
    if gender == "" or gender is None:
        missing_fields.append("Customer Gender")
    if marital_status == "" or marital_status is None:
        missing_fields.append("Marital Status")
    if education == "" or education is None:
        missing_fields.append("Education")
    if risk_type == "" or risk_type is None:
        missing_fields.append("Risk Type")
    if kyc == "" or kyc is None:
        missing_fields.append("KYC Complete")
    if account_type == "" or account_type is None:
        missing_fields.append("Account Type")
 

    if missing_fields:
        st.error("Please fill all the required fields:")
        st.stop()

    # Step 3: Prepare dataframe
    input_data = pd.DataFrame([{
        'CUSTOMER_AGE': age or 0,
        'ANNUAL_INCOME': income or 0,
        'DISBURSEMENT_AMOUNT': disbursement or 0,
        'CURR_LIAB_AMT': liabilities or 0,
        'AVG_BAL_IN_ACCOUNT': avg_bal or 0,
        'EMI_AMOUNT': emi or 0,
        'INTEREST_RATE': interest or 0,
        'CUSTOMER_GENDER': gender,
        'MARTIAL_STATUS': marital_status,
        'EDUCATION_DESC': education,
        'RISK_TYPE_DESC': risk_type,
        'KYC_COMPLETE_FLAG': kyc,
        'ACCOUNT_TYPE': account_type
    }])

    # Step 4: One-hot encoding and match model columns
    cat_cols = ['CUSTOMER_GENDER', 'MARTIAL_STATUS', 'EDUCATION_DESC',
                'RISK_TYPE_DESC', 'KYC_COMPLETE_FLAG', 'ACCOUNT_TYPE']
    input_encoded = pd.get_dummies(input_data, columns=cat_cols, drop_first=True)

    # Add missing columns if needed
    for col in model_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[model_columns]

    # Step 5: Predict
    prediction = model.predict(input_encoded)[0]
    result = "✅ Approved" if prediction == 1 else "❌ Not Approved"
    st.success(f"Loan Application Status: {result}")
