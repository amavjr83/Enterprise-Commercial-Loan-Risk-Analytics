"""
view_borrowers.py
View a sample of the borrower data.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 80)
    print("SAMPLE BORROWERS")
    print("=" * 80)
    
    cursor.execute("""
        SELECT TOP 10 
            BorrowerID,
            BorrowerName,
            EntityType,
            Industry,
            AnnualRevenue,
            TotalAssets,
            CreditScore,
            RiskTier
        FROM Borrowers
        ORDER BY NEWID()
    """)
    
    rows = cursor.fetchall()
    
    print(f"{'ID':<5} {'Borrower Name':<30} {'Industry':<20} {'Revenue':<15} {'Score':<8} {'Tier'}")
    print("-" * 80)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1][:29]:<30} {row[3][:19]:<20} ${row[4]:>12,} {row[6]:<8} {row[7]}")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")