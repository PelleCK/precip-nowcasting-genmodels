import os
import config_DGMR
from batchcreator_DGMR import get_list_IDs
from datetime import datetime
import numpy as np
import tensorflow as tf

print(f"Create splitting sets with corresponding IDs")
physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(physical_devices))

start_dt = datetime(2018, 12, 19, 8, 0)
#start_dt = datetime(2006,1,1,0,0)
end_dt = datetime(2019, 12, 31, 23, 55)
#end_dt =  datetime(2021,12,31,0,0)
print(f"Start date: {start_dt}")
print(f"End date: {end_dt}")

x_length = 6
y_length = 1
filter_no_rain = 'avg0.01mm'
filename_npy = f'list_IDs{start_dt.year}{str(end_dt.year)[2:]}_avg001mm_train.npy'
filename = os.path.join(config_DGMR.path_code, f'data/{filename_npy}')

print(f"Retrieve IDs")

list_IDs = get_list_IDs(start_dt, end_dt, x_length, y_length, filter_no_rain=filter_no_rain)
print(f"Number of IDs: {len(list_IDs)}")
#print("Result of IDs:")
#print(list_IDs)
list_IDs = np.asarray(list_IDs, dtype='object')

np.save(filename, list_IDs)
print(f"Saved at location: {filename}")
#"""
