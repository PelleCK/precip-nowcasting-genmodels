import argparse
import multiprocessing
import os
import sys
import pickle
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

import h5py
import matplotlib.pyplot as plt
import numpy as np

# Add path to DGMR and import configuration and clutter-checking function
sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR')
import config_DGMR

# Load 'default' mask from older image to filter out 'radar7' data in newer images
default_mask_path = os.path.join(
    config_DGMR.dir_rtcor_recent,
    f'2019/{config_DGMR.prefix_rtcor_recent}201901010000.h5'.strip('/')
)
with h5py.File(default_mask_path, 'r') as f:
    rain = f['image1']['image_data'][:]
    DEFAULT_OLD_MASK = (rain == 65535)

# -------------------- Data Loading and Preprocessing --------------------

def collect_all_raw_data(data_dir):
    """Collect all raw data timestamps from the specified directory."""
    data = []
    for year in os.listdir(data_dir):
        year_path = os.path.join(data_dir, year)
        for filename in os.listdir(year_path):
            if filename.endswith('.h5'):
                timestamp = filename.split('_')[-1].split('.')[0]
                data.append(timestamp)
    return data


def split_by_year(data):
    """Split data by year for parallel processing."""
    # use defaultdict for automatic key creation
    year_dict = defaultdict(list)
    for timestamp in data:
        year = timestamp[:4]
        year_dict[year].append(timestamp)
    return year_dict


def load_h5_and_mask(ts):
    """Load the .h5 file and return radar image and mask."""
    year = ts[:4]
    if int(year) < 2019:
        data_dir = config_DGMR.dir_rtcor
        prefix = config_DGMR.prefix_rtcor_archive
    else:
        data_dir = config_DGMR.dir_rtcor_recent
        prefix = config_DGMR.prefix_rtcor_recent
    path = os.path.join(data_dir, f'{year}/{prefix}{ts}.h5')

    radar_img = None
    mask = None
    with h5py.File(path, 'r') as f:
        try:
            radar_img = f['image1']['image_data'][:]
            out_of_image = f['image1']['calibration'].attrs[
                'calibration_out_of_image'
            ]
            mask_ooi = (radar_img == out_of_image)
            mask_first_pixel = (radar_img == radar_img[0][0])

            # use both masks to filter out pixels out of image
            mask = np.logical_or(mask_ooi, mask_first_pixel)

            # If 'radar7' in data, also apply default mask to filter out 'radar7' data
            if 'radar7' in f.keys():
                mask = np.logical_or(mask, DEFAULT_OLD_MASK)

            radar_img[mask] = 0  # Set masked pixels to zero
            mask = (radar_img == 0)  # Only include pixels with precipitation in statistic calculation

            radar_img = np.clip((radar_img / 100) * 12, 0, 100)
        except Exception as e:
            print(f"Error loading file {path}: {e}")
            radar_img, mask = None, None
    return radar_img, mask


# couldn't import from heavy_rain_labeler.py, so added it here
def has_clutter(rdr):
    # Calculate gradien magnitudes
    gx, gy = np.gradient(rdr)
    grad = np.hypot(gx, gy)
    # Pixel is seen as abnormal if gradient is higher than 30
    abnormal_pixels = np.sum(grad > 30)
    # Image is discared if it has more than 50 abnormal pixels
    return abnormal_pixels > 50


def load_and_validate_data(ts, filter_clutter):
    """Load radar data and validate it, applying clutter filtering if needed."""
    rdr, mask = load_h5_and_mask(ts)
    if rdr is None or mask is None:
        return None, None
    
    # Discard cluttered data if needed
    if filter_clutter and has_clutter(rdr):
        return None, None  
    
    return rdr, mask

# -------------------- Calculating Statistic and Categorizating to Bins --------------------

def avg_rainfall(rdr, mask):
    """Calculate the average rainfall from the radar image."""
    nr_unmasked_pixels = np.sum(~mask)
    if nr_unmasked_pixels == 0:
        return np.nan  # Avoid division by zero if no unmasked pixels
    return np.sum(rdr) / nr_unmasked_pixels


def peak_rainfall(rdr):
    """Calculate the peak rainfall intensity from the radar image."""
    return np.max(rdr)


def get_rainfall_statistic(rdr, mask, statistic):
    """Calculate the rainfall statistic (avg or peak) based on the input."""
    if statistic == 'avg':
        return avg_rainfall(rdr, mask)
    elif statistic == 'peak':
        return peak_rainfall(rdr)
    else:
        raise ValueError(f"Invalid statistic: {statistic}")


def categorize_rainfall(ts, statistic, bins, filter_clutter):
    """Categorize the rainfall data into the given bins."""
    rdr, mask = load_and_validate_data(ts, filter_clutter)
    if rdr is None or mask is None:
        return len(bins)  # Invalid data, return an out-of-range value
    
    rain_statistic = get_rainfall_statistic(rdr, mask, statistic)
    if rain_statistic is None or np.isnan(rain_statistic):
        return len(bins)  # Handle invalid or NaN values
    
    for i, (lower, upper) in enumerate(bins):
        if lower < rain_statistic <= upper:
            return i

    return len(bins)  # No matching bin found

# -------------------- Parallel Processing and Distribution Calculation --------------------

def calculate_rain_distribution_for_year(year, timestamps, statistic, filter_clutter):
    """Calculate the rain distribution for a single year."""
    print(f"Calculating rain distribution for year {year}...")
    bins = [(0, 0.01), (0.01, 1.0), (1.0, 5.0), (5.0, 10.0), (10.0, 20.0), (20.0, np.inf)]
    bin_labels = ['no rain', 'low', 'moderate', 'moderate-high', 'high', 'very high']
    
    rain_distribution = np.array([
        category for ts in timestamps
        if (category := categorize_rainfall(ts, statistic, bins, filter_clutter)) < len(bin_labels)
    ])
    
    # Count occurrences in each bin
    rain_dist_dict = {key: 0 for key in bin_labels}
    for i, label in enumerate(bin_labels):
        rain_dist_dict[label] = np.sum(rain_distribution == i)
    return year, rain_dist_dict


