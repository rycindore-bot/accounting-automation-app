import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Professional Accountant Suite", layout="wide")

# App Header
st.title("💼 Senior Accountant & GST Practitioner Dashboard")
st.markdown("---")

# 1. SETUP GOOGLE SHEETS CONNECTIONS (Change the URLs with your actual Google Sheet CSV export links)
# Tip: Google Sheet ke URL ke last me '/edit#gid=0' ko hata kar '/export?format=csv&gid=XXXXX' lagaya jata hai.
CASHFLOW_SHEET_URL = "https://google.com"

# 2. SESSION STATE FOR DATA STORAGE (If cloud is not connected yet, it keeps data temporary)
if 'cashflow_db' not in st.session_state:
    try:
        # Puraani entries load karein agar sheets linked hai
        st.session_state.cashflow_db = pd.read_csv(CASHFLOW_SHEET_URL)
    except:
        # Default backup dataframe structure
        st.session_state.cashflow_db = pd.DataFrame([
            {"Date": "2026-10-28", "Particulars": "ABC Pvt Ltd - GST Fees", "Type": "Cash Inflow", "Amount": 15000.0},
            {"Date": "2026-10-29", "Particulars": "Vendor XYZ Advance", "Type": "Cash Outflow", "Amount": 4500.0}
        ])

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio("Navigation Control Panel", ["Executive Dashboard", "Data Entry Console", "Statutory GST & Tax Matrix"])

# --- MODULE 1: DATA ENTRY CONSOLE (Real Data Add Karne Ke Liye) ---
if menu == "Data Entry Console":
    st.header("➕ Add New Transaction / Record Entries")
    
    # Form layout to add a row cleanly
    with st.form(key="transaction_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date_input = st.date_input("Select Transaction Date", datetime.date.today())
            particulars_input = st.text_input("Entity Name / Narration / Particulars", placeholder="e.g., Reliance Ltd Audit Fee")
            
        with col2:
            type_input = st.selectbox("Transaction Flow Type", ["Cash Inflow", "Cash Outflow", "GST Liability Accrual", "TDS Deducted"])
            amount_input = st.number_input("Transaction Value (₹)", min_value=0.0, value=0.0, step=100.0)
            
        submit_btn = st.form_submit_button(label="🚀 Save Record to Database")
        
    # Logic to add data row into UI dynamically
    if submit_btn:
        if particulars_input == "":
            st.error("Particulars field can't be empty!")
        else:
            new_record = {
                "Date": str(date_input),
                "Particulars": particulars_input,
                "Type": type_input,
                "Amount": amount_input
            }
            # Append new record in Session State
            st.session_state.cashflow_db = pd.concat([st.session_state.cashflow_db, pd.DataFrame([new_record])], ignore_index=True)
            st.success(f"Successfully Added entry for '{particulars_input}'!")

    # Dynamic Data Grid & Data Editor Component
    st.subheader("📝 Live Ledger Database View (Editable)")
    st.markdown("Aap neeche di gayi table par double click karke live value edit bhi kar sakte hain:")
    
    # st.data_editor se aap direct user table me click karke edit kar sakte hain
    edited_df = st.data_editor(st.session_state.cashflow_db, use_container_width=True, num_rows="dynamic")
    st.session_state.cashflow_db = edited_df

    # Export Button to Download data immediately as local Excel/CSV
    csv_data = st.session_state.cashflow_db.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Updated Ledger as CSV", data=csv_data, file_name="Live_Account_Ledger.csv", mime="text/csv")

# --- MODULE 2: EXECUTIVE DASHBOARD ---
elif menu == "Executive Dashboard":
    st.header("📊 Real-Time Financial Overview")
    
    # Calculate live KPIs from current data state
    df = st.session_state.cashflow_db
    total_inflow = df[df['Type'] == 'Cash Inflow']['Amount'].sum()
    total_outflow = df[df['Type'] == 'Cash Outflow']['Amount'].sum()
    net_liquid_cash = total_inflow - total_outflow
    
    # Display Scorecards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Inflow (₹)", f"₹{total_inflow:,.2f}")
    kpi2.metric("Total Outflow (₹)", f"₹{total_outflow:,.2f}")
    kpi3.metric("Net Available Liquid Cash (₹)", f"₹{net_liquid_cash:,.2f}", delta=f"₹{net_liquid_cash}")
    
    st.subheader("Recent Activity Log")
    st.dataframe(df.tail(5), use_container_width=True)

# --- MODULE 3: COMPLIANCE ---
else:
    st.header("📑 GST & Statutory Tracker")
    st.info("Is component me aap firms ke GSTR-1 aur 3B status track kar sakte hain.")
    # Standard static framework display
    st.write("Current Pending Status:")
    st.table(pd.DataFrame([
        {"Company Name": "Client A Pvt Ltd", "GSTIN": "27AAAAA0000A1Z5", "GSTR-1 Status": "Filed", "GSTR-3B Status": "Pending"},
        {"Company Name": "Client B & Co", "GSTIN": "27BBBBB1111B2Z6", "GSTR-1 Status": "Pending", "GSTR-3B Status": "Pending"}
    ]))
