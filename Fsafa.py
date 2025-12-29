import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# -----------------------------
# DATA LOADING (FIXED CACHING)
# -----------------------------
excel_file = "FSAFAWAIExcel.xlsx"

@st.cache_data
def get_company_list(file):
    # Just gets the sheet names
    return pd.ExcelFile(file).sheet_names

@st.cache_data
def load_company_data(file, sheet):
    # Returns a DataFrame (which is serializable)
    return pd.read_excel(file, sheet_name=sheet)

try:
    # Get names for the sidebar
    company_list = get_company_list(excel_file)
    company = st.sidebar.selectbox("Select Company", company_list)

    # Load the specific sheet
    df = load_company_data(excel_file, company)

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    df = df.dropna(how="all")
    df.columns = df.columns.astype(str)
    
    # Separate labels and values
    metrics = df.iloc[:, 0].astype(str)
    
    # -----------------------------
    # DASHBOARD LAYOUT
    # -----------------------------
    tab1, tab2 = st.tabs(["📈 Financial Analysis", "🧪 Forensic Analysis"])

    # FINANCIAL ANALYSIS
    with tab1:
        st.subheader(f"{company} – Financial Performance")
        selected_metrics = st.multiselect(
            "Select Financial Metrics",
            options=metrics.tolist(),
            default=metrics.tolist()[:3] if len(metrics) > 3 else metrics.tolist()
        )

        for m in selected_metrics:
            row_data = df[metrics == m].iloc[:, 1:].T
            row_data.columns = [m]
            st.line_chart(row_data)

    # FORENSIC ANALYSIS
    with tab2:
        st.subheader(f"{company} – Forensic Analysis")

        # Accruals
        accrual_mask = metrics.str.contains("Accrual", case=False, na=False)
        if accrual_mask.any():
            st.markdown("### 📌 Accrual Analysis")
            accrual_data = df[accrual_mask].iloc[:, 1:].T
            accrual_data.columns = ["Accruals"]
            st.line_chart(accrual_data)
        else:
            st.info("No accrual data found.")

        # Forensic Scores
        score_keywords = ["M-Score", "Z-Score", "F-Score"]
        score_mask = metrics.str.contains('|'.join(score_keywords), case=False, na=False)
        score_df = df[score_mask]

        if not score_df.empty:
            st.markdown("### 📊 Forensic Scores")
            for _, row in score_df.iterrows():
                st.write(f"**{row.iloc[0]}**")
                st.area_chart(row.iloc[1:].dropna())

except FileNotFoundError:
    st.error(f"Could not find '{excel_file}'. Please check the filename on GitHub.")
except Exception as e:
    st.error(f"Error: {e}")
