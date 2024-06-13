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
    start_year = file_name[27:31]
    end_year = file_name[43:47]

    # Create a directory for the year if it doesn't exist
    start_year_dir = root_data_dir / start_year
    start_year_dir.mkdir(exist_ok=True)

    # Extract the tar file into its corresponding year directory
    extract_tar_file(tar_file, start_year_dir)

    # check if end year is diff from start year
    if start_year != end_year:
        end_year_dir = root_data_dir / end_year
        end_year_dir.mkdir(exist_ok=True)
        files = sorted(start_year_dir.glob('*.h5'), reverse=True)

        # move files with end year to end year directory
        for file in files:
            if f'_{end_year}' in file.name:
                os.rename(file, end_year_dir / file.name)
            else:
                break


print("Data extraction complete.")
