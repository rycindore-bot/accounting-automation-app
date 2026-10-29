import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration (Must be at the very top)
st.set_page_config(page_title="Professional Accountant Suite", layout="wide")

# 2. Crash-Proof Data Initialization (Session State Setup)
# Explicit columns to avoid any KeyError when switching tabs
DEFAULT_COLUMNS = ["Date", "Particulars", "Type", "Amount"]

if 'cashflow_db' not in st.session_state:
    # Creating structured starting data safely
    initial_data = [
        {"Date": "2026-10-28", "Particulars": "ABC Pvt Ltd - GST Fees", "Type": "Cash Inflow", "Amount": 15000.0},
        {"Date": "2026-10-29", "Particulars": "Vendor XYZ Advance", "Type": "Cash Outflow", "Amount": 4500.0}
    ]
    st.session_state.cashflow_db = pd.DataFrame(initial_data, columns=DEFAULT_COLUMNS)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📑 Navigation Control")
menu = st.sidebar.radio("Go To Module:", ["Executive Dashboard", "Data Entry Console", "Statutory GST & Tax Matrix"])

# --- MODULE 1: DATA ENTRY CONSOLE ---
if menu == "Data Entry Console":
    st.header("➕ Add New Transaction / Record Entries")
    
    # Clean data input form
    with st.form(key="transaction_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date_input = st.date_input("Select Transaction Date", datetime.date.today())
            particulars_input = st.text_input("Entity Name / Narration / Particulars", placeholder="e.g., Reliance Ltd Audit Fee")
            
        with col2:
            type_input = st.selectbox("Transaction Flow Type", ["Cash Inflow", "Cash Outflow", "GST Liability Accrual", "TDS Deducted"])
            amount_input = st.number_input("Transaction Value (₹)", min_value=0.0, value=0.0, step=100.0)
            
        submit_btn = st.form_submit_button(label="🚀 Save Record to Database")
        
    # Logic to securely append new rows without mutating columns
    if submit_btn:
        if not particulars_input.strip():
            st.error("Particulars field cannot be empty!")
        else:
            new_record = pd.DataFrame([{
                "Date": str(date_input),
                "Particulars": particulars_input.strip(),
                "Type": type_input,
                "Amount": float(amount_input)
            }])
            
            # Safe concat strategy
            st.session_state.cashflow_db = pd.concat([st.session_state.cashflow_db, new_record], ignore_index=True)
            st.success(f"Successfully Added entry for '{particulars_input}'!")

    st.markdown("---")
    st.subheader("📝 Live Ledger Database View (Editable Grid)")
    st.info("Aap neeche di gayi table ke cells par double-click karke values directly badal bhi sakte hain.")
    
    # Safe rendering of data editor with strict column enforcement
    current_df = pd.DataFrame(st.session_state.cashflow_db, columns=DEFAULT_COLUMNS)
    edited_df = st.data_editor(current_df, use_container_width=True, num_rows="dynamic", key="main_ledger_editor")
    
    # Sync safely back to session state
    if edited_df is not None:
        st.session_state.cashflow_db = edited_df.reset_index(drop=True)

    # Fast Backup Download Component
    try:
        csv_data = st.session_state.cashflow_db.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Updated Ledger as CSV", data=csv_data, file_name="Live_Account_Ledger.csv", mime="text/csv")
    except Exception as e:
        st.warning("Download option temporary buffering. Please refresh.")

# --- MODULE 2: EXECUTIVE DASHBOARD ---
elif menu == "Executive Dashboard":
    st.header("📊 Real-Time Financial Overview")
    
    # Fetching latest data snapshot safely
    df = pd.DataFrame(st.session_state.cashflow_db, columns=DEFAULT_COLUMNS)
    
    # Error safe aggregation
    try:
        total_inflow = float(df[df['Type'] == 'Cash Inflow']['Amount'].sum())
        total_outflow = float(df[df['Type'] == 'Cash Outflow']['Amount'].sum())
    except KeyError:
        total_inflow = 0.0
        total_outflow = 0.0
        
    net_liquid_cash = total_inflow - total_outflow
    
    # Interactive Visual KPI Summary Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Inflow (₹)", f"₹{total_inflow:,.2f}")
    kpi2.metric("Total Outflow (₹)", f"₹{total_outflow:,.2f}")
    kpi3.metric("Net Available Liquid Cash (₹)", f"₹{net_liquid_cash:,.2f}", delta=f"₹{net_liquid_cash:,.2f}")
    
    st.markdown("---")
    st.subheader("📋 Recent Transaction Stream")
    st.dataframe(df.tail(10), use_container_width=True)

# --- MODULE 3: STATUTORY GST & TAX MATRIX ---
else:
    st.header("📑 GST & Statutory Compliance Hub")
    st.markdown("Freelance Clients aur Pvt Ltd Firms ka compliance status monitor karein:")
    
    compliance_data = [
        {"Company Name": "Client A Pvt Ltd", "GSTIN": "27AAAAA0000A1Z5", "GSTR-1 Status": "Filed", "GSTR-3B Status": "Pending", "TDS Challan": "Paid"},
        {"Company Name": "Client B & Co", "GSTIN": "27BBBBB1111B2Z6", "GSTR-1 Status": "Pending", "GSTR-3B Status": "Pending", "TDS Challan": "Overdue"}
    ]
    
    st.table(pd.DataFrame(compliance_data))
