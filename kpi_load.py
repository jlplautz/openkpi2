import os
import pandas as pd
import sqlite3

# Specify the directory path
directory_path = '/Userdata/bkp_Grafana/Excell_Files/'

# Get a sorted list of files in the directory
files = sorted(os.listdir(directory_path))


def process_excell(file_path):

    # Passo 1: Ler o arquivo Excel
    arquivo_excel = file_path

    sheet1 = pd.read_excel(arquivo_excel, sheet_name='Info')
    sheet2 = pd.read_excel(arquivo_excel, sheet_name='Dashboard')
                           
    # Verify if sheet2 column 1, cell 0 has content
    if  sheet2.empty:
        print(f'>>> File with empty sheet', {file_path})
    else:
        # REading the sheet excel and renamed the collumns
        sheet2 = pd.read_excel(arquivo_excel, sheet_name='Dashboard', names=[
                'siteName', 'siteElement', 'kpiId', 'kpiName', 'reportId',
                'generatedDate', 'generatedTime', 'kpiValue'])  

        # copying Cell value from sheet Info and writting into sheet Dashboard
        cell_value1 = sheet1.iloc[0,1]
        sheet2.iloc[0:14, 4] = int(cell_value1)
        cell_value2 = sheet1.iloc[5,1]

        sheet2.iloc[0:14, 5] = cell_value2[:10]
        sheet2.iloc[0:14, 6] = cell_value2[12:16]

        # Save the changes to the Excel file
        with pd.ExcelWriter(arquivo_excel, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            sheet1.to_excel(writer, sheet_name="Info", index=False)
            sheet2.to_excel(writer, sheet_name="Dashboard", index=False)

        # print("Cell copied successfully!")
        print(f'Processing file: {file_path}')

        # Passo 2: Conectar ao banco de dados SQLite (ou criar um novo)
        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        # Passo 3: Criar uma tabela no banco de dados
        # Suponhamos que o arquivo Excel tenha as colunas: 'siteName', 'siteElement', 'reportId', 'generatedDate', 'generatedTime', 'kpiValue'
        cursor.execute('''

        CREATE TABLE IF NOT EXISTS LTE_8018A (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siteName TEXT,
            siteElement TEXT,
            reportId INT64,
            generatedDate DATE,
            generatedTime TIME,                
            kpiValue DOUBLE
        )
        ''')

        # Passo 4: Inserir os dados do DataFrame no banco de dados SQLite
        for index, row in sheet2.iterrows():
            cursor.execute('''
            INSERT INTO LTE_8018A (siteName, siteElement, reportId, generatedDate, generatedTime, kpiValue)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['siteName'], row['siteElement'], row['reportId'], row['generatedDate'], row['generatedTime'], row['kpiValue']))

        # Passo 5: Commit e fechar a conexão
        conn.commit()
        conn.close()

        print("Dados inseridos com sucesso no banco de dados SQLite.")

# loop through all files i the directory
#for file in os.listdir(directory):
#    if file.endswith('.xlsx') or file.endswith('.xls'):
#        file_path = os.path.join(directory, file)
#        process_excell(file_path)

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
#        print(f"Reading file: {file_name}")
        process_excell(file_path)
        
#        with open(file_path, 'r') as file:
#            content = file.read()
#            print(content)