"""
view_table_schemas.py
View the structure of all tables in the database.
"""
from config import get_connection

tables = ['Borrowers', 'Properties', 'Loans', 'LoanPayments', 
          'DrawRequests', 'LoanCovenants', 'MarketData', 'RiskScores']

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    for table in tables:
        print(f"\n{'='*60}")
        print(f"Table: {table}")
        print('='*60)
        
        cursor.execute(f"""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            max_len = col[2] if col[2] else 'N/A'
            nullable = col[3]
            print(f"  {col_name:25} {data_type:15} {max_len:10} {nullable}")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")