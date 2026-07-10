"""
data_summary.py
Summary of all data in the database.
"""
from config import get_connection

tables = ['Borrowers', 'Properties', 'Loans', 'LoanPayments', 
          'DrawRequests', 'LoanCovenants', 'MarketData', 'RiskScores']

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 60)
    print("DATABASE SUMMARY - CommercialLoanAnalytics")
    print("=" * 60)
    
    total_rows = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:20} {count:>10} rows")
        total_rows += count
    
    print("=" * 60)
    print(f"TOTAL ROWS: {total_rows:,}")
    print("=" * 60)
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")