"""
debug_loan.py
Debug loan generation issues.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 60)
    print("DEBUGGING LOAN GENERATION")
    print("=" * 60)
    
    # Check if we can read from Borrowers
    cursor.execute("SELECT COUNT(*) FROM Borrowers")
    borrower_count = cursor.fetchone()[0]
    print(f" Borrowers count: {borrower_count}")
    
    if borrower_count > 0:
        cursor.execute("SELECT TOP 1 BorrowerID, BorrowerName FROM Borrowers")
        borrower = cursor.fetchone()
        print(f"   Sample borrower: {borrower[0]} - {borrower[1]}")
    
    # Check if we can read from Properties
    cursor.execute("SELECT COUNT(*) FROM Properties")
    property_count = cursor.fetchone()[0]
    print(f" Properties count: {property_count}")
    
    if property_count > 0:
        cursor.execute("SELECT TOP 1 PropertyID, PropertyType, MarketValue FROM Properties")
        property = cursor.fetchone()
        print(f"   Sample property: {property[0]} - {property[1]} - ${property[2]:,}")
    
    # Check Loans table structure
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Loans'
        ORDER BY ORDINAL_POSITION
    """)
    
    print("\n Loans table columns:")
    for row in cursor.fetchall():
        print(f"   {row[0]:20} {row[1]:15} {row[2]}")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")