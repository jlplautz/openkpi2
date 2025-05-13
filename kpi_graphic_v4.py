import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite3 database
db_path = '/Userdata/proj2025/openkpi2/LTE8018.db'  # Replace with your database file path
conn = sqlite3.connect(db_path)

# Step 2: Query the data for a specific siteName and load it into a pandas DataFrame
site_name = 'JABORANDI - FAZ. SANTA EFIGÊNIA'  # Replace with the desired siteName
query = f'''
SELECT createAt, kpiValue
FROM LTE_8018A
WHERE siteName = '{site_name}' AND createAt IS NOT NULL
ORDER BY createAt
'''
df = pd.read_sql_query(query, conn)

# Step 3: Close the database connection
conn.close()

# Step 4: Combine generatedDate and generatedTime into a single datetime column
df['dateTime'] = pd.to_datetime(df['createAt'])

# Step 5: Create a graphic using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(df['dateTime'], df['kpiValue'], marker='o', label=f'KPI Value for {site_name}')
plt.title(f'KPI Value vs Date/Time for {site_name}')
plt.xlabel('KPI Value')
plt.ylabel('Date/Time')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Step 6: Show the plot
plt.show()