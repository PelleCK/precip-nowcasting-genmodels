import os
import tarfile
import config_DGMR as config
from pathlib import Path


# Set the root data directory
root_data_dir = config.dir_rtcor

# Function to extract tar files into the specified directory
def extract_tar_file(tar_path, extract_to):
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=extract_to)

# Iterate over all files in the root data directory
for tar_file in root_data_dir.glob('*.tar'):
    # Extract the year from the file name
    file_name = tar_file.name
    year = file_name[27:31]  # Adjust indices according to your file name structure

    # Create a directory for the year if it doesn't exist
    year_dir = root_data_dir / year
    year_dir.mkdir(exist_ok=True)

    # Extract the tar file into its corresponding year directory
    extract_tar_file(tar_file, year_dir)

print("Data extraction complete.")
