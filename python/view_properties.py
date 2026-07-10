"""
view_properties.py
View a sample of the property data.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 100)
    print("SAMPLE PROPERTIES")
    print("=" * 100)
    
    cursor.execute("""
        SELECT TOP 10 
            PropertyID,
            PropertyName,
            PropertyType,
            City,
            State,
            MarketValue,
            OccupancyRate,
            NetOperatingIncome,
            YearBuilt
        FROM Properties
        ORDER BY MarketValue DESC
    """)
    
    rows = cursor.fetchall()
    
    print(f"{'ID':<5} {'Property Type':<18} {'City':<15} {'Market Value':<18} {'Occ%':<8} {'NOI':<15} {'Year'}")
    print("-" * 95)
    
    for row in rows:
        print(f"{row[0]:<5} {row[2][:17]:<18} {row[3][:14]:<15} ${row[5]:>15,}  {row[6]:>5.1%}  ${row[7]:>12,}  {row[8]}")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")