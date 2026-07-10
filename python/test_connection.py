from config import get_connection

try:
    conn = get_connection()
    print("=" * 50)
    print("SUCCESS!")
    print("Connected to SQL Server.")
    print("=" * 50)
    conn.close()
except Exception as e:
    print("Connection failed.")
    print(e)