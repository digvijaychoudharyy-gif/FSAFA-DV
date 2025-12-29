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
        data = {}
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            data[sheet] = df
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

data = load_data()

# IMPROVED: Robust function to find metrics by looking at the FIRST column
def get_plot_data(df, metric_keyword):
    # 1. Identify the first column (where labels like 'Sales' or 'M Score' live)
    label_col = df.columns[0]
    
    # 2. Find the row where that first column contains our keyword
    mask = df[label_col].astype(str).str.contains(metric_keyword, case=False, na=False)
    row = df[mask]
    
    if row.empty:
        return None, None
    
    # 3. Identify year columns (usually everything except the first label column)
    # We filter out columns named 'Unnamed' which are common in Excel exports
    year_cols = [c for c in df.columns[1:] if "Unnamed" not in str(c)]
    
    # 4. Extract and clean values
    years = year_cols
    values = pd.to_numeric(row[year_cols].iloc[0], errors='coerce')
    
    return years, values

if data:
    company_sheets = list(data.keys())[:5]
    st.title("📊 Financial & Forensic Analysis Dashboard")

    # =========================================================
    # 1. FORENSIC SCORES (SEPARATE GRAPHS)
    # =========================================================
    st.header("🔍 Forensic Accounting Scores")
    
    score_cols = st.columns(3)
    scores_to_plot = ["M Score", "Z Score", "F Score"]

    for i, score_name in enumerate(scores_to_plot):
        with score_cols[i]:
            fig, ax = plt.subplots(figsize=(6, 4))
            for company in company_sheets:
                years, values = get_plot_data(data[company], score_name)
                if values is not None:
                    ax.plot(years, values, marker='o', label=company)
            
            ax.set_title(f"{score_name} Trend")
            ax.set_ylabel("Score Value")
            plt.xticks(rotation=45)
            ax.legend(prop={'size': 7})
            st.pyplot(fig)

    # =========================================================
    # 2. ACCRUALS ANALYSIS
    # =========================================================
    st.header("📉 Accruals Analysis")
    fig_acc, ax_acc = plt.subplots(figsize=(10, 4))
    for company in company_sheets:
        years, values = get_plot_data(data[company], "Accruals")
        if values is not None:
            ax_acc.plot(years, values, marker='s', label=company)
    
    ax_acc.set_title("Accruals Trend Comparison")
    plt.xticks(rotation=45)
    ax_acc.legend()
    st.pyplot(fig_acc)

    # =========================================================
    # 3. FINANCIAL PERFORMANCE
    # =========================================================
    st.header("📈 Financial Performance")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Trend")
        fig_rev, ax_rev = plt.subplots(figsize=(8, 5))
        for company in company_sheets:
            # Matches 'Sales' or 'Revenue'
            years, values = get_plot_data(data[company], "Sales")
            if values is not None:
                ax_rev.plot(years, values, marker='o', label=company)
        plt.xticks(rotation=45)
        ax_rev.legend()
        st.pyplot(fig_rev)

    with col2:
        st.subheader("Profit Trend")
        fig_prof, ax_prof = plt.subplots(figsize=(8, 5))
        for company in company_sheets:
            years, values = get_plot_data(data[company], "Net Profit")
            if values is not None:
                ax_prof.plot(years, values, marker='o', label=company)
        plt.xticks(rotation=45)
        ax_prof.legend()
        st.pyplot(fig_prof)

    st.header("📝 Analyst Interpretation")
    st.text_area("Findings:", height=200)

else:
    st.error("Please ensure 'FSAFA WAI Excel.xlsx' is in the app directory.")
