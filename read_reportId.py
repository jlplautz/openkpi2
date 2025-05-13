import sqlite3

# Specify the database name
database_name = 'LTE8018.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Query to get the last inserted record based on the `id` column
query = '''
SELECT reportId
FROM LTE_8018A
ORDER BY id DESC
LIMIT 1;
'''

# Execute the query
cursor.execute(query)
result = cursor.fetchone()

# Check if a result was found
if result:
    print(f"The last reportId is: {result[0]}")
    print(result)
else:
    print("No records found in the database.")

# Close the connection
conn.close()