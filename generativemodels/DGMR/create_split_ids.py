import os
import config_DGMR
from batchcreator_DGMR import get_list_IDs
from datetime import datetime
import numpy as np
import tensorflow as tf
import argparse

def main(start_date, end_date, x_length, y_length, filter_no_rain, given_filename, analysis=False):
    print(f"Create splitting sets with corresponding IDs")
    # physical_devices = tf.config.list_physical_devices('GPU')
    # print("Num GPUs Available: ", len(physical_devices))

    start_dt = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
    print(f"Start date: {start_dt}")
    print(f"End date: {end_dt}")

    filename_npy = f'list_IDs_{start_dt.year}{str(end_dt.year)[2:]}_{filter_no_rain.replace(".", "")}_{x_length}x{y_length}y_{given_filename}.npy'

    if analysis:
        filename = os.path.join(config_DGMR.path_code, f'data/analysis/{filename_npy}')
    else:
        filename = os.path.join(config_DGMR.path_code, f'data/{filename_npy}')

    print(f"Retrieve IDs")

    list_IDs = get_list_IDs(start_dt, end_dt, x_length, y_length, filter_no_rain=filter_no_rain)
    print(f"Number of IDs: {len(list_IDs)}")
    #print("Result of IDs:")
    #print(list_IDs)
    list_IDs = np.asarray(list_IDs, dtype='object')

    np.save(filename, list_IDs)
    print(f"Saved at location: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate and save list IDs')
    parser.add_argument('--start_date', type=str, required=True, help='Start date in format YYYY-MM-DD HH:MM')
    parser.add_argument('--end_date', type=str, required=True, help='End date in format YYYY-MM-DD HH:MM')
    parser.add_argument('--x_length', type=int, required=True, help='X length')
    parser.add_argument('--y_length', type=int, required=True, help='Y length')
    parser.add_argument('--filter_no_rain', type=str, required=True, help='Filter no rain')
    parser.add_argument('--split_name', type=str, required=True, help='Name of split (added to filename)')
    parser.add_argument('--analysis', action='store_true', help='Store file in analysis path if set')

    args = parser.parse_args()
    main(args.start_date, args.end_date, args.x_length, args.y_length, args.filter_no_rain, args.split_name, args.analysis)
