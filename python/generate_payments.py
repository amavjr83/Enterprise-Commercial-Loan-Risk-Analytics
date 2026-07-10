"""
generate_payments.py
Generates loan payment schedules for all active loans.
"""
import random
from datetime import datetime, timedelta
from config import get_connection

def generate_payments():
    """Generate payment schedules for loans"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all active loans
    cursor.execute("""
        SELECT LoanID, LoanAmount, InterestRate, LoanTermMonths, StartDate
        FROM Loans
        WHERE LoanStatus = 'Active'
    """)
    
    loans = cursor.fetchall()
    print(f"Found {len(loans)} active loans")
    
    if not loans:
        print("No active loans found!")
        conn.close()
        return
    
    payments_inserted = 0
    batch_size = 200
    
    for loan in loans:
        loan_id, loan_amount, interest_rate, term_months, start_date = loan
        loan_amount_float = float(loan_amount)
        monthly_rate = float(interest_rate) / 12
        
        # Calculate monthly payment using amortization formula
        if monthly_rate > 0:
            payment = loan_amount_float * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
        else:
            payment = loan_amount_float / term_months
        
        # Generate payment schedule
        remaining_balance = loan_amount_float
        payment_date = start_date
        
        for month in range(1, term_months + 1):
            # Calculate interest and principal
            interest_paid = remaining_balance * monthly_rate
            principal_paid = payment - interest_paid
            
            # Ensure principal doesn't exceed balance
            if principal_paid > remaining_balance:
                principal_paid = remaining_balance
                payment = remaining_balance + interest_paid
            
            remaining_balance -= principal_paid
            
            # Add month to payment date
            payment_date = start_date + timedelta(days=30 * month)
            
            # Random late payment (10% chance)
            days_late = random.choices([0, 0, 0, 0, 0, 0, 0, 0, 30, 60], weights=[0.9, 0.03, 0.02, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005])[0]
            
            # Insert payment - NO TotalPaid column (it's computed)
            cursor.execute("""
                INSERT INTO LoanPayments (
                    LoanID, PaymentDate, PrincipalPaid, InterestPaid, DaysLate
                ) VALUES (?, ?, ?, ?, ?)
            """, (loan_id, payment_date, round(principal_paid, 2), 
                  round(interest_paid, 2), days_late))
            
            payments_inserted += 1
            
            if payments_inserted % batch_size == 0:
                conn.commit()
                print(f"  Inserted {payments_inserted} payments...")
            
            # Stop if balance is paid off
            if remaining_balance <= 0:
                break
    
    conn.commit()
    conn.close()
    print(f" Inserted {payments_inserted} loan payments!")

if __name__ == "__main__":
    print("=" * 60)
    print("LOAN PAYMENT GENERATION")
    print("=" * 60)
    generate_payments()
    print("\n Payment generation complete!")