import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite3 database
db_path = '/Userdata/proj2025/openkpi2/banco_de_dados.db'  # Replace with your database file path
conn = sqlite3.connect(db_path)

# Step 2: Query the data for a specific siteName and load it into a pandas DataFrame
site_name = 'CORAMANDEL'  # Replace with the desired siteName
query = f'''
SELECT generatedDate || ' ' || generatedTime AS dateTime, kpiValue
FROM LTE_8018A
WHERE siteName = '{site_name}' AND generatedDate IS NOT NULL AND generatedTime IS NOT NULL
ORDER BY generatedDate, generatedTime
'''
df = pd.read_sql_query(query, conn)

# Step 3: Close the database connection
conn.close()

# Step 4: Convert dateTime to a datetime object for proper plotting
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Step 5: Create a graphic using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(df['dateTime'], df['kpiValue'], marker='o', label=f'KPI Value for {site_name}')
plt.title(f'KPI Value Over Time for {site_name}')
plt.xlabel('Date/Time')
plt.ylabel('KPI Value')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Step 6: Show the plot
plt.show()