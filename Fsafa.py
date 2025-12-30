import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Financial & Forensic Dashboard",
    layout="wide"
)

st.title("📊 Financial & Forensic Analysis Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data(file):
    xls = pd.ExcelFile(file)
    data = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return data

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is None:
    st.warning("Please upload the Excel file to continue.")
    st.stop()

data = load_data(uploaded_file)

# ---------------------------
# COMPANY SELECTION
# ---------------------------
company_list = data["Financials"]["Company"].unique()
company = st.selectbox("Select Company", company_list)

# Filter data
fin = data["Financials"][data["Financials"]["Company"] == company]
analysis = data["Financial_Analysis"][data["Financial_Analysis"]["Company"] == company]
forensic = data["Forensic"][data["Forensic"]["Company"] == company]

# ---------------------------
# SECTION A – FINANCIAL ANALYSIS
# ---------------------------
st.markdown("## 📈 Financial Statement Analysis")

col1, col2 = st.columns(2)

# ---- Company Snapshot ----
with col1:
    st.subheader("Company Snapshot")

    fig, ax = plt.subplots()
    ax.plot(fin["Year"], fin["Revenue"], label="Revenue")
    ax.plot(fin["Year"], fin["Profit"], label="Profit")
    ax.plot(fin["Year"], fin["CFO"], label="CFO")

    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)

# ---- DuPont Analysis ----
with col2:
    st.subheader("DuPont Analysis")
    dupont_cols = ["Year", "Net Profit Margin", "Asset Turnover", "Equity Multiplier", "ROE"]
    st.dataframe(analysis[dupont_cols])

# ---------------------------
# EFFICIENCY & LIQUIDITY
# ---------------------------
st.markdown("## ⚙️ Efficiency & Liquidity Analysis")

col3, col4 = st.columns(2)

# Efficiency Ratios
with col3:
    st.subheader("Efficiency Ratios")
    fig, ax = plt.subplots()
    ax.plot(analysis["Year"], analysis["DSO"], label="DSO")
    ax.plot(analysis["Year"], analysis["DPO"], label="DPO")
    ax.plot(analysis["Year"], analysis["DIO"], label="DIO")
    ax.plot(analysis["Year"], analysis["CCC"], label="CCC")
    ax.set_xlabel("Year")
    ax.legend()
    st.pyplot(fig)

# Liquidity Ratios
with col4:
    st.subheader("Liquidity Ratios")
    fig, ax = plt.subplots()
    ax.plot(analysis["Year"], analysis["WCR"], label="Working Capital Ratio")
    ax.plot(analysis["Year"], analysis["Cash Ratio"], label="Cash Ratio")
    ax.set_xlabel("Year")
    ax.legend()
    st.pyplot(fig)

# ---------------------------
# FORENSIC ANALYSIS
# ---------------------------
st.markdown("## 🔍 Forensic Accounting Analysis")

fig, ax = plt.subplots()
ax.bar(forensic["Year"], forensic["M_Score"], label="M-Score")
ax.bar(forensic["Year"], forensic["F_Score"], bottom=forensic["M_Score"], label="F-Score")
ax.bar(forensic["Year"], forensic["Z_Score"], bottom=forensic["M_Score"] + forensic["F_Score"], label="Z-Score")
ax.bar(forensic["Year"], forensic["Accruals"], label="Accruals", alpha=0.6)
ax.legend()
st.pyplot(fig)

# ---------------------------
# FINAL VERDICT
# ---------------------------
st.markdown("## 🧠 Final Forensic Verdict")

avg_m = forensic["M_Score"].mean()
avg_z = forensic["Z_Score"].mean()
avg_acc = forensic["Accruals"].mean()

verdict = ""
if avg_m > -2.22 and avg_z < 1.8:
    verdict = "High risk of earnings manipulation and financial distress."
elif avg_m < -2.22 and avg_z > 3:
    verdict = "Strong financial quality with low manipulation risk."
else:
    verdict = "Moderate financial health with mixed risk indicators."

st.success(f"**Overall Verdict:** {verdict}")
