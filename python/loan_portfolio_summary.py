"""
loan_portfolio_summary.py
Summary statistics for the loan portfolio.
"""
from config import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=" * 70)
    print("LOAN PORTFOLIO SUMMARY")
    print("=" * 70)
    
    # Total loan portfolio
    cursor.execute("""
        SELECT 
            COUNT(*) as TotalLoans,
            SUM(LoanAmount) as TotalPortfolio,
            AVG(LoanAmount) as AvgLoanSize,
            AVG(InterestRate) as AvgRate,
            AVG(LoanTermMonths) as AvgTerm
        FROM Loans
    """)
    
    row = cursor.fetchone()
    print(f"Total Loans:          {row[0]:,}")
    print(f"Total Portfolio:      ${row[1]:,.2f}")
    print(f"Average Loan Size:    ${row[2]:,.2f}")
    print(f"Average Interest Rate: {row[3]:.2%}")
    print(f"Average Loan Term:    {row[4]:.0f} months")
    
    print("\n" + "=" * 70)
    print("LOANS BY STATUS")
    print("=" * 70)
    
    cursor.execute("""
        SELECT LoanStatus, COUNT(*), SUM(LoanAmount)
        FROM Loans
        GROUP BY LoanStatus
        ORDER BY COUNT(*) DESC
    """)
    
    for row in cursor.fetchall():
        print(f"{row[0]:15} {row[1]:>6} loans  ${row[2]:>15,.2f}")
    
    print("\n" + "=" * 70)
    print("RISK DISTRIBUTION")
    print("=" * 70)
    
    cursor.execute("""
        SELECT RiskCategory, COUNT(*)
        FROM RiskScores
        GROUP BY RiskCategory
        ORDER BY 
            CASE RiskCategory 
                WHEN 'Low' THEN 1
                WHEN 'Moderate' THEN 2
                WHEN 'High' THEN 3
                WHEN 'Very High' THEN 4
            END
    """)
    
    for row in cursor.fetchall():
        print(f"{row[0]:15} {row[1]:>6} loans")
    
    print("\n" + "=" * 70)
    print("TOP 5 BORROWERS BY TOTAL LOAN AMOUNT")
    print("=" * 70)
    
    cursor.execute("""
        SELECT TOP 5
            b.BorrowerName,
            COUNT(l.LoanID) as LoanCount,
            SUM(l.LoanAmount) as TotalExposure
        FROM Borrowers b
        JOIN Loans l ON b.BorrowerID = l.BorrowerID
        GROUP BY b.BorrowerName
        ORDER BY TotalExposure DESC
    """)
    
    for row in cursor.fetchall():
        print(f"{row[0][:30]:30} {row[1]:>4} loans  ${row[2]:>15,.2f}")
    
    conn.close()
    
except Exception as e:
    print(f" Error: {e}")