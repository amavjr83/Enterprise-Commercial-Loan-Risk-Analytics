"""
create_database.py
Creates the CommercialLoanAnalytics database if it doesn't exist.
"""
import pyodbc

# Connection to master database
SERVER = r"DESKTOP-K41C8P6\SQLEXPRESS"
DRIVER = "ODBC Driver 17 for SQL Server"

CONNECTION_STRING = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    "Initial Catalog=master;"
    "Trusted_Connection=yes;"
)

DATABASE = "CommercialLoanAnalytics"

try:
    print("Connecting to SQL Server...")
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    print("Connected successfully!")
    
    # Check if database exists
    cursor.execute(f"""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DATABASE}')
        BEGIN
            CREATE DATABASE {DATABASE}
            PRINT 'Database {DATABASE} created successfully!'
        END
        ELSE
        BEGIN
            PRINT 'Database {DATABASE} already exists.'
        END
    """)
    
    conn.commit()
    print(f" Database '{DATABASE}' is ready!")
    conn.close()
    
except Exception as e:
    print(f" Error creating database: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure SQL Server Express is running")
    print("2. Check if the server name is correct")
    print("3. Try using 'localhost\\SQLEXPRESS' instead")
    print("4. Make sure Windows Authentication is enabled")