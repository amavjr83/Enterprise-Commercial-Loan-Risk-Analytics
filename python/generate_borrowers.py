"""
generate_borrowers.py
Generates realistic commercial borrower data for the CommercialLoanAnalytics database.
Creates 1,000+ borrowers with real company names, industries, and financials.
"""
import random
import numpy as np
from datetime import datetime, timedelta
from config import get_connection

# -------------------------------------------------------
# DATA SETS FOR REALISTIC GENERATION
# -------------------------------------------------------

# Real company name components
COMPANY_PREFIXES = ['Apex', 'Apex', 'Arctic', 'Atlantic', 'Aurora', 'Azure', 'Bell', 'Blue', 'Cascade', 'Central', 
                    'Coastal', 'Crest', 'Crown', 'Diamond', 'Digital', 'Dynamo', 'Eagle', 'East', 'Eclipse', 'Elite', 
                    'Emerald', 'Empire', 'Endeavor', 'Energy', 'Everest', 'Excellence', 'Falcon', 'First', 'Fortress', 
                    'Frontier', 'Fusion', 'Genesis', 'Global', 'Golden', 'Gothic', 'Granite', 'Graphite', 'Great', 
                    'Green', 'Gulf', 'Halcyon', 'Harbor', 'Harvest', 'Heritage', 'Horizon', 'Imperial', 'Infinity', 
                    'Innovation', 'Integrity', 'Interstate', 'Iron', 'Ivy', 'Jade', 'Jasper', 'Jubilee', 'Keystone', 
                    'Kings', 'Lakes', 'Lancaster', 'Landmark', 'Liberty', 'Lighthouse', 'Lunar', 'Magna', 'Magnetic', 
                    'Majestic', 'Mallard', 'Maple', 'Maritime', 'Marlin', 'Maverick', 'Meridian', 'Metro', 'Midwest', 
                    'Millennium', 'Minerva', 'Momentum', 'Monarch', 'Mountain', 'National', 'Nautilus', 'Navigator', 
                    'Nexus', 'Noble', 'Northern', 'Nova', 'Oak', 'Oceanic', 'Olympic', 'Omega', 'Opal', 'Opus', 
                    'Orion', 'Pacific', 'Palm', 'Panorama', 'Paramount', 'Patriot', 'Pegasus', 'Penn', 'Pinnacle', 
                    'Pioneer', 'Platinum', 'Polar', 'Prestige', 'Prime', 'Progressive', 'Prometheus', 'Prosperity', 
                    'Pulse', 'Quantum', 'Quartz', 'Queen', 'Radiant', 'Redwood', 'Regal', 'Renaissance', 'Republic', 
                    'Reserve', 'Resolute', 'Revelation', 'Ridge', 'Rising', 'River', 'Rocket', 'Royal', 'Ruby', 'Sage', 
                    'Sapphire', 'Saturn', 'Savannah', 'Scenic', 'Serenity', 'Shield', 'Sierra', 'Silver', 'Sky', 
                    'Sovereign', 'Spire', 'Stellar', 'Sterling', 'Stone', 'Stratosphere', 'Summit', 'Sun', 'Sunrise', 
                    'Sunset', 'Superior', 'Surf', 'Swan', 'Talon', 'Tempo', 'Terra', 'Thor', 'Thunder', 'Timber', 
                    'Titan', 'Titanium', 'Tranquility', 'Traverse', 'Trident', 'Trinity', 'Triumph', 'Tundra', 
                    'Twin', 'Ultima', 'Ultra', 'United', 'Unity', 'Universal', 'University', 'Uplift', 'Valley', 
                    'Vanguard', 'Velocity', 'Venus', 'Verdant', 'Veritas', 'Vernon', 'Vertex', 'Victoria', 'Viking', 
                    'Village', 'Violet', 'Viridian', 'Virtue', 'Vista', 'Vital', 'Volcano', 'Vortex', 'Voyage', 
                    'Warrior', 'Water', 'West', 'Western', 'Whisper', 'Wilderness', 'Willow', 'Windsor', 'Wings', 
                    'Winslow', 'Winston', 'Winter', 'Wisteria', 'Wolves', 'Woodland', 'Wyndham', 'Xavier', 'Xenon', 
                    'Yankee', 'York', 'Yosemite', 'Zephyr', 'Zeus', 'Zion']

COMPANY_SUFFIXES = ['Capital', 'Partners', 'Group', 'Enterprises', 'Holdings', 'Ventures', 'Corporation', 'Associates', 
                    'Investments', 'Management', 'Resources', 'Solutions', 'Innovations', 'Dynamics', 'Concepts', 
                    'Professionals', 'Strategic', 'Alliance', 'Bancorp', 'Financial', 'Asset Management', 'Wealth', 
                    'Advisors', 'Equity', 'Securities', 'Merchant', 'Commercial', 'Real Estate', 'Development', 
                    'Construction', 'Technology', 'Logistics', 'Transport', 'Energy Solutions', 'Renewable', 'Medical', 
                    'Dental', 'Legal', 'Consulting', 'Executive', 'Premier', 'Fortress', 'Heritage', 'Legacy', 'Prime']

