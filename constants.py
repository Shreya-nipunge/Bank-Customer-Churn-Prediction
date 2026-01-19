
GENDER_MAP = {'M': 0, 'F': 1}
EDUCATION_MAP = {
    'Graduate': 0, 
    'High School': 1, 
    'Unknown': 2, 
    'Uneducated': 3, 
    'College': 4, 
    'Post-Graduate': 5, 
    'Doctorate': 6
}
MARITAL_MAP = {'Married': 0, 'Single': 1, 'Unknown': 2, 'Divorced': 3}
INCOME_MAP = {
    '$60K - $80K': 0, 
    'Less than $40K': 1, 
    '$80K - $120K': 2, 
    '$120K +': 3, 
    '$40K - $60K': 4, 
    'Unknown': 5
}
CARD_MAP = {'Blue': 0, 'Gold': 1, 'Silver': 2, 'Platinum': 3}

TARGET_MAP = {'Existing Customer': 1, 'Attrited Customer': 0}

FEATURE_COLUMNS = [
    'Customer_Age', 'Gender', 'Dependent_count', 'Education_Level',
    'Marital_Status', 'Income_Category', 'Card_Category', 'Months_on_book',
    'Total_Relationship_Count', 'Months_Inactive_12_mon',
    'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
    'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
    'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'
]
