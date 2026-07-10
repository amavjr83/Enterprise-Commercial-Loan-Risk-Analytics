"""
generate_market_data.py
Generates market data for cities.
"""
import random
from datetime import datetime, timedelta
from config import get_connection

# Cities from our properties
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 
          'San Diego', 'Dallas', 'Austin', 'San Jose', 'Jacksonville', 'Fort Worth', 'Columbus', 
          'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington', 
          'Boston', 'El Paso', 'Detroit', 'Nashville', 'Memphis', 'Portland', 'Oklahoma City', 
          'Las Vegas', 'Louisville', 'Baltimore', 'Milwaukee', 'Albuquerque', 'Tucson', 'Fresno', 
          'Sacramento', 'Kansas City', 'Mesa', 'Atlanta', 'Omaha', 'Colorado Springs', 'Raleigh', 
          'Miami', 'Oakland', 'Minneapolis', 'Tulsa', 'Wichita', 'New Orleans', 'Arlington', 
          'Cleveland', 'Bakersfield', 'Tampa', 'Aurora', 'Honolulu', 'Anaheim', 'Santa Ana', 
          'Corpus Christi', 'Riverside', 'St. Louis', 'Lexington', 'Stockton', 'Pittsburgh', 
          'Cincinnati', 'Anchorage', 'Plano', 'Orlando', 'Durham', 'Chula Vista', 'Toledo', 
          'Fort Wayne', 'St. Petersburg', 'Laredo', 'Jersey City', 'Chandler', 'Madison', 
          'Lubbock', 'Scottsdale', 'Reno', 'Buffalo', 'Gilbert', 'Glendale', 'North Las Vegas', 
          'Winston-Salem', 'Chesapeake', 'Norfolk', 'Fremont', 'Garland', 'Irving', 'Hialeah', 
          'Boise', 'Richmond', 'Baton Rouge', 'Des Moines', 'Spokane', 'Modesto', 'Tacoma', 
          'Fontana', 'Santa Clarita', 'San Bernardino', 'Port St. Lucie', 'Fayetteville']

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
          'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
          'VA', 'WA', 'WV', 'WI', 'WY']

def generate_market_data():
    """Generate market data for cities"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"Generating market data for {len(CITIES)} cities...")
    
    inserted = 0
    
    for city in CITIES:
        state = random.choice(STATES)
        
        # Generate realistic market metrics
        avg_rent = random.randint(15, 75)  # $ per sq ft
        vacancy_rate = round(random.uniform(0.03, 0.15), 3)
        cap_rate = round(random.uniform(0.04, 0.09), 3)
        economic_growth = round(random.uniform(-0.02, 0.05), 3)
        
        # Data date (last 2 years)
        data_date = datetime.now() - timedelta(days=random.randint(0, 730))
        data_date = data_date.date()
        
        cursor.execute("""
            INSERT INTO MarketData (
                City, State, AvgRentPerSqFt, VacancyRate, CapRate, EconomicGrowthRate, DataDate
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (city, state, avg_rent, vacancy_rate, cap_rate, economic_growth, data_date))
        
        inserted += 1
        
        if inserted % 20 == 0:
            conn.commit()
            print(f"  Inserted {inserted} market records...")
    
    conn.commit()
    conn.close()
    print(f" Inserted {inserted} market data records!")

if __name__ == "__main__":
    print("=" * 60)
    print("MARKET DATA GENERATION")
    print("=" * 60)
    generate_market_data()
    print("\n Market data generation complete!")