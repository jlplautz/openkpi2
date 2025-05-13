import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite3 database
db_path = '/Userdata/proj2025/openkpi2/banco_de_dados.db'  # Replace with your database file path
conn = sqlite3.connect(db_path)

# Step 2: Query the data and load it into a pandas DataFrame
query = '''
SELECT generatedDate, kpiValue
FROM LTE_8018A
WHERE generatedDate IS NOT NULL
ORDER BY generatedDate
'''
df = pd.read_sql_query(query, conn)

# Step 3: Close the database connection
conn.close()

# Step 4: Create a graphic using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(pd.to_datetime(df['generatedDate']), df['kpiValue'], marker='o', label='KPI Value')
plt.title('KPI Value Over Time')
plt.xlabel('Date')
plt.ylabel('KPI Value')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Step 5: Show the plot
plt.show()