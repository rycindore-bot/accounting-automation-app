import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinOps Automation - GST & Corporate Compliance Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APP BRANDING & HEADERS ---
st.title("💼 FinOps & Compliance Automation Studio")
st.markdown("##### *Designed for Senior Accountants, Freelance Practitioners & GST Experts*")
st.divider()

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("🛠️ Operations Core")
menu = st.sidebar.radio(
    "Go To Module:",
    [
        "📊 Executive Dashboard",
        "💵 Cash Flow & Bank Recon",
        "⚖️ Accounts Payable & Receivable",
        "📈 Sales & Credit Approvals",
        "📑 Statutory & GST Compliance",
        "💰 Payroll & Statutory Deduction Engine",
        "🔄 Inter-Party & Related Ledger Reconciliation"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 Tip: Download individual sheets as CSV inside each module for bank uploads or Tally XML ingestion.")

# --- SESSION STATE INITIALIZATION FOR PERSISTENCE (MOCK) ---
if 'sales_invoices' not in st.session_state:
    st.session_state.sales_invoices = pd.DataFrame([
        {"Invoice ID": "INV-2026-001", "Client Name": "Apex Alpha Pvt Ltd", "Amount (INR)": 450000, "GSTIN": "27AAAAA1111A1Z1", "Status": "Pending Review"},
        {"Invoice ID": "INV-2026-002", "Client Name": "Matrix Logistics", "Amount (INR)": 125000, "GSTIN": "24BBBBB2222B2Z2", "Status": "Pending Review"},
        {"Invoice ID": "INV-2026-003", "Client Name": "Zephyr Cloud Infotech", "Amount (INR)": 890000, "GSTIN": "07CCCCC3333C3Z3", "Status": "Approved"}
    ])

# ==========================================
# 1. EXECUTIVE DASHBOARD MODULE
# ==========================================
if menu == "📊 Executive Dashboard":
    st.subheader("📌 Day-to-Day Financial Snapshot")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net Liquid Cash", "₹ 24,50,000", "+₹ 3,20,000 (Today)")
    with col2:
        st.metric("Pending Approvals", "2 Invoices", "Urgent Action Required")
    with col3:
        st.metric("GST Submissions due (Oct)", "4 / 8 Entities", "Deadline: 11th & 20th")
    with col4:
        st.metric("Net Inter-Party Discrepancy", "₹ 42,500", "Action Required")
        
    st.divider()
    
    # Priority Checklist for Practitioner
    st.markdown("### 🗓️ Priority Checklist Today")
    todo_data = {
        "Client Entity": ["Apex Alpha Pvt Ltd", "Om SAI Manufacturing", "Vedic Trades & Firms", "Matrix Logistics"],
        "Task Details": ["Verify Bank Reconciliation Statement", "Compile GSTR-1 Sales Invoices", "Deposit Monthly TDS Challan (Sec 194C)", "Process Monthly Salary Payroll & PF Match"],
        "Deadline": ["Today 6:00 PM", "Tomorrow", "Within 3 Days", "5th of Next Month"],
        "Done": [False, False, True, False]
    }
    df_todo = pd.DataFrame(todo_data)
    st.data_editor(df_todo, use_container_width=True)

# ==========================================
# 2. CASH FLOW & BANK RECON MODULE
# ==========================================
elif menu == "💵 Cash Flow & Bank Recon":
    st.subheader("💵 Dynamic Cash Flow Verifier & Bank Reconciliation Statement (BRS)")
    
    tab1, tab2 = st.tabs(["Daily Cash Tracker", "Bank Statement Recon Engine"])
    
    with tab1:
        st.markdown("### Verify Daily Closing Balance Variance")
        c1, c2, c3 = st.columns(3)
        with c1:
            opening_bal = st.number_input("Opening Book Balance (INR)", value=1250000.0)
        with c2:
            total_receipts = st.number_input("Total Receipts Today (INR)", value=450000.0)
        with c3:
            total_payments = st.number_input("Total Payments Today (INR)", value=180000.0)
            
        calculated_closing = opening_bal + total_receipts - total_payments
        st.info(f"📐 Auto-Calculated Closing Balance as per Books: **₹ {calculated_closing:,.2f}**")
        
        actual_physical = st.number_input("Actual Balance as per Bank / Cash Box (INR)", value=1520000.0)
        variance = actual_physical - calculated_closing
        
        if variance == 0:
            st.success("🎯 Zero Variance! Books perfectly match with physical/bank balance.")
        else:
            st.error(f"⚠️ Variance Detected: **₹ {variance:,.2f}**. Verify unpresented cheques or uncredited receipts.")
            
    with tab2:
        st.markdown("### Process Unreconciled Statement Items")
        st.write("Upload clean bank ledger or directly clear items below:")
        
        recon_data = pd.DataFrame([
            {"Transaction Date": "2026-10-25", "Particulars": "Cheque Issued to Vendor A", "Type": "Debit", "Amount": 75000, "Cleared in Bank?": False},
            {"Transaction Date": "2026-10-26", "Particulars": "Direct Credit by Client Z", "Type": "Credit", "Amount": 142000, "Cleared in Bank?": True},
            {"Transaction Date": "2026-10-28", "Particulars": "Bank Charges Debited", "Type": "Debit", "Amount": 1500, "Cleared in Bank? :": False}
        ])
        
        edited_recon = st.data_editor(recon_data, use_container_width=True)
        st.button("Update BRS Ledger")

# ==========================================
# 3. ACCOUNTS PAYABLE & RECEIVABLE MODULE
# ==========================================
elif menu == "⚖️ Accounts Payable & Receivable":
    st.subheader("⚖️ Vendor Payables (AP) & Customer Receivables (AR) Aging Control")
    
    entity_filter = st.selectbox("Select Business Entity / Client:", ["All Entities", "Apex Alpha Pvt Ltd", "Matrix Logistics", "Vedic Trades & Firms"])
    
    col_ar, col_ap = st.columns(2)
    
    with col_ar:
        st.markdown("#### 🔵 Accounts Receivable (AR) Aging Matrix")
        ar_data = pd.DataFrame({
            "Customer Name": ["Globex Corp", "Beta Tech", "Delta Retailers"],
            "Total Outstanding": [320000, 150000, 45000],
            "0-30 Days": [320000, 100000, 0],
            "31-60 Days": [0, 50000, 20000],
            "60+ Days (High Risk)": [0, 0, 25000]
        })
        st.dataframe(ar_data, use_container_width=True)
        
    with col_ap:
        st.markdown("#### 🔴 Accounts Payable (AP) Due / MSME Trackers")
        ap_data = pd.DataFrame({
            "Vendor Name": ["Star Enterprise (MSME)", "Sigma Logistics", "Quantum Infrastructure"],
            "Total Payable": [180000, 95000, 600000],
            "Days Pending": [12, 42, 55],
            "Status": ["Safe (<45 Days)", "Review MSME rule", "Critical Overdue"]
        })
        st.dataframe(ap_data, use_container_width=True)

# ==========================================
# 4. SALES & CREDIT APPROVALS MODULE
# ==========================================
elif menu == "📈 Sales & Credit Approvals":
    st.subheader("📈 Commercial Sales & Credit Note Verification Desk")
    st.write("Review pending commercial sales invoices or high-value credits before financial dispatch.")
    
    # Fetch data from state
    df_sales = st.session_state.sales_invoices
    
    # Process updates directly via data editor
    updated_df = st.data_editor(
        df_sales,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Approval Actions",
                options=["Pending Review", "Approved", "Rejected / Send to Correction"],
                required=True,
            )
        },
        use_container_width=True,
        key="sales_editor"
    )
    
    if st.button("Commit Status Changes to System Ledger"):
        st.session_state.sales_invoices = updated_df
        st.success("✅ Commercial sales approvals updated successfully!")

