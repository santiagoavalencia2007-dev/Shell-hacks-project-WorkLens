import streamlit as st
from risk_model import calculate_job_risk, list_jobs

st.set_page_config(page_title="WorkLens", page_icon="📊", layout="wide")

st.title("WorkLens")
st.caption("AI occupational applicability and job transformation risk.")

job_list = list_jobs()
job_title = st.selectbox("Select or search an occupation", job_list)

result = calculate_job_risk(job_title)

st.subheader(f"{result['job_title']} Analysis")

col1, col2 = st.columns(2)
col1.metric("Empirical AI Applicability", f"{result['overall_probability']:.1f}%")
col2.metric("Automation Risk Level", result["job_risk"])

st.markdown("### Strategic Recommendation")
st.info(result["recommendation"])

st.markdown("---")
st.caption("Workforce intelligence powered by Gemini and Microsoft Research Work Activity Data.")