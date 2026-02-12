import streamlit as st
import requests

st.title("🛡 AegisURL - AI Threat Analyzer")

url_input = st.text_input("Enter suspicious URL:")

if st.button("Analyze"):
    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={"content": url_input}
    )

    result = response.json()

    st.subheader("Risk Score")
    st.write(result["risk_score"])

    st.subheader("Risk Level")
    st.write(result["risk_level"])

    st.subheader("Threats Detected")
    for threat in result["threats_detected"]:
        st.write("•", threat)

    st.subheader("Recommendation")
    st.write(result["recommendation"])
