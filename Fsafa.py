import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# -----------------------------
# LOAD EXCEL FILE
# -----------------------------
@st.cache_data
def load_excel(file):
    return pd.ExcelFile(file)

excel_file = "FSAFA WAI Excel.xlsx"
xls = load_excel(excel_file)

# -----------------------------
# COMPANY SELECTION
# -----------------------------
company = st.sidebar.selectbox("Select Company", xls.sheet_names)
df = pd.read_excel(xls, sheet_name=company)

# -----------------------------
# CLEAN DATA
# -----------------------------
df = df.dropna(how="all")
df.columns = df.columns.astype(str)

# Separate metrics and years
metrics = df.iloc[:, 0]
data = df.iloc[:, 1:]

# Convert numeric where possible
data = data.apply(pd.to_numeric, errors="coerce")

# -----------------------------
# DASHBOARD LAYOUT
# -----------------------------
tab1, tab2 = st.tabs(["📈 Financial Analysis", "🧪 Forensic Analysis"])

# =====================================================
# FINANCIAL ANALYSIS
# =====================================================
with tab1:
    st.subheader(f"{company} – Financial Performance")

    selected_metrics = st.multiselect(
        "Select Financial Metrics",
        options=metrics.tolist(),
        default=metrics[:3].tolist()
    )

    for metric in selected_metrics:
        row = df[df.iloc[:, 0] == metric].iloc[:, 1:].T
        row.columns = [metric]
        st.line_chart(row)

# =====================================================
# FORENSIC ANALYSIS
# =====================================================
with tab2:
    st.subheader(f"{company} – Forensic Analysis")

    # --- Accruals ---
    st.markdown("### 📌 Accrual Analysis")

    accrual_row = df[df.iloc[:, 0].str.contains("Accrual", case=False, na=False)]

    if not accrual_row.empty:
        accrual_data = accrual_row.iloc[:, 1:].T
        accrual_data.columns = ["Accruals"]

        st.line_chart(accrual_data)

        st.markdown("**Positive Accrual Years Highlighted:**")
        positive_years = accrual_data[accrual_data["Accruals"] > 0]
        st.dataframe(positive_years)
    else:
        st.info("No accrual data found in this sheet.")

    # --- Scores Section ---
    st.markdown("### 📊 Forensic Scores")

    score_keywords = ["M-Score", "Z-Score", "F-Score"]
    score_rows = df[df.iloc[:, 0].str.contains('|'.join(score_keywords), case=False, na=False)]

    if not score_rows.empty:
        for _, row in score_rows.iterrows():
            score_name = row.iloc[0]
            score_values = row.iloc[1:].dropna()
            st.line_chart(score_values, height=250)
    else:
        st.info("No forensic score data available.")

    # -----------------------------
    # COMPANY NOTES / PARAGRAPHS
    # -----------------------------
    st.markdown("### 📝 Company Notes")

    text_rows = df[df.iloc[:, 1:].isna().all(axis=1)]
    if not text_rows.empty:
        for note in text_rows.iloc[:, 0]:
            st.write("•", note)
    else:
        st.info("No descriptive text available for this company.")
