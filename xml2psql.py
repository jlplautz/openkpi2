import os
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import psycopg2

"""
This script processes XML files containing KPI data, extracts relevant information,
and saves it to CSV files. It handles multiple measurement types and appends data 
to existing files if they already exist.

Created by: O&M Solis
Date: 2025-10-01   

Dockerfile: Dockerfile
docker run --name kpidatabase -e POSTGRES_USER=Solis -e POSTGRES_PASSWORD=Solis2025 -p 5434:5432 -d postgres:11
docker exec -it kpidatabase bash
psql -U Solis
"""


# Directory containing KPI files
directory_path = "/var/openkpi/kpi_files"

# PostgreSQL connection details
db_config = {
    "dbname": "kpiDatabase",
    "user": "Solis",
    "password": "Solis2025",
    "host": "localhost",
    "port": 5434
}

# Function to insert data into PostgreSQL
def insert_into_postgres(data):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the kpi_data table
        insert_query = """
        INSERT INTO kpi_data (create_at, manage_object, measurement_type, kpi_name, kpi_value)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)

        # Commit the transaction
        conn.commit()
        print(f"Inserted {len(data)} rows into the database.")

        # Close the connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {e}")

# Function to process KPI files
def process_kpiFiles(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize a dictionary to store data for each measurementType
    data_by_measurementType = {}

    # List to store rows for PostgreSQL insertion
    postgres_data = []

    # Iterate through the XML tree and extract the desired data
    for PMSetup in root.iter('PMSetup'):
        # Extract common fields for the row
        createAt = PMSetup.attrib.get('startTime')

        for PMMOResult in PMSetup.iter('PMMOResult'):
            manageObject = None
            measurementType = None

            for child in PMMOResult:
                if child.tag == 'MO':
                    for subchild in child:
                        if subchild.tag == 'baseId':
                            manageObject = subchild.text
                elif child.tag == 'NE-WBTS_1.0':
                    measurementType = child.attrib.get('measurementType')

                    # Initialize the data structure for this measurementType if not already done
                    if measurementType not in data_by_measurementType:
                        data_by_measurementType[measurementType] = []

                    # Create a dictionary to store KPI values for this row
                    row = {
                        'createAt': createAt,
                        'manageObject': manageObject
                    }

                    # Add KPI values as columns
                    has_kpi_value = False  # Track if there is any kpiValue > 0
                    for subchild in child:
                        if int(subchild.text) > 0:
                            row[subchild.tag] = int(subchild.text)
                            has_kpi_value = True

                            # Add data to PostgreSQL list
                            postgres_data.append((
                                createAt,
                                manageObject,
                                measurementType,
                                subchild.tag,
                                int(subchild.text)
                            ))

                    # Append the row to the corresponding measurementType
                    if has_kpi_value:
                        data_by_measurementType[measurementType].append(row)

    # # Insert data into PostgreSQL
    # if postgres_data:
    #     insert_into_postgres(postgres_data)

    # # Append or create CSV files for each measurementType
    # for measurementType, rows in data_by_measurementType.items():
    #     if rows:  # Only proceed if there are rows with kpiValue > 0
    #         df_new = pd.DataFrame(rows)

    #         # Check if the CSV file for this measurementType already exists
    #         filename = f"{measurementType}.csv"
    #         if os.path.exists(filename):
    #             # If the file exists, append the new data
    #             df_existing = pd.read_csv(filename)
    #             df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    #             df_combined.to_csv(filename, index=False)
    #             print(f"Appended data to {filename}")
    #         else:
    #             # If the file does not exist, create a new one
    #             df_new.to_csv(filename, index=False)
    #             print(f"Created new file: {filename}")

# Loop through all files in the directory
files = sorted(os.listdir(directory_path))
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        process_kpiFiles(file_path)