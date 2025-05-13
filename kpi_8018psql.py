import os
from datetime import datetime
import pandas as pd
import psycopg2


# Specify the directory path
directory_path = '/Userdata/bkp_Grafana/Excell_Files/'

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
        date_str = cell_value2
        sheet2.iloc[0:(row_count), 5] = cell_value2[0:16]

        # Step 2: Connect to PostgreSQL database
        conn = psycopg2.connect(**database_config)
        cursor = conn.cursor()

        # Step 3: Create a table in the database
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LTE_8018A (
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
            INSERT INTO LTE_8018A (siteName, siteElement, reportId, createAt, emptyField, kpiValue)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (row['siteName'], row['siteElement'], row['reportId'], row['createAt'], row['emptyField'], row['kpiValue']))

        # Step 5: Commit and close the connection
        conn.commit()
        conn.close()

        print(f"Data inserted into PostgreSQL database for file: {file_name}")


# PostgreSQL database configuration
database_config = {
    'dbname': 'LTE8018A',  # Replace with your database name
    'user': 'Plautz',        # Replace with your username
    'password': '123456',# Replace with your password
    'host': 'localhost',        # Replace with your PostgreSQL host
    'port': 5432                # Default PostgreSQL port
}

# Loop through all files in the directory
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        process_excel(file_path, database_config)