
import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from constants import GENDER_MAP, EDUCATION_MAP, MARITAL_MAP, INCOME_MAP, CARD_MAP, FEATURE_COLUMNS
from database import save_prediction, get_history, init_db

# Page Config
st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize DB
init_db()

# Custom CSS for Premium Design
st.markdown("""
    <style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Transparent Header */
    header { background: rgba(0,0,0,0) !important; }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Input Field Styling */
    .stNumberInput input, .stSelectbox [data-baseweb="select"] {
        border-radius: 12px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 10px !important;
    }
    
    /* Custom Title */
    .main-title {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #64748b;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Prediction Card */
    .res-card {
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .res-stay { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
    .res-exit { background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
    }

    /* Column Spacing */
    [data-testid="column"] {
        padding: 0 1rem;
    }

    /* Mobile adjustments */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .glass-card { padding: 1.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

# App Content
st.markdown('<h1 class="main-title">Bank Customer Churn Prediction</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced ML Analytics for Proactive Customer Retention</p>', unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    return joblib.load('churn_model.pkl')

model = load_model()

# Form Container
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("👤 Customer Demographics")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Customer Age", 18, 100, 45, help="Age of the client in years")
    gender = st.selectbox("Gender", list(GENDER_MAP.keys()))
    dependents = st.number_input("Dependent Count", 0, 10, 3)

with col2:
    education = st.selectbox("Education Level", list(EDUCATION_MAP.keys()))
    marital = st.selectbox("Marital Status", list(MARITAL_MAP.keys()))
    income = st.selectbox("Income Category", list(INCOME_MAP.keys()))

with col3:
    card = st.selectbox("Card Category", list(CARD_MAP.keys()))
    months_on_book = st.number_input("Months on Book", 1, 120, 36, help="Period of relationship with bank")
    rel_count = st.number_input("Relationship Count", 1, 6, 3, help="Total number of products held")

st.markdown('<hr style="border-color: rgba(0,0,0,0.05)">', unsafe_allow_html=True)
st.subheader("💳 Financial Performance & Activity")
col4, col5, col6 = st.columns(3)

with col4:
    months_inactive = st.number_input("Months Inactive (12m)", 0, 12, 1)
    contacts = st.number_input("Contacts (12m)", 0, 10, 2)
    limit = st.number_input("Credit Limit ($)", 0.0, 100000.0, 5000.0)

with col5:
    revolving = st.number_input("Revolving Balance ($)", 0.0, 50000.0, 1500.0)
    open_buy = st.number_input("Avg Open to Buy ($)", 0.0, 100000.0, 3500.0)
    amt_change = st.number_input("Amt Change (Q4 vs Q1)", 0.0, 10.0, 0.7)

with col6:
    trans_amt = st.number_input("Total Trans Amt ($)", 0.0, 50000.0, 2500.0)
    trans_ct = st.number_input("Total Trans Count", 0, 200, 45)
    ct_change = st.number_input("Ct Change (Q4 vs Q1)", 0.0, 10.0, 0.8)

# Utilization ratio on its own line for emphasis
util_ratio = st.slider("Avg Utilization Ratio", 0.0, 1.0, 0.1, step=0.01)

if st.button("🚀 PREDICT CUSTOMER LOYALTY"):
    # Data Prep
    data = {
        'customer_age': age, 'gender': gender, 'dependent_count': dependents,
        'education_level': education, 'marital_status': marital, 'income_category': income,
        'card_category': card, 'months_on_book': months_on_book,
        'total_relationship_count': rel_count, 'months_inactive_12_mon': months_inactive,
        'contacts_count_12_mon': contacts, 'credit_limit': limit,
        'total_revolving_bal': revolving, 'avg_open_to_buy': open_buy,
        'total_amt_chng_q4_q1': amt_change, 'total_trans_amt': trans_amt,
        'total_trans_ct': trans_ct, 'total_ct_chng_q4_q1': ct_change,
        'avg_utilization_ratio': util_ratio
    }
    
    # Preprocess for model
    processed = [
        age, GENDER_MAP[gender], dependents, EDUCATION_MAP[education],
        MARITAL_MAP[marital], INCOME_MAP[income], CARD_MAP[card],
        months_on_book, rel_count, months_inactive, contacts, limit,
        revolving, open_buy, amt_change, trans_amt, trans_ct, ct_change, util_ratio
    ]
    
    # Prediction
    prediction = model.predict([processed])[0]
    probs = model.predict_proba([processed])[0]
    confidence = float(max(probs))
    status = "Stay" if prediction == 1 else "Exit"
    
    # Save to history
    save_prediction(data, status, confidence)
    
    # Result UI
    if status == "Stay":
        st.markdown(f'''
            <div class="res-card res-stay">
                <h2>✅ CUSTOMER STATUS: LOYAL</h2>
                <p style="font-size: 1.2rem; opacity: 0.9;">High probability of retention</p>
                <h1 style="font-size: 4rem; margin: 0;">{confidence*100:.1f}%</h1>
                <p>MATCH CONFIDENCE</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="res-card res-exit">
                <h2>⚠️ CUSTOMER STATUS: AT RISK</h2>
                <p style="font-size: 1.2rem; opacity: 0.9;">High probability of churn</p>
                <h1 style="font-size: 4rem; margin: 0;">{confidence*100:.1f}%</h1>
                <p>MATCH CONFIDENCE</p>
            </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# History Section
st.header("📊 Prediction Analytics & History")
history = get_history(50)

if history:
    df_h = pd.DataFrame(history)
    
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
        # Use simple time for x axis
        df_h['time'] = pd.to_datetime(df_h['timestamp']).dt.strftime('%H:%M:%S')
        fig = px.area(df_h.sort_values('timestamp'), x="time", y="confidence", 
                      title="Model Prediction Confidence Trend",
                      line_shape="spline",
                      color_discrete_sequence=["#3b82f6"])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[0, 1.05],
            font_family="Inter",
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_data:
        st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
        st.subheader("Recent Logs")
        st.dataframe(
            df_h[['time', 'prediction', 'confidence']].head(10),
            column_config={
                "time": "Time",
                "prediction": "Status",
                "confidence": st.column_config.ProgressColumn("Confidence", format="%.2f", min_value=0, max_value=1)
            },
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Start predicting to see analytics here.")
