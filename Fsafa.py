import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

FILE_PATH = "FSAFAWAIExcel.xlsx"

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        xls = pd.ExcelFile(FILE_PATH)
        data = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
        return data
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

data = load_data()

# FIXED: This function no longer uses df["Metric"]. It uses position-based indexing.
def get_plot_data(df, metric_keyword):
    if df.empty:
        return None, None
        
    # Get the name of the very first column (could be 'Metric', 'Year', or 'Company')
    first_col_name = df.columns[0]
    
    # Search for the keyword in that first column
    mask = df[first_col_name].astype(str).str.contains(metric_keyword, case=False, na=False)
    row = df[mask]
    
    if row.empty:
        return None, None
    
    # Identify valid data columns (skip the first label column and ignore 'Unnamed' columns)
    valid_cols = [c for c in df.columns[1:] if "Unnamed" not in str(c)]
    
    # Extract years and numeric values
    years = [str(c) for c in valid_cols] # Convert years to strings for consistent X-axis
    values = pd.to_numeric(row[valid_cols].iloc[0], errors='coerce')
    
    return years, values

if data:
    # We take the first 5 sheets as the companies
    company_sheets = list(data.keys())[:5]
    
    st.title("📊 Financial & Forensic Analysis Dashboard")

    # =========================================================
    # 1. FORENSIC SCORES (M, Z, F SEPARATED)
    # =========================================================
    st.header("🔍 Forensic Accounting Scores")
    
    score_tabs = st.tabs(["Beneish M-Score", "Altman Z-Score", "Piotroski F-Score"])
    scores_mapping = ["M Score", "Z Score", "F Score"]

    for i, tab in enumerate(score_tabs):
        with tab:
            fig, ax = plt.subplots(figsize=(12, 5))
            metric_to_find = scores_mapping[i]
            
            for company in company_sheets:
                years, values = get_plot_data(data[company], metric_to_find)
                if values is not None and not values.isna().all():
                    ax.plot(years, values, marker='o', label=company)
            
            ax.set_title(f"{metric_to_find} Trends Across Companies")
            ax.set_ylabel("Score")
            plt.xticks(rotation=45)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            st.pyplot(fig)

    # =========================================================
    # 2. ACCRUALS TREND
    # =========================================================
    st.header("📉 Accruals Analysis")
    fig_acc, ax_acc = plt.subplots(figsize=(12, 5))
    for company in company_sheets:
        years, values = get_plot_data(data[company], "Accruals")
        if values is not None:
            ax_acc.plot(years, values, marker='s', label=company)
    
    ax_acc.set_title("Total Accruals Comparison")
    plt.xticks(rotation=45)
    ax_acc.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig_acc)

    # =========================================================
    # 3. FINANCIAL PERFORMANCE (REVENUE & PROFIT)
    # =========================================================
    st.header("📈 Financial Performance")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue (Sales) Trend")
        fig_rev, ax_rev = plt.subplots(figsize=(8, 5))
        for company in company_sheets:
            years, values = get_plot_data(data[company], "Sales")
            if values is not None:
                ax_rev.plot(years, values, marker='o', label=company)
        plt.xticks(rotation=45)
        ax_rev.legend()
        st.pyplot(fig_rev)

    with col2:
        st.subheader("Net Profit Trend")
        fig_prof, ax_prof = plt.subplots(figsize=(8, 5))
        for company in company_sheets:
            years, values = get_plot_data(data[company], "Net Profit")
            if values is not None:
                ax_prof.plot(years, values, marker='o', label=company)
        plt.xticks(rotation=45)
        ax_prof.legend()
        st.pyplot(fig_prof)

    # =========================================================
    # 4. INTERPRETATION
    # =========================================================
    st.header("📝 Analyst Interpretation")
    st.text_area("Observations and Forensic Red Flags:", height=150)

else:
    st.warning("Excel file not found. Please ensure 'FSAFA WAI Excel.xlsx' is in the folder.")
