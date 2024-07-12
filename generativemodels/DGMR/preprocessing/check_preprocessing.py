import os
import sys
# sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/')
# sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR/preprocessing')
sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR/')

import matplotlib.pyplot as plt
import numpy as np
import pysteps
import h5py

# from preprocessing_rtcor import *
import config_DGMR
from batchcreator_DGMR import undo_prep

import datetime

def generate_timestamps(start_ts, steps, increment_minutes):
    # Convert the integer timestamp to a string and then to a datetime object
    start_ts_str = str(start_ts)
    start_dt = datetime.datetime.strptime(start_ts_str, '%Y%m%d%H%M')
    
    timestamps = []
    
    for step in range(steps):
        # Increment the datetime object by the specified number of minutes
        new_dt = start_dt + datetime.timedelta(minutes=increment_minutes * step)
        # Format back to the required integer format
        new_ts_str = new_dt.strftime('%Y%m%d%H%M')
        new_ts_int = int(new_ts_str)
        timestamps.append(f"{new_ts_int:012}.npy")
    
    return timestamps

prep_dir = config_DGMR.dir_rtcor_prep
# fns = ["202002162000.npy", "202002162030.npy", "202002162100.npy"]
# fns = ["202006271600.npy", "202006271630.npy", "202006271700.npy"]
# fns = ["202002161900.npy", "202002161930.npy", "202002162000.npy"]

# ts = 202006050930
# fns = generate_timestamps(ts, 12, 5)
# fns = ['202008202230.npy', '202008210000.npy', '202008210030.npy', '202008210100.npy', '202008210200.npy', '202008210500.npy']

fns = ['202105011105.npy'] # 1105:00 LT 1 May 2021

cmap, norm, _, _ = pysteps.visualization.precipfields.get_colormap('intensity', 'mm/h', 'pysteps')

path = os.path.join(config_DGMR.dir_rtcor_recent, '2019/{}201901010000.h5'.format(config_DGMR.prefix_rtcor_recent))
with h5py.File(path, 'r') as f:
    rain = f['image1']['image_data'][:]
    mask = ~(rain == 65535)

imgs_prepped = [] # [np.load(os.path.join(prep_dir, fn)) for fn in fns]
for fn in fns:
    try:
        img = np.load(os.path.join(prep_dir, fn))
        imgs_prepped.append(img)
    except FileNotFoundError:
        print(f"File {fn} not found.")

imgs_prepped = np.stack(imgs_prepped, axis=0)
print(imgs_prepped.shape)

imgs_unprepped = undo_prep(imgs_prepped)

fig, axs = plt.subplots(1, len(fns), figsize=(12, 4))

for i, (fn, img) in enumerate(zip(fns, imgs_unprepped)):
    rdr_example = np.nan_to_num(img)
    rdr_example[~mask] = np.nan
    axs[i].imshow(rdr_example, cmap=cmap, norm=norm)
    axs[i].axis('off')
    axs[i].set_title(fn.split('.')[0])

plt.tight_layout()
plt.savefig(os.path.join(config_DGMR.PROJECT_FOLDER, f"figures/subplots_{fns[0].split('.')[0]}.png"))
plt.show()