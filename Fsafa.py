import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

FILE_PATH = "FSAFAWAIExcel.xlsx"

# ---------------- LOAD EXCEL ----------------
@st.cache_data
def load_excel():
    xls = pd.ExcelFile(FILE_PATH)
    data = {}
    for sheet in xls.sheet_names:
        data[sheet] = pd.read_excel(xls, sheet_name=sheet)
    return data

data = load_excel()
company_sheets = list(data.keys())[:5]   # first 5 sheets = companies

# ---------------- TITLE ----------------
st.title("📊 Financial & Forensic Analysis Dashboard")

# =========================================================
# FORENSIC ANALYSIS
# =========================================================
st.header("🔍 Forensic Accounting Analysis")

# ---------- ACCRUALS GRAPH ----------
st.subheader("Accruals Trend (2014–2025)")

fig1, ax1 = plt.subplots(figsize=(10,5))

for company in company_sheets:
    df = data[company]

    metric_col = df.columns[0]           # first column = metric names
    year_cols = df.columns[1:]            # remaining columns = years

    accrual_row = df[df[metric_col].astype(str).str.contains("accrual", case=False, na=False)]

    if not accrual_row.empty:
        # Convert values to numeric, forcing errors to NaN to prevent the plot crash
        y_values = pd.to_numeric(accrual_row.iloc[0, 1:], errors='coerce')
        ax1.plot(year_cols, y_values, marker='o', label=company)

ax1.set_title("Accrual Trend Comparison")
ax1.set_xlabel("Year")
ax1.set_ylabel("Accrual Value")
ax1.legend()
st.pyplot(fig1)

# ---------- FORENSIC SCORES ----------
st.subheader("M-Score, Z-Score & F-Score Comparison")

fig2, ax2 = plt.subplots(figsize=(10,5))

for company in company_sheets:
    df = data[company]
    metric_col = df.columns[0]

    scores = df[df[metric_col].astype(str).isin(["M Score", "Z Score", "F Score"])]

    if not scores.empty:
        for _, row in scores.iterrows():
            # Convert values to numeric to avoid matplotlib float conversion error
            y_values = pd.to_numeric(row[1:], errors='coerce')
            ax2.plot(df.columns[1:], y_values, marker='o', label=f"{company} - {row[metric_col]}")

ax2.set_title("Forensic Scores")
ax2.set_ylabel("Score Value")
ax2.legend()
st.pyplot(fig2)

# =========================================================
# FINANCIAL ANALYSIS
# =========================================================
st.header("📈 Financial Performance")

# ---------- REVENUE ----------
st.subheader("Revenue Trend")

fig3, ax3 = plt.subplots(figsize=(10,5))

for company in company_sheets:
    df = data[company]
    metric_col = df.columns[0]

    revenue = df[df[metric_col].astype(str).str.contains("revenue|sales", case=False, na=False)]

    if not revenue.empty:
        y_values = pd.to_numeric(revenue.iloc[0, 1:], errors='coerce')
        ax3.plot(df.columns[1:], y_values, marker='o', label=company)

ax3.set_title("Revenue Comparison")
ax3.set_ylabel("Revenue")
ax3.legend()
st.pyplot(fig3)

# ---------- PROFIT ----------
st.subheader("Profit Trend")

fig4, ax4 = plt.subplots(figsize=(10,5))

for company in company_sheets:
    df = data[company]
    metric_col = df.columns[0]

    profit = df[df[metric_col].astype(str).str.contains("profit", case=False, na=False)]

    if not profit.empty:
        y_values = pd.to_numeric(profit.iloc[0, 1:], errors='coerce')
        ax4.plot(df.columns[1:], y_values, marker='o', label=company)

ax4.set_title("Profit Comparison")
ax4.set_ylabel("Profit")
ax4.legend()
st.pyplot(fig4)

# =========================================================
# INTERPRETATION SECTION
# =========================================================
st.header("📝 Analyst Interpretation")
st.text_area(
    "Write your forensic and financial interpretation here:",
    height=200
)