# ==========================================
# 5. STATUTORY & GST COMPLIANCE MODULE
# ==========================================
elif menu == "📑 Statutory & GST Compliance":
    st.subheader("📑 Statutory Master Tracker & GST Return Compiler")
    st.write("Multi-firm workflow engine for filing dates, returns verification, and Challan generations.")
    
    compliance_data = pd.DataFrame([
        {"Entity Name": "Apex Alpha Pvt Ltd", "Structure": "Pvt Ltd", "GSTR-1 Status": "Filed", "GSTR-3B Status": "Pending ITC Recon", "TDS Challan 281": "Paid", "ROC Form MGT-7": "Draft Completed"},
        {"Entity Name": "Matrix Logistics", "Structure": "Partnership", "GSTR-1 Status": "Ready to Upload", "GSTR-3B Status": "Pending Outward Finalization", "TDS Challan 281": "Unpaid", "ROC Form MGT-7": "Not Applicable"},
        {"Entity Name": "Vedic Trades & Firms", "Structure": "Proprietorship", "GSTR-1 Status": "Filed", "GSTR-3B Status": "Filed", "TDS Challan 281": "Not Applicable", "ROC Form MGT-7": "Not Applicable"},
        {"Entity Name": "Om SAI Manufacturing", "Structure": "Pvt Ltd", "GSTR-1 Status": "Pending Invoices", "GSTR-3B Status": "Pending Review", "TDS Challan 281": "Paid", "ROC Form MGT-7": "Filed"}
    ])
    
    # Color highlight implementation via dynamic editor
    st.data_editor(compliance_data, use_container_width=True)
    
    st.markdown("### 🧮 Fast Tax & Interest Calculator for Delayed Filing")
    c_tax, c_days = st.columns(2)
    with c_tax:
        tax_due = st.number_input("Net Tax Liability Payable (INR)", value=50000.0)
    with c_days:
        days_delayed = st.number_input("Number of Days Delayed past due date", value=5, step=1)
        
    # GST / Tax delay calculations under standard Indian laws (e.g. 18% per annum)
    daily_rate = 0.18 / 365
    calculated_interest = tax_due * daily_rate * days_delayed
    st.warning(f"🕒 Calculated Interest Liability u/s 50 (at 18% p.a.): **₹ {calculated_interest:,.2f}**")

