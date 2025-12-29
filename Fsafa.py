import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Financial & Forensic Analysis Dashboard", layout="wide")

FILE_PATH = "FSAFAWAIExcel.xlsx"

companies = [
    "Maruti Suzuki",
    "Eicher Motors",
    "Mahindra & Mahindra",
    "Tata Motors",
    "Ashok Leyland"
]

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    data = {}
    for company in companies:
        data[company] = pd.read_excel(FILE_PATH, sheet_name=company)
    return data

data = load_data()

# ---------------- TITLE ----------------
st.title("📊 Financial & Forensic Analysis Dashboard")
st.markdown("**Data Source:** Uploaded Excel File (Static Analysis)")

# ============================================================
# SECTION 1 — FORENSIC ANALYSIS
# ============================================================
st.header("🔍 Forensic Accounting Analysis")

# ---- Accruals Line Chart ----
st.subheader("Accruals Trend (2014–2025)")

fig, ax = plt.subplots(figsize=(10,5))

for company in companies:
    df = data[company]
    accrual_row = df[df["Metric"].str.contains("Accrual", case=False, na=False)]
    if not accrual_row.empty:
        years = [col for col in df.columns if "Mar" in str(col)]
        values = accrual_row[years].values.flatten()
        ax.plot(years, values, marker="o", label=company)

ax.set_title("Accrual Trend Comparison")
ax.set_ylabel("Accrual Value")
ax.set_xlabel("Year")
ax.legend()
st.pyplot(fig)

# ---- M-Score, Z-Score, F-Score ----
st.subheader("Forensic Scores Comparison")

fig2, ax2 = plt.subplots(figsize=(10,5))

for company in companies:
    df = data[company]
    score_row = df[df["Metric"].isin(["M Score", "Z Score", "F Score"])]
    if not score_row.empty:
        scores = score_row.set_index("Metric").mean(axis=1)
        ax2.plot(scores.index, scores.values, marker="o", label=company)

ax2.set_title("M-Score, Z-Score & F-Score Comparison")
ax2.set_ylabel("Score Value")
ax2.legend()
st.pyplot(fig2)

# ============================================================
# SECTION 2 — FINANCIAL ANALYSIS
# ============================================================
st.header("📈 Financial Performance Analysis")

# ---- Revenue Trend ----
st.subheader("Revenue Trend (All Companies)")

fig3, ax3 = plt.subplots(figsize=(10,5))

for company in companies:
    df = data[company]
    rev = df[df["Metric"].str.contains("Sales", case=False)]
    if not rev.empty:
        years = [col for col in df.columns if "Mar" in str(col)]
        ax3.plot(years, rev[years].values.flatten(), marker="o", label=company)

ax3.set_title("Revenue Comparison")
ax3.set_ylabel("Revenue")
ax3.legend()
st.pyplot(fig3)

# ---- Profit Trend ----
st.subheader("Profit Trend")

fig4, ax4 = plt.subplots(figsize=(10,5))

for company in companies:
    df = data[company]
    profit = df[df["Metric"].str.contains("Profit", case=False)]
    if not profit.empty:
        years = [col for col in df.columns if "Mar" in str(col)]
        ax4.plot(years, profit[years].values.flatten(), marker="o", label=company)

ax4.set_title("Profit Comparison")
ax4.set_ylabel("Profit")
ax4.legend()
st.pyplot(fig4)

# ============================================================
# SECTION 3 — USER INTERPRETATION SPACE
# ============================================================
st.header("📝 Analyst Interpretation & Observations")

st.text_area(
    "Write your analysis, insights, red flags, and conclusions here:",
    height=200
)
