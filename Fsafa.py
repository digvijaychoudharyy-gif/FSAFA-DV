import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial & Forensic Analysis", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data(file):
    return pd.read_excel(file, sheet_name=None)

uploaded_file = st.file_uploader("FSAFAWAIExcel.xlsx", type=["xlsx"])

if uploaded_file:
    sheets = load_data(uploaded_file)
    company = st.selectbox("Select Company", list(sheets.keys()))
    df = sheets[company]

    df.columns = df.columns.astype(str)

    # -----------------------------
    # FINANCIAL ANALYSIS
    # -----------------------------
    st.header("📈 Financial Analysis")

    financial_metrics = ["Revenue", "Net Profit", "EBITDA", "ROE", "ROA"]

    available_metrics = [m for m in financial_metrics if m in df.iloc[:, 0].values]

    selected_metrics = st.multiselect(
        "Select Financial Metrics",
        available_metrics,
        default=available_metrics[:2]
    )

    for metric in selected_metrics:
        data = df[df.iloc[:, 0] == metric].iloc[:, 1:].T
        data.columns = [metric]
        st.line_chart(data)

    # -----------------------------
    # FORENSIC ANALYSIS
    # -----------------------------
    st.header("🧪 Forensic Analysis")

    score_map = {
        "M-Score": "Beneish M-Score",
        "Z-Score": "Altman Z-Score",
        "F-Score": "Piotroski F-Score"
    }

    score_results = {}

    for key, label in score_map.items():
        row = df[df.iloc[:, 0].str.contains(key, case=False, na=False)]
        if not row.empty:
            values = row.iloc[:, 1:].T
            values.columns = [label]
            st.subheader(label)
            st.line_chart(values)
            score_results[label] = values.iloc[-1, 0]

    # -----------------------------
    # FORENSIC INTERPRETATION
    # -----------------------------
    st.subheader("🧠 Forensic Interpretation")

    verdicts = []

    if "Beneish M-Score" in score_results:
        if score_results["Beneish M-Score"] > -2.22:
            verdicts.append("⚠️ High probability of earnings manipulation (M-Score)")
        else:
            verdicts.append("✅ Low manipulation risk (M-Score)")

    if "Altman Z-Score" in score_results:
        if score_results["Altman Z-Score"] < 1.8:
            verdicts.append("❌ Financial distress risk (Z-Score)")
        elif score_results["Altman Z-Score"] > 3:
            verdicts.append("✅ Financially strong company")
        else:
            verdicts.append("⚠️ Grey zone financial health")

    if "Piotroski F-Score" in score_results:
        if score_results["Piotroski F-Score"] >= 7:
            verdicts.append("✅ Strong fundamentals (F-Score)")
        else:
            verdicts.append("⚠️ Weak financial quality (F-Score)")

    for v in verdicts:
        st.write("•", v)

    # -----------------------------
    # FINAL DECISION
    # -----------------------------
    st.subheader("📌 Overall Company Assessment")

    if verdicts.count("✅") >= 2:
        st.success("Overall: FINANCIALLY STRONG COMPANY")
    elif verdicts.count("⚠️") >= 2:
        st.warning("Overall: MODERATE RISK COMPANY")
    else:
        st.error("Overall: HIGH RISK / WEAK FUNDAMENTALS")
