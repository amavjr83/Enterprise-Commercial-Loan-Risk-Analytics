"""
delinquency_analysis.py
Analyzes loan payment delinquency patterns.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 70)
    print("DELINQUENCY ANALYSIS")
    print("=" * 70)
    
    # Payment delinquency summary
    cursor.execute("""
        SELECT 
            CASE 
                WHEN DaysLate = 0 THEN 'On Time'
                WHEN DaysLate BETWEEN 1 AND 30 THEN '1-30 Days Late'
                WHEN DaysLate BETWEEN 31 AND 60 THEN '31-60 Days Late'
                WHEN DaysLate > 60 THEN '60+ Days Late'
            END as DelinquencyStatus,
            COUNT(*) as PaymentCount,
            AVG(TotalPaid) as AvgPayment
        FROM LoanPayments
        GROUP BY 
            CASE 
                WHEN DaysLate = 0 THEN 'On Time'
                WHEN DaysLate BETWEEN 1 AND 30 THEN '1-30 Days Late'
                WHEN DaysLate BETWEEN 31 AND 60 THEN '31-60 Days Late'
                WHEN DaysLate > 60 THEN '60+ Days Late'
            END
        ORDER BY 
            MIN(DaysLate)
    """)
    
    print(f"{'Status':20} {'Payments':>12} {'Avg Payment':>15}")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"{row[0]:20} {row[1]:>12,}  ${row[2]:>13,.2f}")
    
    print("\n" + "=" * 70)
    print("LOANS WITH DELINQUENT PAYMENTS")
    print("=" * 70)
    
    cursor.execute("""
        SELECT TOP 10
            l.LoanID,
            b.BorrowerName,
            COUNT(*) as LatePayments,
            AVG(CAST(lp.DaysLate AS FLOAT)) as AvgDaysLate
        FROM LoanPayments lp
        JOIN Loans l ON lp.LoanID = l.LoanID
        JOIN Borrowers b ON l.BorrowerID = b.BorrowerID
        WHERE lp.DaysLate > 0
        GROUP BY l.LoanID, b.BorrowerName
        HAVING COUNT(*) > 3
        ORDER BY LatePayments DESC
    """)
    
    rows = cursor.fetchall()
    if rows:
        print(f"{'Loan ID':<10} {'Borrower':<30} {'Late Payments':>15} {'Avg Days Late':>15}")
        print("-" * 70)
        for row in rows:
            print(f"{row[0]:<10} {row[1][:29]:<30} {row[2]:>15} {row[3]:>15.1f}")
    else:
        print("No delinquent payments found!")
    
    print("\n" + "=" * 70)
    print("DELINQUENCY RATE BY LOAN TYPE")
    print("=" * 70)
    
    cursor.execute("""
        SELECT 
            l.LoanType,
            COUNT(DISTINCT l.LoanID) as TotalLoans,
            COUNT(DISTINCT CASE WHEN lp.DaysLate > 0 THEN l.LoanID END) as DelinquentLoans,
            CAST(COUNT(DISTINCT CASE WHEN lp.DaysLate > 0 THEN l.LoanID END) AS FLOAT) / 
                COUNT(DISTINCT l.LoanID) * 100 as DelinquencyRate
        FROM Loans l
        JOIN LoanPayments lp ON l.LoanID = lp.LoanID
        GROUP BY l.LoanType
        ORDER BY DelinquencyRate DESC
    """)
    
    print(f"{'Loan Type':<20} {'Total Loans':>12} {'Delinquent':>12} {'Rate':>10}")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"{row[0][:19]:<20} {row[1]:>12} {row[2]:>12} {row[3]:>9.1f}%")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")