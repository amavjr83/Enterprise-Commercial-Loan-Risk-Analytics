"""
generate_loans_simple.py - Fixed decimal conversion
"""
import random
from datetime import datetime, timedelta
from config import get_connection

def main():
    print("Starting loan generation...")
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get data
    cursor.execute("SELECT BorrowerID FROM Borrowers")
    borrowers = [row[0] for row in cursor.fetchall()]
    print(f"Found {len(borrowers)} borrowers")
    
    cursor.execute("SELECT PropertyID, MarketValue FROM Properties")
    properties = cursor.fetchall()
    print(f"Found {len(properties)} properties")
    
    if not borrowers or not properties:
        print("ERROR: Missing required data!")
        conn.close()
        return
    
    inserted = 0
    for i in range(600):
        borrower = random.choice(borrowers)
        prop_id, prop_value = random.choice(properties)
        
        # Convert decimal to float for calculation
        prop_value_float = float(prop_value)
        
        loan_amount = round(prop_value_float * random.uniform(0.5, 0.8) / 1000) * 1000
        rate = round(random.uniform(0.04, 0.10), 3)
        term = random.choice([60, 120, 180, 240, 300, 360])
        
        start = datetime.now() - timedelta(days=random.randint(0, 1095))
        start = start.date()
        maturity = start + timedelta(days=term * 30)
        
        cursor.execute("""
            INSERT INTO Loans (BorrowerID, PropertyID, LoanAmount, InterestRate, LoanTermMonths,
                              StartDate, MaturityDate, LoanType, LoanStatus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (borrower, prop_id, loan_amount, rate, term,
              start, maturity, 
              random.choice(['Term Loan', 'Construction', 'Bridge', 'SBA 504', 'SBA 7(a)']),
              random.choices(['Active', 'Active', 'Active', 'Closed', 'Default'], 
                           weights=[0.65, 0.15, 0.10, 0.06, 0.04])[0]))
        
        inserted += 1
        if inserted % 50 == 0:
            conn.commit()
            print(f"  Inserted {inserted} loans...")
    
    conn.commit()
    conn.close()
    print(f" Inserted {inserted} loans!")

if __name__ == "__main__":
    main()