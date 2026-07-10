"""
config.py
Central configuration file for the Enterprise Commercial Loan Risk Analytics project.
Stores:
- SQL Server connection settings
- Database name
- ODBC Driver
"""
import pyodbc

# -------------------------------------------------------
# SQL SERVER CONFIGURATION
# -------------------------------------------------------
SERVER = r"DESKTOP-K41C8P6\SQLEXPRESS"
DATABASE = "CommercialLoanAnalytics"
DRIVER = "ODBC Driver 17 for SQL Server"  # We'll confirm this

# -------------------------------------------------------
# CONNECTION STRING
# -------------------------------------------------------
CONNECTION_STRING = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

# -------------------------------------------------------
# DATABASE CONNECTION FUNCTION
# -------------------------------------------------------
def get_connection():
    """
    Returns an active SQL Server connection.
    """
    return pyodbc.connect(CONNECTION_STRING)