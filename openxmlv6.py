import os
import xml.etree.ElementTree as ET
import psycopg2

"""
docker run --name kpidatabase -e POSTGRES_USER=Solis -e POSTGRES_PASSWORD=Solis2025 -e POSTGRES_DB=kpidata -p 5434:5432 -d postgres:11
"""

# Directory containing KPI files
directory_path = "/var/openkpi/kpi_files"

# PostgreSQL connection details
db_config = {
    "dbname": "kpidata",
    "user": "Solis",
    "password": "Solis2025",
    "host": "localhost",
    "port": 5434
}

# Function to create a table for a measurementType if it doesn't exist
def create_table_if_not_exists(measurementType, kpi_columns):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Create table query with dynamic columns for kpiValues
        columns = ", ".join([f'"{col}" INTEGER' for col in kpi_columns])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{measurementType}" (
            id SERIAL PRIMARY KEY,
            create_at TIMESTAMP,
            manage_object TEXT,
            {columns}
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Table '{measurementType}' is ready.")
    except Exception as e:
        print(f"Error creating table '{measurementType}': {e}")

# Function to insert data into the corresponding table
def insert_into_table(measurementType, data, kpi_columns):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data query with dynamic columns
        columns = ", ".join([f'"{col}"' for col in kpi_columns])
        placeholders = ", ".join(["%s"] * (len(kpi_columns) + 2))  # +2 for create_at and manage_object
        insert_query = f"""
        INSERT INTO "{measurementType}" (create_at, manage_object, {columns})
        VALUES ({placeholders})
        """
        cursor.executemany(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Inserted {len(data)} rows into table '{measurementType}'.")
    except Exception as e:
        print(f"Error inserting data into table '{measurementType}': {e}")

# Function to process KPI files
def process_kpiFiles(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    print(file_path)
    
    # Iterate through the XML tree and extract the desired data
    for PMSetup in root.iter('PMSetup'):
        # Extract common fields for the row
        createAt = PMSetup.attrib.get('startTime')

        for PMMOResult in PMSetup.iter('PMMOResult'):
            manageObject = None
            measurementType = None
            kpi_columns = set()  # To track all kpiNames for this measurementType
            data_rows = []  # To store rows for insertion

            for child in PMMOResult:
                if child.tag == 'MO':
                    for subchild in child:
                        if subchild.tag == 'baseId':
                            manageObject = subchild.text
                elif child.tag == 'NE-WBTS_1.0':
                    measurementType = child.attrib.get('measurementType')

                    # Create a dictionary to store KPI values for this row
                    row = {
                        'createAt': createAt,
                        'manageObject': manageObject
                    }

                    # Add KPI values as columns dynamically
                    has_kpi_value = False  # Track if there is any kpiValue > 0
                    for subchild in child:
                        if int(subchild.text) > 0 or int(subchild.text) < 0:
                            if subchild.tag != 'measurementType':  # Exclude non-KPI tags
                                row[subchild.tag] = int(subchild.text)
                                kpi_columns.add(subchild.tag)
                                has_kpi_value = True


                    # Prepare the row for insertion
                    if has_kpi_value:
                        data_rows.append(row)

            # Ensure the table for this measurementType exists
            if measurementType and kpi_columns:
                create_table_if_not_exists(measurementType, kpi_columns)

                # Prepare data for insertion
                kpi_columns = sorted(kpi_columns)  # Ensure consistent column order
                data_to_insert = []
                for row in data_rows:
                    data_to_insert.append([
                        row.get('createAt'),
                        row.get('manageObject'),
                        *[row.get(col, None) for col in kpi_columns]
                    ])

                # Insert data into the corresponding table
                insert_into_table(measurementType, data_to_insert, kpi_columns)

# Loop through all files in the directory
files = sorted(os.listdir(directory_path))
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        process_kpiFiles(file_path)