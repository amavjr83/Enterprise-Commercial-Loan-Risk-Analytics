"""
check_schema.py
Check the schema of all tables.
"""
from config import get_connection

conn = get_connection()
cursor = conn.cursor()

# Check Properties table
print("=" * 60)
print("PROPERTIES TABLE SCHEMA")
print("=" * 60)
cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'Properties'
    ORDER BY ORDINAL_POSITION
""")

for row in cursor.fetchall():
    print(f"{row[0]:20} {row[1]:15} {row[2]}")

# Check Loans table
print("\n" + "=" * 60)
print("LOANS TABLE SCHEMA")
print("=" * 60)
cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'Loans'
    ORDER BY ORDINAL_POSITION
""")

for row in cursor.fetchall():
    print(f"{row[0]:20} {row[1]:15} {row[2]}")

# Check Borrowers table
print("\n" + "=" * 60)
print("BORROWERS TABLE SCHEMA")
print("=" * 60)
cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'Borrowers'
    ORDER BY ORDINAL_POSITION
""")

for row in cursor.fetchall():
    print(f"{row[0]:20} {row[1]:15} {row[2]}")

conn.close()