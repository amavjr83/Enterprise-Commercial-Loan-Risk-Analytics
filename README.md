#  Enterprise Commercial Loan Risk Analytics

##  Project Overview
A complete commercial loan analytics platform with realistic data generation, risk scoring, and an interactive Power BI dashboard.

**Total Dataset:** 118,660 rows  
**Total Portfolio:** $5.58 Billion  
**Active Loans:** 542

---

##  Key Features

- **4-page Interactive Power BI Dashboard**
- **Python ETL Pipeline** with 8 data generation scripts
- **SQL Server Database** with 8 normalized tables
- **Risk Scoring** with LTV, DSCR, and composite scores
- **Delinquency Analysis** with payment tracking
- **Portfolio Analytics** with concentration metrics

---

##  Technologies Used

| Category | Technologies |
|----------|--------------|
| **Database** | SQL Server, T-SQL |
| **Visualization** | Power BI, DAX |
| **Data Engineering** | Python, pyodbc, pandas, numpy |
| **Version Control** | Git, GitHub |

---

##  Dashboard Pages

### 1. Executive Overview
- Key KPIs and portfolio summary
- Loans by status and risk distribution
- Top borrowers and property types

### 2. Risk Analysis
- Risk distribution (Low, Moderate, High, Very High)
- LTV vs DSCR scatter plot
- Risk by loan type
- Portfolio at risk trend

### 3. Delinquency Analysis
- Payment status breakdown
- Delinquency trends over time
- Avg days late by loan type
- Top delinquent borrowers

### 4. Portfolio Details
- Geographic distribution (map)
- Loan concentration analysis
- Detailed portfolio table
- Interest rate distribution

---

##  Key Insights

| Metric | Value |
|--------|-------|
| Total Portfolio | $5.58 Billion |
| Total Loans | 600 |
| Average Loan Size | $9.3 Million |
| Average Interest Rate | 6.85% |
| On-Time Payment Rate | 99% |
| Default Rate | 4% |

### Loan Status
- **Active:** 542 loans ($5.04B)
- **Closed:** 33 loans ($302M)
- **Default:** 25 loans ($239M)

### Risk Distribution
- **High Risk:** 362 loans
- **Very High Risk:** 222 loans
- **Moderate Risk:** 16 loans

---

##  How to Run This Project

### 1. Database Setup
```sql
-- Run SQL scripts in order:
01_CreateDatabase.sql
02_CreateTables.sql
03_CreateIndexes.sql
04_Views.sql
05_AnalyticsQueries.sql
