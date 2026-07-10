"""
generate_properties.py
Generates realistic commercial property data.
"""
import random
from config import get_connection

# Data sets
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

PROPERTY_TYPES = ['Office', 'Retail', 'Industrial', 'Warehouse', 'Multifamily', 
                  'Hospitality', 'Medical Office', 'Data Center', 'Self-Storage']

def generate_properties(num_properties=800):
    """Generate property data and insert into database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"Generating {num_properties} properties...")
    
    properties_inserted = 0
    batch_size = 50
    
    for i in range(num_properties):
        # Generate property details
        property_type = random.choice(PROPERTY_TYPES)
        
        # Market value based on property type
        if property_type in ['Office', 'Retail']:
            market_value = random.randint(2_000_000, 20_000_000)
        elif property_type in ['Industrial', 'Warehouse']:
            market_value = random.randint(3_000_000, 25_000_000)
        elif property_type == 'Multifamily':
            market_value = random.randint(1_000_000, 30_000_000)
        elif property_type == 'Hospitality':
            market_value = random.randint(5_000_000, 40_000_000)
        elif property_type == 'Data Center':
            market_value = random.randint(10_000_000, 50_000_000)
        else:
            market_value = random.randint(1_000_000, 15_000_000)
        
        # Round to nearest thousand
        market_value = round(market_value / 1000) * 1000
        
        # Occupancy rate (60-98%)
        occupancy_rate = round(random.uniform(0.60, 0.98), 3)
        
        # NOI (3-9% of market value)
        cap_rate = random.uniform(0.03, 0.09)
        net_operating_income = round((market_value * cap_rate) / 1000) * 1000
        
        # Year built (1950-2025)
        year_built = random.randint(1950, 2025)
        
        # City and state
        city = random.choice(CITIES)
        state = random.choice(STATES)
        
        # Address
        street_num = random.randint(100, 9999)
        street_names = ['Main St', 'Broadway', 'Park Ave', 'Market St', 'Elm St', 'Oak St', 
                       'Pine St', 'Maple Ave', 'Cedar St', 'Washington Ave', 'Commerce Dr',
                       'Corporate Dr', 'Innovation Dr', 'Technology Dr', 'Research Blvd']
        street = random.choice(street_names)
        address = f"{street_num} {street}"
        
        property_name = f"{property_type} Property - {city}"
        
        # Insert into database - NO BorrowerID column!
        cursor.execute("""
            INSERT INTO Properties (
                PropertyName, PropertyType, Address, City, State,
                MarketValue, OccupancyRate, NetOperatingIncome, YearBuilt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (property_name, property_type, address, city, state,
              market_value, occupancy_rate, net_operating_income, year_built))
        
        properties_inserted += 1
        
        # Commit in batches
        if properties_inserted % batch_size == 0:
            conn.commit()
            print(f"  Inserted {properties_inserted} properties...")
    
    conn.commit()
    conn.close()
    
    print(f" Successfully inserted {properties_inserted} properties!")
    return properties_inserted

if __name__ == "__main__":
    print("=" * 60)
    print("PROPERTY DATA GENERATION")
    print("=" * 60)
    generate_properties(800)
    print("\n Property generation complete!")