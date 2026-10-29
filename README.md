
# AccountPro

Accounting, Payroll and Compliance Management using Python and Streamlit.

## Features
- Multi-client master
- Daily cash-flow entries
- Bank transaction verification records
- Sales approvals
- Accounts receivable and payable
- GST, TDS and statutory compliance tracking
- Manual payroll calculation and salary register
- Related-party ledger
- CSV/Excel import and CSV export
- PostgreSQL database

## Requirements
- Python 3.11 or newer
- PostgreSQL database
- Streamlit Community Cloud or local Streamlit installation

## Setup
1. Install dependencies:
   `pip install -r requirements.txt`
2. Configure `.streamlit/secrets.toml`.
3. Run:
   `streamlit run app.py`

## Security
Never commit database credentials, passwords, employee data or client files.
Use a private GitHub repository and a managed PostgreSQL database with backups.

## Important
This is a starter application, not a complete accounting or statutory filing system.
Test calculations and permissions before entering real financial data.
