import os
import sys

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pysteps

sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR/')
import config_DGMR as config
import random
import datetime

rtcor_dir_recent = '/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/rtcor-recent'

date = datetime.datetime(2023, 2, 1, 0, 0)
date_str = date.strftime('%Y%m%d%H%M')
path = os.path.join(rtcor_dir_recent, '2023/{}{}.h5'.format(config.prefix_rtcor_recent, date_str))
with h5py.File(path, 'r') as f:
    image_data = f['image1']['image_data'][:].astype(float)
    DEFAULT_MASK = ~(image_data == 65535)

def process_image_data(image_path):
    with h5py.File(image_path, 'r') as f:                
        # print(f.keys())

        image_data = f['image1']['image_data'][:].astype(float)
        mask = ~(image_data == 65535)
        
        print('unmasked pixels before: ', np.sum(mask))
        if 'radar7' in f.keys():
            print('RADAR7 FOUND')
            mask = np.logical_and(mask, DEFAULT_MASK)
            print('unmasked pixels after: ', np.sum(mask))
        image_data = np.nan_to_num(image_data)
        image_data[~mask] = np.nan
        # print('total unmasked pixels after mask: ', np.sum(~np.isnan(image_data)))
        return image_data

def visualize_images(old_files, new_files):
    cmap, norm, _, _ = pysteps.visualization.precipfields.get_colormap('intensity', 'mm/h', 'pysteps')

    num_old_images = len(old_files)
    num_new_images = len(new_files)

    fig, axs = plt.subplots(2, max(num_old_images, num_new_images), figsize=(5*(num_old_images + num_new_images), 10))

    print('old files:')
    for i, fn in enumerate(old_files):
        old_img_path = os.path.join(rtcor_dir_recent, '2023/{}{}.h5'.format(config.prefix_rtcor_recent, fn))
        img = process_image_data(old_img_path)
        axs[0, i].imshow(img, cmap=cmap, norm=norm)
        axs[0, i].axis('off')
        axs[0, i].set_title(f'Old Image {fn}')

    print('\nnew files:')
    for i, fn in enumerate(new_files):
        new_img_path = os.path.join(rtcor_dir_recent, '2023/{}{}.h5'.format(config.prefix_rtcor_recent, fn))
        img = process_image_data(new_img_path)
        axs[1, i].imshow(img, cmap=cmap, norm=norm)
        axs[1, i].axis('off')
        axs[1, i].set_title(f'New Image {fn}')

    fig.suptitle('Comparison of images')
    fig.tight_layout()
    plt.savefig('comparison_images.png')

# automatically pick random timestamp strings between '202301010000' and '202301312355' for old_files
old_files = []

start_date = datetime.datetime(2023, 1, 1, 0, 0)
end_date = datetime.datetime(2023, 1, 30, 23, 55)
time_delta = datetime.timedelta(minutes=5)

num_files = 10  # Specify the number of files you want to randomly choose

for _ in range(num_files):
    random_minutes = random.randint(0, int((end_date - start_date).total_seconds() / 60))
    random_minutes = random_minutes // 5 * 5  # Round down to the nearest multiple of 5
    random_date = start_date + datetime.timedelta(minutes=random_minutes)
    old_files.append(random_date.strftime('%Y%m%d%H%M'))

# automatically pick random timestamp strings between '202302010000' and '202312312355' for new_files
new_files = []

start_date = datetime.datetime(2023, 2, 1, 0, 0)
end_date = datetime.datetime(2023, 12, 31, 23, 55)
time_delta = datetime.timedelta(minutes=5)

num_files = 10  # Specify the number of files you want to randomly choose

for _ in range(num_files):
    random_minutes = random.randint(0, int((end_date - start_date).total_seconds() / 60))
    random_minutes = random_minutes // 5 * 5  # Round down to the nearest multiple of 5
    random_date = start_date + datetime.timedelta(minutes=random_minutes)
    new_files.append(random_date.strftime('%Y%m%d%H%M'))


# old_images = []
# new_images = []

# for file_name in old_files:
#     old_img_path = os.path.join(rtcor_dir_recent, '2023/{}{}.h5'.format(config.prefix_rtcor_recent, file_name))
#     old_images.append(process_image_data(old_img_path))

# for file_name in new_files:
#     new_img_path = os.path.join(rtcor_dir_recent, '2023/{}{}.h5'.format(config.prefix_rtcor_recent, file_name))
#     new_images.append(process_image_data(new_img_path))

visualize_images(old_files, new_files)
