import streamlit as st
import pandas as pd
import plotly.express as px
from core.database import SessionLocal, InvoiceDB
from sqlalchemy.orm import Session

# --- CONFIGURATION ---
st.set_page_config(page_title="DocuFlow Dashboard", page_icon="💰", layout="wide")

# --- HELPER FUNCTIONS ---
def get_data():
    """Fetches all invoices from the database."""
    db: Session = SessionLocal()
    try:
        invoices = db.query(InvoiceDB).all()
        # Convert to a format Pandas understands (list of dicts)
        data = [
            {
                "ID": inv.id,
                "Date": inv.invoice_date,
                "Vendor": inv.vendor_name,
                "Total ($)": inv.total_amount,
                "Filename": inv.filename,
                "Created At": inv.created_at
            }
            for inv in invoices
        ]
        return pd.DataFrame(data)
    finally:
        db.close()

# --- SIDEBAR ---
st.sidebar.title("🚀 DocuFlow")
st.sidebar.markdown("Automated Invoice Processing Pipeline")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# --- MAIN DASHBOARD ---
st.title("💸 Financial Overview")

# 1. Fetch Data
df = get_data()

if not df.empty:
    # 2. KPI Metrics (Top Row)
    total_spend = df["Total ($)"].sum()
    total_invoices = len(df)
    unique_vendors = df["Vendor"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spending", f"${total_spend:,.2f}")
    col2.metric("Invoices Processed", total_invoices)
    col3.metric("Active Vendors", unique_vendors)

    # 3. Charts (Middle Row)
    st.markdown("### 📈 Spending Trends")
    
    # Clean up date column for charting
    # (Some dates might be None or messy strings, so we handle errors)
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    
    # Simple Bar Chart: Spend by Vendor
    fig_vendor = px.bar(
        df, x="Vendor", y="Total ($)", 
        title="Spending by Vendor", 
        color="Total ($)",
        template="plotly_dark"
    )
    st.plotly_chart(fig_vendor, use_container_width=True)

    # 4. Data Table (Bottom Row)
    st.markdown("### 📄 Recent Invoices")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No data found in the database. Drag some PDFs into the folder!")

# --- FOOTER ---
st.markdown("---")
st.caption("DocuFlow v1.0 | Built with Python, Celery, & Streamlit")