import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Page Setup
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# 2. File Loading with Error Handling
excel_file = "FSAFAWAIExcel.xlsx"

@st.cache_data
def load_data(file):
    try:
        return pd.ExcelFile(file)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None

xls = load_data(excel_file)

if xls:
    # Sidebar - Sheet Selection
    company = st.sidebar.selectbox("Select Company", xls.sheet_names)
    
    # Load sheet and clean
    df = pd.read_excel(xls, sheet_name=company)
    df = df.dropna(how="all").reset_index(drop=True)
    
    # Identify Header and Data
    # Assuming Column 0 is Metric Names, and Column 1+ are Years
    df.columns = [str(col).strip() for col in df.columns]
    metrics = df.iloc[:, 0].astype(str).str.strip()
    
    tab1, tab2 = st.tabs(["📈 Financials", "🧪 Forensic"])

    # --- TAB 1: FINANCIALS ---
    with tab1:
        st.subheader(f"Performance: {company}")
        selected = st.multiselect("Select Metrics", options=metrics.tolist(), default=metrics.tolist()[:2])
        
        for m in selected:
            # Extract row, skip the label column, and transpose for charting
            row = df[metrics == m].iloc[:, 1:].T
            row.columns = [m]
            row.index.name = "Year"
            st.line_chart(row)

    # --- TAB 2: FORENSIC ---
    with tab2:
        st.subheader("Forensic Indicators")
        
        # Search for any row containing 'Score' or 'Accrual'
        forensic_mask = metrics.str.contains("Score|Accrual", case=False, na=False)
        forensic_df = df[forensic_mask]

        if not forensic_df.empty:
            for _, row in forensic_df.iterrows():
                label = row.iloc[0]
                data_points = pd.to_numeric(row.iloc[1:], errors='coerce').dropna()
                
                if not data_points.empty:
                    st.write(f"**{label}**")
                    st.area_chart(data_points)
        else:
            st.info("No forensic metrics (Scores/Accruals) found.")
            
        # Display raw data for transparency
        with st.expander("View Raw Data Table"):
            st.dataframe(df)
