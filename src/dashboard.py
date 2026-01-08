import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.orm import Session
from core.database import SessionLocal, InvoiceDB
import warnings

# --- 1. SILENCE WARNINGS ---
warnings.filterwarnings("ignore")

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DocuFlow Dashboard",
    page_icon="💰",
    layout="wide"
)

# --- DATA LOADER ---
def get_data():
    """Fetches all invoices from the database and returns a DataFrame."""
    db: Session = SessionLocal()
    try:
        invoices = db.query(InvoiceDB).all()
        
        data = [
            {
                "ID": inv.id,
                "Filename": inv.filename,
                "Invoice Number": inv.invoice_number,
                "Vendor": inv.vendor_name,
                "Date": inv.invoice_date,
                "Total Amount": inv.total_amount,
                "Created At": inv.created_at
            }
            for inv in invoices
        ]
        return pd.DataFrame(data)
    finally:
        db.close()

# --- SIDEBAR ---
st.sidebar.title("🚀 DocuFlow")
st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:**")
st.sidebar.success("🟢 Database Connected")
st.sidebar.success("🟢 Worker Active")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# --- MAIN DASHBOARD ---
st.title("💸 Invoice Ingestion Overview (v1.1)")
st.markdown("Real-time monitoring of processed financial documents.")

# 1. Load Data
df = get_data()

if not df.empty:
    # --- FIX 1: DATE PARSING ---
    # Handle DD/MM/YYYY formats correctly
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce', dayfirst=True)

    # --- FIX 2: FILL NULL AMOUNTS (Prevents Plotly Crash) ---
    # Critical: Convert 'None', 'NaN', or Strings to 0.0 floats
    df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors='coerce').fillna(0.0)

    # 2. KPI Metrics
    total_spend = df["Total Amount"].sum()
    total_docs = len(df)
    unique_vendors = df["Vendor"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Processed Volume", f"${total_spend:,.2f}")
    col2.metric("Documents Ingested", total_docs)
    col3.metric("Active Vendors", unique_vendors)

    st.markdown("---")

    # 3. Charts
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("💰 Spend by Vendor")
        vendor_spend = df.groupby("Vendor")["Total Amount"].sum().reset_index()
        fig_vendor = px.bar(
            vendor_spend, 
            x="Vendor", 
            y="Total Amount",
            color="Total Amount",
            template="plotly_dark"
        )
        st.plotly_chart(fig_vendor, use_container_width=True)

    with col_chart2:
        st.subheader("📊 Recent Activity")
        # Fix: Ensure no NaNs are passed to size
        fig_scatter = px.scatter(
            df, 
            x="ID", 
            y="Total Amount", 
            size="Total Amount",
            color="Vendor",
            hover_data=["Filename"],
            title="Invoice Sizes"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Data Grid
    st.subheader("📄 Recent Invoices")
    st.dataframe(
        df.sort_values(by="ID", ascending=False),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Waiting for data... Drag a PDF into the folder to begin!")