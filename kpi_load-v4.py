import os
import pandas as pd
import sqlite3
import shutil
import warnings 
from datetime import datetime


# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Specify the directory path
directory_path = '/Userdata/bkp_Grafana/Excell_file1/'
destination_path = '/Userdata/bkp_Grafana/temp_read/'
# Get a sorted list of files in the directory
files = sorted(os.listdir(directory_path))

def process_excel(file_path, database_name):
    # Step 1: Read the Excel file
    arquivo_excel = file_path

    sheet1 = pd.read_excel(arquivo_excel, sheet_name='Info')
    sheet2 = pd.read_excel(arquivo_excel, sheet_name='Dashboard')

    # Find the quantity of row into the sheet(Dashboard)
    row_count = sheet2.shape[0]

    # Verify if sheet2 is empty
    if sheet2.empty:
        print(f'>>> File with empty sheet: {file_name}')
        shutil.move(file_path, destination_path)
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
        date_str = cell_value2
        # print(date_str)
        # print(type(date_str))
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        #print(type(date_obj))
        # print(date_obj)
        sheet2.iloc[0:(row_count), 5] = date_str

        # sheet2.iloc[0:14, 6] = cell_value2[12:16]
    
        # Step 2: Connect to SQLite database
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Step 3: Create a table in the database
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LTE_8018A (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siteName TEXT,
            siteElement TEXT,
            reportId INT64,
            createAt TEXT,
            emptyField TEXT,
            kpiValue INTEGER
        )
        ''')

        # Step 4: Insert data from DataFrame into SQLite database
        for index, row in sheet2.iterrows():
            cursor.execute('''
            INSERT INTO LTE_8018A (siteName, siteElement, reportId, createAt,  emptyField, kpiValue)
            VALUES (?, ?, ?, ?, ?, COALESCE(?,0))
            ''', (row['siteName'], row['siteElement'], row['reportId'], row['createAt'],  row['emptyField'], row['kpiValue']))

        # Step 5: Commit and close the connection
        conn.commit()
        conn.close()
        shutil.move(file_path, destination_path)
        # Move the file to the read directory
        print(f"Data inserted into SQLite database for file: {file_name}")

        return 0

# Initialize a counter for empty files  
empty_file_count = 0

# Specify the database name
database_name = 'LTE8018.db'  # Replace with your desired database name

# Loop through all files in the directory
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        empty_file_count += process_excel(file_path, database_name)

print(f"Total number of empty files: {empty_file_count}")
