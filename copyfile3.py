import paramiko
import os
import re
from datetime import datetime

# List of radios with their connection details
radios = [
    {"server_ip": "10.1.1.2", "username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.101.2","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.16.12","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.16.31","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.16.32","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.30.2","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.35.2","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.36.10","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.5.2","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
    {"server_ip": "10.1.60.2","username": "toor4nsn", "password": "oZPS0POrRieRtu","remote_directory": "/ram/stats/iOms/"},
]

# Local directory where files will be saved
local_directory = r"C:\Userdata\proj2025\openkpi2\kpi_files"
os.makedirs(local_directory, exist_ok=True)

def adjust_file_name(original_name):
    """
    Adjust the file name to include the timestamp in HH:MM format.
    Example: "MT.BTS-414225.20250505.151500.LTE.raw" -> 15_15.LTE.raw
    """
    # Extract the timestamp using regex
    match = re.search(r"\.(\d{8}\.\d{6})\.", original_name)
    if match:
        timestamp_str = match.group(1)  # Example: 20250505.151500
        # Extract the time part (HHMMSS) and convert to HH:MM
        time_part = timestamp_str.split(".")[1]  # Example: 151500
        formatted_time = f"{time_part[:2]}_{time_part[2:4]}"  # Example: 15_15
        # Replace the timestamp in the file name with the formatted time
        new_name = original_name.replace(timestamp_str, formatted_time)
        return new_name
    return original_name  # Return the original name if no match is found

def download_and_rename_files(server_ip, username, password, remote_directory):
    try:
        # Establish SFTP connection
        transport = paramiko.Transport((server_ip, 22))
        transport.connect(username=username, password=password)

        # Create the SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the remote directory
        print(f"Connecting to server {server_ip}...")
        remote_files = sftp.listdir(remote_directory)

        for file_name in remote_files:
            # Check if the file matches the quarterly KPI naming pattern
            if file_name.startswith("PM.BTS") and file_name.endswith(".raw"):
                # Adjust the file name
                new_file_name = adjust_file_name(file_name)

                # Define remote and local file paths
                remote_file_path = os.path.join(remote_directory, file_name)
                local_file_path = os.path.join(local_directory, f"{server_ip}_{new_file_name}")

                # Download the file with the new name
                print(f"Downloading {file_name} as {new_file_name}...")
                sftp.get(remote_file_path, local_file_path)
                print(f"File {new_file_name} downloaded successfully.")

        # Close the SFTP connection
        sftp.close()
        transport.close()
        print(f"All files from {server_ip} processed successfully.\n")

    except Exception as e:
        print(f"Error during file transfer from {server_ip}: {e}")

# Iterate through all radios and download files
for radio in radios:
    download_and_rename_files(
        server_ip=radio["server_ip"],
        username=radio["username"],
        password=radio["password"],
        remote_directory=radio["remote_directory"]
    )