# Real industries
INDUSTRIES = [
    'Construction', 'Real Estate Development', 'Property Management', 'Retail', 'Hospitality',
    'Healthcare', 'Technology', 'Manufacturing', 'Transportation', 'Logistics', 'Energy',
    'Renewable Energy', 'Professional Services', 'Legal Services', 'Medical Practice',
    'Dental Practice', 'Accounting', 'Architecture', 'Engineering', 'Education',
    'Financial Services', 'Investment Management', 'Insurance', 'Agriculture',
    'Food Processing', 'Distribution', 'Wholesale', 'Restaurants', 'Entertainment',
    'Media', 'Telecommunications', 'Utilities', 'Mining', 'Oil & Gas'
]

# Entity types
ENTITY_TYPES = ['LLC', 'Corporation', 'Partnership', 'Sole Proprietorship', 'LLP', 'Trust']

# -------------------------------------------------------
# GENERATION FUNCTIONS
# -------------------------------------------------------

def generate_company_name():
    """Generate a realistic company name"""
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    
    # Sometimes add a location word
    if random.random() < 0.3:
        locations = ['National', 'Regional', 'American', 'Northern', 'Southern', 'Eastern', 'Western', 'Central']
        return f"{prefix} {random.choice(locations)} {suffix}"
    
    return f"{prefix} {suffix}"

def generate_industry():
    """Select a realistic industry"""
    return random.choice(INDUSTRIES)

def generate_entity_type():
    """Select an entity type"""
    weights = [0.45, 0.30, 0.15, 0.05, 0.04, 0.01]  # LLC most common
    return random.choices(ENTITY_TYPES, weights=weights)[0]

def generate_annual_revenue():
    """Generate annual revenue with realistic distribution"""
    # Log-normal distribution for revenue
    mu = 15.0  # Mean of log
    sigma = 1.2  # Standard deviation of log
    revenue = np.random.lognormal(mu, sigma)
    
    # Round to nearest thousand
    return round(revenue / 1000) * 1000

def generate_total_assets():
    """Generate total assets based on revenue with some variation"""
    revenue = generate_annual_revenue()
    # Assets typically 1-5x revenue for commercial borrowers
    multiplier = random.uniform(1.5, 5.0)
    assets = revenue * multiplier
    return round(assets / 1000) * 1000

def generate_credit_score():
    """Generate a credit score (300-850) with realistic distribution"""
    # Most businesses have good credit
    scores = []
    for _ in range(100):
        # Mixture of distributions
        if random.random() < 0.6:
            # Good credit (650-800)
            score = int(np.random.normal(720, 40))
        elif random.random() < 0.85:
            # Excellent credit (800-850)
            score = int(np.random.normal(820, 20))
        else:
            # Poor credit (500-650)
            score = int(np.random.normal(600, 50))
        scores.append(max(300, min(850, score)))
    return random.choice(scores)

def generate_risk_tier(credit_score):
    """Determine risk tier based on credit score"""
    if credit_score >= 750:
        return 'A'
    elif credit_score >= 700:
        return 'B'
    elif credit_score >= 650:
        return 'C'
    elif credit_score >= 600:
        return 'D'
    else:
        return 'E'

def generate_borrowers(num_borrowers=1000):
    """Generate borrower data and insert into database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"Generating {num_borrowers} borrowers...")
    
    borrowers_inserted = 0
    batch_size = 100
    
    for i in range(num_borrowers):
        company_name = generate_company_name()
        entity_type = generate_entity_type()
        industry = generate_industry()
        annual_revenue = generate_annual_revenue()
        total_assets = generate_total_assets()
        credit_score = generate_credit_score()
        risk_tier = generate_risk_tier(credit_score)
        
        # Insert into database
        cursor.execute("""
            INSERT INTO Borrowers (
                BorrowerName, EntityType, Industry, AnnualRevenue, 
                TotalAssets, CreditScore, RiskTier, CreatedDate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
        """, (company_name, entity_type, industry, annual_revenue, 
              total_assets, credit_score, risk_tier))
        
        borrowers_inserted += 1
        
        # Commit in batches
        if borrowers_inserted % batch_size == 0:
            conn.commit()
            print(f"  Inserted {borrowers_inserted} borrowers...")
    
    conn.commit()
    conn.close()
    
    print(f" Successfully inserted {borrowers_inserted} borrowers!")
    return borrowers_inserted

# -------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("COMMERCIAL LOAN RISK ANALYTICS")
    print("Borrower Data Generation")
    print("=" * 60)
    
    # Generate 1000 borrowers
    generate_borrowers(1000)
    
    print("\n Borrower generation complete!")
    print("Next: Run generate_properties.py")