
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
)

# Initialize DB
init_db()

# Premium CSS - Direct & Robust
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }

    /* Main Background */
    .stApp {
        background: #f8fafc;
    }

    /* Styling Headers */
    h1 {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .sub-heading {
        color: #64748b;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Input Field Labels */
    label {
        font-weight: 600 !important;
        color: #475569 !important;
    }

    /* Predict Button */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        height: 3.5rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Result Cards */
    .res-card {
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white !important;
        margin: 1.5rem 0;
    }
    .res-card * { color: white !important; }
    .res-stay { background: linear-gradient(135deg, #059669, #10b981) !important; }
    .res-exit { background: linear-gradient(135deg, #e11d48, #f43f5e) !important; }

    /* Fix for Streamlit's default container borders */
    [data-testid="stExpander"], [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e2e8f0 !important;
        background-color: white !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1>Bank Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-heading'>Advanced Machine Learning Analytics for Banking Proactive Retention</div>", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    return joblib.load('churn_model.pkl')

model = load_model()

# Form Section
with st.container(border=True):
    st.subheader("👤 Customer Demographics")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Customer Age", 18, 100, 45)
        gender = st.selectbox("Gender", list(GENDER_MAP.keys()))
        dependents = st.number_input("Dependent Count", 0, 10, 3)
    with c2:
        education = st.selectbox("Education Level", list(EDUCATION_MAP.keys()))
        marital = st.selectbox("Marital Status", list(MARITAL_MAP.keys()))
        income = st.selectbox("Income Category", list(INCOME_MAP.keys()))
    with c3:
        card = st.selectbox("Card Category", list(CARD_MAP.keys()))
        months_on_book = st.number_input("Months on Book", 1, 120, 36)
        rel_count = st.number_input("Relationship Count", 1, 6, 3)

    st.divider()

    st.subheader("💳 Financial Behavior")
    c4, c5, c6 = st.columns(3)
    with c4:
        months_inactive = st.number_input("Months Inactive (12m)", 0, 12, 1)
        contacts = st.number_input("Contacts (12m)", 0, 10, 2)
        limit = st.number_input("Credit Limit ($)", 0.0, 100000.0, 5000.0)
    with c5:
        revolving = st.number_input("Revolving Balance ($)", 0.0, 50000.0, 1500.0)
        open_buy = st.number_input("Avg Open to Buy ($)", 0.0, 100000.0, 3500.0)
        amt_change = st.number_input("Amt Change (Q4 vs Q1)", 0.0, 10.0, 0.7)
    with c6:
        trans_amt = st.number_input("Total Trans Amt ($)", 0.0, 50000.0, 2500.0)
        trans_ct = st.number_input("Total Trans Count", 0, 200, 45)
        ct_change = st.number_input("Ct Change (Q4 vs Q1)", 0.0, 10.0, 0.8)

    util_ratio = st.slider("Avg Utilization Ratio", 0.0, 1.0, 0.1, step=0.01)
    
    st.write(" ")
    if st.button("🚀 PREDICT CUSTOMER LOYALTY STATUS", use_container_width=True):
        # Prediction Logic
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
        processed = [
            age, GENDER_MAP[gender], dependents, EDUCATION_MAP[education],
            MARITAL_MAP[marital], INCOME_MAP[income], CARD_MAP[card],
            months_on_book, rel_count, months_inactive, contacts, limit,
            revolving, open_buy, amt_change, trans_amt, trans_ct, ct_change, util_ratio
        ]
        prediction = model.predict([processed])[0]
        probs = model.predict_proba([processed])[0]
        confidence = float(max(probs))
        status = "Stay" if prediction == 1 else "Exit"
        save_prediction(data, status, confidence)

        # Result Display
        res_class = "res-stay" if status == "Stay" else "res-exit"
        res_label = "LOYAL" if status == "Stay" else "AT RISK"
        res_icon = "✅" if status == "Stay" else "⚠️"
        
        st.markdown(f'''
            <div class="res-card {res_class}">
                <h2 style="margin:0;">{res_icon} CUSTOMER STATUS: {res_label}</h2>
                <h1 style="font-size: 4.5rem; margin: 0.5rem 0; color: white !important;">{confidence*100:.1f}%</h1>
                <p style="font-weight: 600; font-size: 1.1rem; opacity: 0.9;">MODEL PREDICTION CONFIDENCE</p>
            </div>
        ''', unsafe_allow_html=True)

# Analytics Section
st.write(" ")
st.header("📊 Prediction History & Insights")
history = get_history(50)

if history:
    df_h = pd.DataFrame(history)
    ch, dt = st.columns([2, 1])
    
    with ch:
        with st.container(border=True):
            df_h['time'] = pd.to_datetime(df_h['timestamp']).dt.strftime('%H:%M:%S')
            fig = px.area(df_h.sort_values('timestamp'), x="time", y="confidence", 
                          title="Confidence Trend (Latest Predictions)",
                          line_shape="spline", template="plotly_white")
            fig.update_traces(line_color='#3b82f6', fillcolor="rgba(59, 130, 246, 0.1)")
            fig.update_layout(yaxis_range=[0, 1.05], font_family="Inter", height=350, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with dt:
        with st.container(border=True):
            st.subheader("Logs")
            st.dataframe(
                df_h[['time', 'prediction', 'confidence']].head(10),
                column_config={
                    "time": "Time",
                    "prediction": "Status",
                    "confidence": st.column_config.ProgressColumn("Conf", format="%.2f", min_value=0, max_value=1)
                },
                hide_index=True,
                use_container_width=True
            )
else:
    st.info("Analytics will populate after your first prediction.")
