import datetime
import os
import random
import sys

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pysteps
from matplotlib.colors import ListedColormap

sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR/')
import config_DGMR as config

# Define constants for the mask
DEFAULT_MASK_VALUE = 65535

def load_h5(path):
    try:
        with h5py.File(path, 'r') as f:
            radar_img = f['image1']['image_data'][:].astype(float)  # Ensure radar_img is float
            out_of_image = f['image1']['calibration'].attrs['calibration_out_of_image']
            mask_ooi = (radar_img == out_of_image)
            mask_first_pixel = (radar_img == radar_img[0][0])
            mask = np.logical_or(mask_ooi, mask_first_pixel)
            radar_img[mask] = np.nan
            return radar_img, mask, 'radar7' in f.keys()
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None, None, False

def load_image(ts, recent=False):
    path = os.path.join(config.dir_rtcor_recent, f'2023/{config.prefix_rtcor_recent}{ts}.h5')
    return load_h5(path), ts

def readable_date(ts):
    return datetime.datetime.strptime(ts, '%Y%m%d%H%M').strftime('%Y-%m-%d %H:%M')

def visualize_images(image_sets, filename):
    cmap, norm, _, _ = pysteps.visualization.precipfields.get_colormap('intensity', 'mm/h', 'pysteps')
    num_images = len(image_sets)
    num_rows = (num_images + 4) // 5  # Calculate the number of rows
    fig, axs = plt.subplots(num_rows, 5, figsize=(25, 5*num_rows))  # Adjust the figsize based on the number of rows
    axs = axs.flatten()  # Flatten the axs array to iterate over it easily

    for i, ((img, mask, _), ts) in enumerate(image_sets):
        axs[i].imshow(img, cmap=cmap, norm=norm)
        axs[i].imshow(mask, cmap='gray', alpha=0.3)
        axs[i].axis('off')
        axs[i].set_title(readable_date(ts))

    # Hide any remaining empty subplots
    for j in range(num_images, num_rows * 5):
        axs[j].axis('off')

    save_path = os.path.join('./figures', filename)
    plt.savefig(save_path)
    plt.show()

def visualize_combined_images(image_sets, old_mask, filename):
    cmap, norm, _, _ = pysteps.visualization.precipfields.get_colormap('intensity', 'mm/h', 'pysteps')
    num_images = len(image_sets)
    fig, axs = plt.subplots(num_images, 3, figsize=(15, 5*num_images))

    for i, ((img, mask, _), ts) in enumerate(image_sets):
        readable_ts = readable_date(ts)

        # Original mask
        axs[i, 0].imshow(img, cmap=cmap, norm=norm)
        axs[i, 0].imshow(mask, cmap='gray', alpha=0.3)
        axs[i, 0].axis('off')
        axs[i, 0].set_title(f"{readable_ts} Original Mask")

        # Combined mask
        combined_img = img.copy()
        combined_img[old_mask] = np.nan
        axs[i, 1].imshow(combined_img, cmap=cmap, norm=norm)
        axs[i, 1].imshow(old_mask, cmap='gray', alpha=0.3)
        axs[i, 1].axis('off')
        axs[i, 1].set_title(f"{readable_ts} Combined Mask")

        # Mask difference
        mask_diff = np.zeros_like(mask, dtype=int)
        mask_diff[mask] = 1
        mask_diff[old_mask] += 2
        cmap_diff = ListedColormap(['white', 'gray', 'blue', 'black'])
        axs[i, 2].imshow(mask_diff, cmap=cmap_diff, vmin=0, vmax=3)
        axs[i, 2].axis('off')
        axs[i, 2].set_title(f"{readable_ts} Mask Difference")

    save_path = os.path.join('./figures', filename)
    plt.savefig(save_path)
    plt.show()

def main():
    chosen_old_images = ['202301122040', '202301010055', '202301101655', '202301160930', '202301020155']
    chosen_new_images_radar7 = ['202312031515', '202310241140', '202312211545', '202310181945', '202311041645']
    chosen_new_images_no_radar7 = ['202307141555', '202303161310', '202305071310', '202302020040', '202304280720']

    # Load the chosen old images
    chosen_old_images_data = [load_image(ts, recent=False) for ts in chosen_old_images]

    # Visualize chosen old images
    visualize_images(chosen_old_images_data, 'chosen_old_images.png')

    # Load the chosen new images with radar7 and without radar7
    chosen_new_images_radar7_data = [load_image(ts, recent=True) for ts in chosen_new_images_radar7]
    chosen_new_images_no_radar7_data = [load_image(ts, recent=True) for ts in chosen_new_images_no_radar7]

    # Get the mask of the first chosen old image
    first_old_image_mask = chosen_old_images_data[0][0][1]

    # Visualize chosen new images with original and combined masks, and differences
    visualize_combined_images(chosen_new_images_radar7_data, first_old_image_mask, 'chosen_new_images_radar7_combined.png')
    visualize_combined_images(chosen_new_images_no_radar7_data, first_old_image_mask, 'chosen_new_images_no_radar7_combined.png')

if __name__ == "__main__":
    main()
