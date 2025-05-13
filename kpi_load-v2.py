import os
import pandas as pd
import sqlite3

# Specify the directory path
directory_path = '/Userdata/bkp_Grafana/Excell_Files/'

# Get a sorted list of files in the directory
files = sorted(os.listdir(directory_path))


def process_excel(file_path):
    # Step 1: Read the Excel file
    arquivo_excel = file_path

    sheet1 = pd.read_excel(arquivo_excel, sheet_name='Info')
    sheet2 = pd.read_excel(arquivo_excel, sheet_name='Dashboard')

    # Verify if sheet2 is empty
    if sheet2.empty:
        print(f'>>> File with empty sheet: {file_name}')
    else:
        # Rename columns for sheet2
        sheet2.columns = [
            'siteName', 'siteElement', 'kpiId', 'kpiName', 'reportId',
            'generatedDate', 'generatedTime', 'kpiValue'
        ]

        # Copy cell values from sheet1 to sheet2 (in memory only)
        cell_value1 = sheet1.iloc[0, 1]
        sheet2.iloc[0:14, 4] = int(cell_value1)
        cell_value2 = sheet1.iloc[5, 1]
        sheet2.iloc[0:14, 5] = cell_value2[:10]
        sheet2.iloc[0:14, 6] = cell_value2[12:16]

        # Step 2: Connect to SQLite database
        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        # Step 3: Create a table in the database
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LTE_8018A (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siteName TEXT,
            siteElement TEXT,
            reportId INT64,
            generatedDate DATE,
            generatedTime TIME,
            kpiValue INTEGER
        )
        ''')

        # Step 4: Insert data from DataFrame into SQLite database
        for index, row in sheet2.iterrows():
            cursor.execute('''
            INSERT INTO LTE_8018A (siteName, siteElement, reportId, generatedDate, generatedTime, kpiValue)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['siteName'], row['siteElement'], row['reportId'], row['generatedDate'], row['generatedTime'], row['kpiValue']))

        # Step 5: Commit and close the connection
        conn.commit()
        conn.close()

        print(f"Data successfully inserted into SQLite database for file: {file_name}")


# Loop through all files in the directory
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        process_excel(file_path)