# ==========================================
# 6. PAYROLL & STATUTORY DEDUCTION ENGINE
# ==========================================
elif menu == "💰 Payroll & Statutory Deduction Engine":
    st.subheader("💰 Automated Structural Payroll & Monthly Salary Processing Machine")
    st.write("Input structural figures to eliminate manual Excel formulas. Auto calculates PF, PT, and Net Take Home.")
    
    # Default Employee Template
    emp_template = pd.DataFrame([
        {"Emp ID": "EMP01", "Employee Name": "Raman Sharma", "Basic Salary": 40000, "HRA": 15000, "Special Allowance": 10000, "LWP Days": 0},
        {"Emp ID": "EMP02", "Employee Name": "Priya Nair", "Basic Salary": 55000, "HRA": 20000, "Special Allowance": 12000, "LWP Days": 1},
        {"Emp ID": "EMP03", "Employee Name": "Amit Patel", "Basic Salary": 30000, "HRA": 12000, "Special Allowance": 5000, "LWP Days": 3}
    ])
    
    st.markdown("#### 📝 Edit Monthly Payroll Roster")
    edited_emp = st.data_editor(emp_template, use_container_width=True)
    
    # Computational Logic for Monthly Payroll Processing Loop
    processed_roster = []
    for _, row in edited_emp.iterrows():
        # Days assume standard 30-day corporate cycle
        payable_ratio = (30 - row["LWP Days"]) / 30
        
        gross_structural = row["Basic Salary"] + row["HRA"] + row["Special Allowance"]
        earned_gross = gross_structural * payable_ratio
        
        # Statutory Math (Indian Compliance Rules Example)
        # Provident Fund (PF) -> 12% of Basic or capped at Statutory ceiling standard matching rules
        pf_deduction = (row["Basic Salary"] * payable_ratio) * 0.12
        
        # Professional Tax (PT) Slab Estimation (Standard Slab average ₹200-250)
        pt_deduction = 200.0 if earned_gross > 20000 else 0.0
        
        net_salary = earned_gross - pf_deduction - pt_deduction
        
        processed_roster.append({
            "Emp ID": row["Emp ID"],
            "Employee Name": row["Employee Name"],
            "Earned Gross (INR)": round(earned_gross, 2),
            "EPF Contribution (12%)": round(pf_deduction, 2),
            "Professional Tax (PT)": pt_deduction,
            "Net Net Disbursement": round(net_salary, 2)
        })
        
    df_final_payroll = pd.DataFrame(processed_roster)
    
    st.markdown("#### 📊 Processed Sheet Output (Verified Net Bank Payout)")
    st.dataframe(df_final_payroll, use_container_width=True)
    
    # File download function for seamless workflow bank uploads
    csv = df_final_payroll.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Certified Bank Salary Disbursement CSV",
        data=csv,
        file_name=f"Verified_Payroll_Output_{datetime.date.today().strftime('%B_%Y')}.csv",
        mime='text/csv'
    )

# ==========================================
# 7. INTER-PARTY & RELATED PARTY LEDGER MODULE
# ==========================================
elif menu == "🔄 Inter-Party & Related Ledger Reconciliation":
    st.subheader("🔄 Inter-Party Mismatch & Related Party Transactions Cross-Verification Matrix")
    st.write("Reconcile debit/credit balances across holding, subsidiaries, or interrelated cross-firm entities.")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("##### 🏢 Entity Alpha Books (Receivable from Entity Beta)")
        alpha_books = pd.DataFrame({
            "Date": ["2026-10-01", "2026-10-10", "2026-10-22"],
            "Voucher Ref": ["JV-091", "INV-882", "REC-04"],
            "Debit (INR)": [500000, 120000, 0],
            "Credit (INR)": [0, 0, 300000],
        })
        st.dataframe(alpha_books, use_container_width=True)
        st.info("Closing Balance in Alpha Books: **₹ 3,20,000 (Dr)**")
        
    with col_e2:
        st.markdown("##### 🏢 Entity Beta Books (Payable to Entity Alpha)")
        beta_books = pd.DataFrame({
            "Date": ["2026-10-01", "2026-10-10", "2026-10-22"],
            "Voucher Ref": ["JV-091", "INV-882", "REC-04"],
            "Debit (INR)": [0, 0, 300000],
            "Credit (INR)": [500000, 95000, 0], # Note: 95000 instead of 120000 (Mismatch)
        })
        st.dataframe(beta_books, use_container_width=True)
        st.info("Closing Balance in Beta Books: **₹ 2,95,000 (Cr)**")
        
    st.divider()
    st.markdown("### 🔍 Discrepancy Reconciliation Analysis")
    mismatch_val = 320000 - 295000
    st.error(f"❌ Unreconciled Gap Found: **₹ {mismatch_val:,.2f}**")
    st.markdown(
        """
        *   **Identified Reason:** Invoice `INV-882` recorded as **₹ 1,20,000** in Entity Alpha, but booked as **₹ 95,000** in Entity Beta.
        *   **Action Plan:** Post correction journal entry in Entity Beta for **₹ 25,000** under short-provision adjustment.
        """
    )