def calculate_rain_distributions(data, statistic, filter_clutter, rain_distributions_path):
    """Calculate or load rain distributions across multiple years."""
    if os.path.exists(rain_distributions_path):
        print("Loading existing rain distributions...")
        with open(rain_distributions_path, 'rb') as f:
            return pickle.load(f)

    print("Splitting data by year...")
    yearly_data = split_by_year(data)

    print("Calculating rain distributions in parallel...")
    rain_distributions = {}
    num_cores = multiprocessing.cpu_count()
    
    # Parallel processing of rain distribution calculations
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = {
            executor.submit(
                calculate_rain_distribution_for_year, year, timestamps, statistic, filter_clutter
            ): year for year, timestamps in yearly_data.items()
        }
        for future in as_completed(futures):
            year, rain_dist_dict = future.result()
            rain_distributions[year] = rain_dist_dict

    print("Saving rain distributions...")
    with open(rain_distributions_path, 'wb') as f:
        pickle.dump(rain_distributions, f)
    
    return rain_distributions

# -------------------- Visualization --------------------

def plot_rain_distributions(rain_distributions, data_type, statistic):
    """Plot and save rain distributions per year."""
    years = sorted(rain_distributions.keys())
    labels = ['no rain', 'low', 'moderate', 'moderate-high', 'high', 'very high']
    
    bar_width = 0.35
    index = np.arange(len(years))

    fig, ax = plt.subplots(figsize=(14, 7))
    colormap = plt.get_cmap('tab20c')
    colors = [colormap(i / len(labels)) for i in range(len(labels))]
    
    bottoms = np.zeros(len(years))

    for i, label in enumerate(labels):
        rain_counts = [rain_distributions[year][label] for year in years]
        ax.bar(index, rain_counts, bar_width, bottom=bottoms, label=label, color=colors[i])
        bottoms += np.array(rain_counts)

    rainfall_type = "Peak" if statistic == 'peak' else "Average"
    data_desc = {
        'all_raw': 'All Raw Data, No Clutter Filtering',
        'all_raw_no_clutter': 'Raw Data, Clutter Filtered',
        'sequences_unique': 'Sequence Data, Unique Frames',
        'sequences_nonunique': 'Sequence Data, All, Non-Unique Frames'
    }.get(data_type, 'Unknown Data Type')
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Frames')
    ax.set_title(f'Rain Distribution per Year ({data_desc}, {rainfall_type} Rainfall)')
    ax.set_xticks(index)
    ax.set_xticklabels(years, rotation=45)
    ax.legend(title='Rain Intensity')

    plt.tight_layout()
    plt.savefig(os.path.join(config_DGMR.PROJECT_FOLDER,
                             f'data/analysis/images/rain_distributions_{data_type}_{statistic}.png'))
    plt.show()


def get_data_and_type(data_dir, process_raw_data, use_unique, filter_clutter, split_path):
    """
    Get the appropriate data and its type based on input flags.
    data type is used for saving/loading rain distributions and plotting.
    """
    if process_raw_data:
        print("Collecting all raw data timestamps...")
        data = collect_all_raw_data(data_dir)
        data_type = 'all_raw'
        if filter_clutter:
            data_type += '_no_clutter'
    else:
        print("Loading split data...")
        data = np.load(split_path, allow_pickle=True)
        data = [ts for seq in data.flatten() for ts in seq]
        if use_unique:
            data = np.unique(data)
            data_type = 'sequences_unique'
        else:
            data_type = 'sequences_nonunique'
    return data, data_type


def main(process_raw_data, use_unique, statistic, filter_clutter):
    raw_data_dir = config_DGMR.dir_rtcor
    analysis_folder = os.path.join(config_DGMR.PROJECT_FOLDER, "data/analysis")
    splits_folder = os.path.join(analysis_folder, "splits")
    
    split_fn = 'list_IDs_200824_avg001mm_4x20y_analysis_split_final.npy'
    split_path = os.path.join(splits_folder, split_fn)

    data, data_type = get_data_and_type(raw_data_dir, process_raw_data, use_unique,
                                        filter_clutter, split_path)

    dists_folder = os.path.join(analysis_folder, "rain_dist_data")
    rain_distributions_path = os.path.join(dists_folder,
                                           f'rain_distributions_{data_type}_{statistic}.pkl')
    
    rain_distributions = calculate_rain_distributions(data, statistic, filter_clutter,
                                                      rain_distributions_path)
    
    plot_rain_distributions(rain_distributions, data_type, statistic)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and analyze rainfall data.")
    
    parser.add_argument('statistic', choices=['avg', 'peak'],
                        help="Statistic to use: 'avg' (average rainfall) or 'peak' "
                             "(peak rainfall intensity).")
    parser.add_argument('--process-raw-data', action='store_true',
                        help="Process raw data instead of sequence data.")
    parser.add_argument('--use-unique', action='store_true',
                        help="Use unique timestamps when processing sequence data.")
    parser.add_argument('--filter-clutter', action='store_true',
                        help="Filter out cluttered images (only applicable with raw data).")

    args = parser.parse_args()

    # Argument validation
    if args.filter_clutter and not args.process_raw_data:
        parser.error("--filter-clutter can only be used with --process-raw-data.")
    if args.use_unique and args.process_raw_data:
        parser.error("--use-unique can only be used with sequence data.")

    main(args.process_raw_data, args.use_unique, args.statistic, args.filter_clutter)
