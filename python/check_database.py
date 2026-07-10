"""
check_database.py
Check the database and list all tables.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    
    tables = cursor.fetchall()
    
    print("=" * 50)
    print(f"Database: CommercialLoanAnalytics")
    print(f"Tables found: {len(tables)}")
    print("=" * 50)
    
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  (No tables found - ready for data generation!)")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")