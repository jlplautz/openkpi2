import paramiko
import os
import re
import pytz
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

def get_current_quarter():
    """
    Determine the current quarter of the hour (e.g., 15:00, 15:15, 15:30, 15:45).
    """
    utc = pytz.utc
    now = datetime.now(utc)
    minute = now.minute
    if 0 <= minute < 15:
        return f"{now.hour:02d}:00"
    elif 15 <= minute < 30:
        return f"{now.hour:02d}:15"
    elif 30 <= minute < 45:
        return f"{now.hour:02d}:30"
    else:
        return f"{now.hour:02d}:45"

def adjust_file_name(original_name):
    """
    Adjust the file name to change the extension from .raw to .xml.
    Example: "PM.BTS-414225.20250505.151500.LTE.raw" -> "PM.BTS-414225.20250505.151500.xml"
    """
    # Extract the timestamp using regex
    # match = re.search(r"\.(\d{8}\.\d{6})\.", original_name)
    if original_name.endswith(".LTE.raw"):
        new_name = original_name.replace(".LTE.raw", ".xml")
        return new_name, None  # Return the new name and None for the quarter
    return original_name, None  # Return the original name if no match is found

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

        # Get the current quarter
        current_quarter = get_current_quarter()
        print(f"Current quarter: {current_quarter}")

        for file_name in remote_files:
            # Check if the file matches the quarterly KPI naming pattern
            if file_name.startswith("PM.BTS") and file_name.endswith(".LTE.raw"):
                # Adjust the file name and extract the timestamp
                new_file_name = adjust_file_name(file_name)

                # Skip files without a valid timestamp
                #if not file_quarter:
                #    continue

                # Skip files not in the current quarter
                # if file_quarter != current_quarter:
                #    print(f"Skipping {file_name} (not in {current_quarter})")
                #    continue

                # Define remote and local file paths
                remote_file_path = os.path.join(remote_directory, file_name)
                print(remote_file_path)
                local_file_path = os.path.join(local_directory, new_file_name)
                print(local_file_path)

                # Check if the file already exists locally
                if os.path.exists(local_file_path):
                    print(f"File {new_file_name} already exists locally. Skipping download.")
                    continue

                # Download the file with the new name
                print(f"Downloading {file_name} as {new_file_name}...")
                sftp.get(remote_file_path, local_file_path)
                print(f"File {file_name} downloaded successfully.")

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