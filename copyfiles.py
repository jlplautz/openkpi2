import paramiko
import os
import schedule
import time
from datetime import datetime

# Server details
server_ip = "10.1.101.2"
username = "toor4nsn"
password = "oZPS0POrRieRtu"

# Remote directory containing KPI files
remote_directory = "/ram/stats/iOms/"

# Local directory where files will be saved
local_directory = r'C:\Userdata\proj2025\openkpi2\kpi_files'
os.makedirs(local_directory, exist_ok=True)

def download_kpi_files():
    try:
        # Establish SFTP connection
        transport = paramiko.Transport((server_ip, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the remote directory
        print(f"[{datetime.now()}] Connecting to server {server_ip}...")
        remote_files = sftp.listdir(remote_directory)

        for file_name in remote_files:
            # Define remote and local file paths
            remote_file_path = os.path.join(remote_directory, file_name)
            local_file_path = os.path.join(local_directory, file_name)

            # Check if the file already exists locally
            if not os.path.exists(local_file_path):
                print(f"Downloading {file_name}...")
                sftp.get(remote_file_path, local_file_path)
                print(f"File {file_name} downloaded successfully.")
            else:
                print(f"File {file_name} already exists. Skipping download.")

        # Close the SFTP connection
        sftp.close()
        transport.close()
        print(f"[{datetime.now()}] All files processed successfully.\n")

    except Exception as e:
        print(f"Error during file transfer: {e}")

# Schedule the task to run every 15 minutes
schedule.every(15).minutes.do(download_kpi_files)

print("KPI file downloader is running. Press Ctrl+C to stop.")
download_kpi_files()  # Run immediately on startup

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)