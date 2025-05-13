import os
import shutil
from datetime import datetime
import pandas as pd
import psycopg2

# Specify the directory path
# directory_path = '/var/app/current/ArgusApp/app/uploads/pm/report'
# destination_path = '/var/app/current/ArgusApp/app/uploads/pm/report_read'
directory_path = "/Userdata/bkp_Grafana/temp"
destination_path = "/Userdata/bkp_Grafana/temp_read"


# Get a sorted list of files in the directory
files = sorted(os.listdir(directory_path))

def process_excel(file_path, database_config):
    # Step 1: Read the Excel file
    arquivo_excel = file_path

    sheet1 = pd.read_excel(arquivo_excel, sheet_name='Info')
    sheet2 = pd.read_excel(arquivo_excel, sheet_name='Dashboard')

    # Find the quantity of rows in the sheet (Dashboard)
    row_count = sheet2.shape[0]
    
    # Verify if sheet2 is empty
    if sheet2.empty:
        print(f'>>> File with empty sheet: {file_name}')

        return 1
    else:
        # Rename columns for sheet2
        sheet2.columns = [
            'siteName', 'siteElement', 'kpiId', 'kpiName', 'reportId',
            'createAt', 'emptyField', 'kpiValue'
        ]

        # Copy cell values from sheet1 to sheet2 (in memory only)
        cell_value1 = sheet1.iloc[0, 1]
        sheet2.iloc[0:(row_count), 4] = int(cell_value1)
        cell_value2 = sheet1.iloc[5, 1]
        date_str = cell_value2[:16]
        sheet2.iloc[0:(row_count), 5] = pd.to_datetime(date_str)

        # Step 2: Connect to PostgreSQL database
        conn = psycopg2.connect(**database_config)
        cursor = conn.cursor()

        # Step 3: Create a table in the database
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lte8018a (
            id SERIAL PRIMARY KEY,
            siteName TEXT,
            siteElement TEXT,
            reportId BIGINT,
            createAt TIMESTAMP,
            emptyField TEXT,
            kpiValue INTEGER
       )
        ''')
 
        # Step 4: Insert data from DataFrame into PostgreSQL database
        for index, row in sheet2.iterrows():
            cursor.execute('''
            INSERT INTO lte8018a (siteName, siteElement, reportId, createAt, emptyField, kpiValue)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (row['siteName'], row['siteElement'], row['reportId'], row['createAt'], row['emptyField'], row['kpiValue']))

        # Step 5: Commit and close the connection
        conn.commit()
        conn.close()
        shutil.move(file_name, destination_path)  # Move the file to the read directory
        return 0

        print(f"Data inserted into PostgreSQL database for file: {file_name}")

# PostgreSQL database configuration
database_config = {
    'dbname': 'LTE8018A',  # Replace with your database name
    'user': 'plautz',      # Replace with your username
    'password': '123456',  # Replace with your password
    'host': 'localhost',   # Replace with your PostgreSQL host
    'port': 5433           # Default PostgreSQL port
}

# Initialize a counter for empty files  
empty_file_count = 0

# Loop through all files in the directory
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        empty_file_count += process_excel(file_path, database_config)

print(f"Total number of empty files: {empty_file_count}")

'''
docker run --name kpidata -e POSTGRES_USER=Plautz -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=LTE8018A -p 5433:5432 -d postgres:11

sudo systemctl restart postgresql
docker exec -it <container_name> bash

Step 1: Access the PostgreSQL Container

Connect to the Database:
psql -U <username> -d <database_name>


Solution: Run a Second PostgreSQL Container on a Different Port
You can run a second PostgreSQL container by mapping it to a different port on the host machine (e.g., 5433).

Command to Run the Second Container
docker run --name second-postgres-container \
  -e POSTGRES_USER=Plautz \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=LTE8018A \
  -p 5433:5432 \
  -d postgres:11

--name second-postgres-container: Assigns a unique name to the second container.
-p 5433:5432: Maps port 5432 inside the container to port 5433 on the host machine.
The rest of the environment variables (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB) configure the database as usual.


docker exec -it kpidata bash
psql -U Plautz -d LTE8018A
DELETE FROM lte8018a;
'''