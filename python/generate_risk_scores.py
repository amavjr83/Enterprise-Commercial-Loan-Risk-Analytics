"""
generate_risk_scores.py
Generates risk scores for all loans.
"""
import random
from config import get_connection

def generate_risk_scores():
    """Generate risk scores for loans"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all loans with property and borrower info
    cursor.execute("""
        SELECT 
            l.LoanID,
            l.LoanAmount,
            l.InterestRate,
            p.MarketValue,
            p.OccupancyRate,
            b.CreditScore,
            b.RiskTier
        FROM Loans l
        JOIN Properties p ON l.PropertyID = p.PropertyID
        JOIN Borrowers b ON l.BorrowerID = b.BorrowerID
    """)
    
    loans = cursor.fetchall()
    print(f"Found {len(loans)} loans for risk scoring")
    
    if not loans:
        print("No loans found!")
        conn.close()
        return
    
    scores_inserted = 0
    
    for loan in loans:
        loan_id, loan_amount, rate, market_value, occupancy, credit_score, risk_tier = loan
        
        # Convert to float
        loan_amount = float(loan_amount)
        market_value = float(market_value)
        occupancy = float(occupancy) if occupancy else 0.8
        credit_score = float(credit_score) if credit_score else 700
        
        # Calculate LTV (Loan-to-Value)
        ltv = loan_amount / market_value if market_value > 0 else 0.8
        
        # Calculate DSCR (Debt Service Coverage Ratio)
        # Simplified: assume NOI = 5% of property value
        noi = market_value * 0.05
        annual_debt_service = loan_amount * float(rate)
        dscr = noi / annual_debt_service if annual_debt_service > 0 else 1.5
        
        # Calculate Debt Yield
        debt_yield = noi / loan_amount if loan_amount > 0 else 0.05
        
        # Composite risk score (0-100, lower is better)
        risk_score = 0
        risk_score += min(100, ltv * 80)  # LTV factor
        risk_score += max(0, (1 - dscr) * 50)  # DSCR factor
        risk_score += max(0, (1 - occupancy) * 30)  # Occupancy factor
        risk_score += max(0, (1 - credit_score/850) * 50)  # Credit score factor
        
        # Normalize to 0-100
        risk_score = min(100, max(0, int(risk_score)))
        
        # Risk category
        if risk_score < 30:
            risk_category = 'Low'
        elif risk_score < 50:
            risk_category = 'Moderate'
        elif risk_score < 70:
            risk_category = 'High'
        else:
            risk_category = 'Very High'
        
        # Insert risk score
        cursor.execute("""
            INSERT INTO RiskScores (
                LoanID, LTV, DSCR, DebtYield, CompositeRiskScore, RiskCategory, ScoreDate
            ) VALUES (?, ?, ?, ?, ?, ?, GETDATE())
        """, (loan_id, round(ltv, 3), round(dscr, 2), round(debt_yield, 3),
              risk_score, risk_category))
        
        scores_inserted += 1
        
        if scores_inserted % 100 == 0:
            conn.commit()
            print(f"  Inserted {scores_inserted} risk scores...")
    
    conn.commit()
    conn.close()
    print(f" Inserted {scores_inserted} risk scores!")

if __name__ == "__main__":
    print("=" * 60)
    print("RISK SCORE GENERATION")
    print("=" * 60)
    generate_risk_scores()
    print("\n Risk score generation complete!")