"""
check_table_data.py
Check how many rows are in each table.
"""
from config import get_connection

tables = ['Borrowers', 'Properties', 'Loans', 'LoanPayments', 
          'DrawRequests', 'LoanCovenants', 'MarketData', 'RiskScores']

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 50)
    print("TABLE ROW COUNTS")
    print("=" * 50)
    
    total_rows = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:20} {count:>10} rows")
        total_rows += count
    
    print("=" * 50)
    print(f"TOTAL ROWS: {total_rows}")
    print("=" * 50)
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")