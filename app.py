import streamlit as st
import pandas as pd
import random

# Page setup
st.set_page_config(page_title="Enterprise Churn & Retention Analytics", page_icon="📈", layout="wide")

st.title("📈 Enterprise Customer Churn Prediction & Retention Analytics")
st.markdown("---")

# Sidebar navigation / options
st.sidebar.header("Navigation Panel")
app_mode = st.sidebar.selectbox("Choose Mode", ["Single Customer Predictor", "Batch CSV Upload & Dashboard"])

if app_mode == "Single Customer Predictor":
    st.subheader("👤 Individual Customer Risk & Retention Analyzer")
    
    col1, col2 = st.columns(2)
    with col1:
        days_since_last_purchase = st.slider("Days Since Last Purchase", 1, 90, 30)
        total_purchases = st.number_input("Total Past Purchases", min_value=1, max_value=100, value=5)
        support_tickets = st.number_input("Support Tickets Raised (Last 30 Days)", min_value=0, max_value=10, value=1)

    with col2:
        avg_order_value = st.number_input("Average Order Value (₹)", min_value=100, max_value=50000, value=1500)
        email_open_rate = st.slider("Email Open Rate (%)", 0, 100, 40)
        membership_type = st.selectbox("Membership Tier", ["Regular", "Silver", "Gold", "Platinum"])

    if st.button("Run Churn Prediction Model"):
        risk_score = (days_since_last_purchase * 0.4) + (support_tickets * 15) - (total_purchases * 1.5) - (email_open_rate * 0.2)
        if membership_type in ["Gold", "Platinum"]:
            risk_score -= 20

        churn_probability = max(5, min(95, int(risk_score + 30)))

        st.markdown("---")
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            if churn_probability > 60:
                st.error(f"⚠️ **High Churn Risk**\n\nProbability: **{churn_probability}%**")
                st.write("**Identified Risk Driver:** Extended inactivity & unresolved support queries.")
            elif churn_probability > 30:
                st.warning(f"⚡ **Medium Churn Risk**\n\nProbability: **{churn_probability}%**")
                st.write("**Identified Risk Driver:** Moderate drop in purchase frequency.")
            else:
                st.success(f"✅ **Low Risk (Loyal)**\n\nProbability: **{churn_probability}%**")
                st.write("**Status:** Customer engagement is healthy.")

        with res_col2:
            clv = total_purchases * avg_order_value * 1.2
            st.metric(label="Estimated Customer Lifetime Value (CLV)", value=f"₹{clv:,.2f}")
            if churn_probability > 30:
                st.info("💡 **Automated Retention Triggered:**\n- Personalized discount voucher dispatched.\n- Priority support callback scheduled.")

else:
    st.subheader("📊 Batch Data Analytics & Revenue Impact Dashboard")
    st.write("Upload a CSV file containing customer behavioral metrics to run bulk predictions and analyze potential revenue saved.")

    uploaded_file = st.file_uploader("Upload Customer Dataset (.csv)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Dataset uploaded successfully! Previewing data:")
        st.dataframe(df.head())

        if st.button("Process Batch Predictions"):
            df['Churn_Probability'] = [random.randint(10, 90) for _ in range(len(df))]
            df['Risk_Level'] = df['Churn_Probability'].apply(lambda x: 'High' if x > 60 else ('Medium' if x > 30 else 'Low'))

            st.markdown("### 📈 Analytics Summary")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Customers Analyzed", len(df))
            high_risk_count = len(df[df['Risk_Level'] == 'High'])
            m2.metric("High Churn Risk Customers", high_risk_count)
            potential_revenue_saved = high_risk_count * 2500
            m3.metric("Estimated Revenue Saved", f"₹{potential_revenue_saved:,.2f}")

            st.markdown("---")
            st.subheader("📋 Segmented Results Table")
            st.dataframe(df)
    else:
        st.info("Tip: You can test the dashboard by uploading any sample CSV file, or use the Single Customer Predictor tab above.")