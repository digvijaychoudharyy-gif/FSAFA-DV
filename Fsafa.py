import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

# Path to your file
FILE_PATH = "FSAFAWAIExcel.xlsx"

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        xls = pd.ExcelFile(FILE_PATH)
        data = {}
        # Loading all sheets found in the file
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            # Standardize the first column name to 'Metric' for search consistency
            df.columns.values[0] = "Metric"
            data[sheet] = df
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

data = load_data()

# Helper function to extract clean numeric data for plotting
def get_plot_data(df, metric_keyword):
    # Find row where metric name contains the keyword
    row = df[df["Metric"].astype(str).str.contains(metric_keyword, case=False, na=False)]
    if row.empty:
        return None, None
    
    # Extract years (columns 1 to 13 usually) and values
    # We filter out columns that are unnamed or contain 'Unnamed'
    cols = [c for c in df.columns[1:] if "Unnamed" not in str(c)]
    years = cols
    values = pd.to_numeric(row[cols].iloc[0], errors='coerce')
    
    return years, values

if data:
    company_sheets = list(data.keys())[:5] # Analyze top 5 companies
    
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
            plt.xticks(rotation=45) # Prevents year overlap
            ax.legend(prop={'size': 7})
            st.pyplot(fig)

    # =========================================================
    # 2. ACCRUALS ANALYSIS
    # =========================================================
    st.header("📉 Accruals Analysis")
    fig_acc, ax_acc = plt.subplots(figsize=(12, 5))
    for company in company_sheets:
        years, values = get_plot_data(data[company], "Accruals")
        if values is not None:
            ax_acc.plot(years, values, marker='s', linestyle='--', label=company)
    
    ax_acc.set_title("Accruals Trend Comparison (2014-2025)")
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

    # =========================================================
    # 4. INTERPRETATION
    # =========================================================
    st.header("📝 Analyst Interpretation")
    st.text_area(
        "Enter forensic findings and notes here:",
        placeholder="E.g., Maruti Suzuki shows high earnings quality with non-discretionary accruals...",
        height=200
    )

else:
    st.error("Please ensure 'FSAFA WAI Excel.xlsx' is uploaded to the same directory as the script.")
