import os
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR')
import config_DGMR


def split_by_start_year(data):
    """Split the array by the starting year."""
    year_dict = defaultdict(list)
    for sequence in data:
        start_timestamp = sequence[0][0]
        start_year = start_timestamp[:4]
        year_dict[start_year].append(sequence)
    return year_dict

def collect_data(splits_folder, start_year=2008, end_year=2024):
    """Collect all data for plotting."""
    years_str = str(start_year) + str(end_year)[2:]

    data_collection = {}
    for file in os.listdir(splits_folder):
        if years_str in file and file.endswith("split_final.npy"):
            seq_str = file.split('_')[4]
            seq_name = f'{seq_str[:1]} inputs, {seq_str[-3:-1]} outputs'
            print(seq_name)

            sequence_ids = np.load(os.path.join(splits_folder, file), allow_pickle=True)
            yearly_data = split_by_start_year(sequence_ids)
            yearly_data = {year: np.array(sequences) for year, sequences in yearly_data.items()}

            data_collection[seq_name] = yearly_data
    return data_collection

def plot_data(data_collection, images_folder):
    """Plot the collected data."""
    sorted_keys = sorted(data_collection.keys(), key=lambda x: (int(x.split()[0]), int(x.split()[-2])))
    all_years = sorted({year for data in data_collection.values() for year in data.keys()})

    bar_width = 0.15
    index = np.arange(len(all_years))
    fig, ax = plt.subplots(figsize=(14, 7))

    colormap = plt.colormaps['tab20c']

    for i, seq_name in enumerate(sorted_keys):
        yearly_data = data_collection[seq_name]
        sequences_counts = [len(yearly_data.get(year, [])) for year in all_years]
        bar_position = index + i * bar_width
        ax.bar(bar_position, sequences_counts, bar_width, label=seq_name, color=colormap(i / len(sorted_keys)))

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of sequences')
    ax.set_title('Number of Sequences per Year for Different Sequence Lengths')
    ax.set_xticks(index + bar_width * (len(sorted_keys) - 1) / 2)
    ax.set_xticklabels(all_years)
    ax.legend()
    ax.set_xlim([-0.5, len(all_years) - 0.5 + len(sorted_keys) * bar_width])

    plt.tight_layout()
    plt.savefig(os.path.join(images_folder, "sequences_comparison_final.png"))
    plt.show()

def analyze_full_sequence(analysis_folder):
    #TODO: specify the file to analyze (fixed mask)
    full_seq = np.load(os.path.join(analysis_folder, "list_IDs_200824_avg001mm_4x20y_analysis_split_final.npy"), allow_pickle=True)
    full_seq_flat = full_seq.flatten()
    full_seq_all_flat = np.array([timestamp for sequence in full_seq_flat for timestamp in sequence])

    n_unique_frames = len(np.unique(full_seq_all_flat))
    # extract start and end year from the timestamps of the first and last frame
    start_year = full_seq_flat[0][0][:4]
    end_year = full_seq_flat[-1][-1][:4]
    n_years = int(end_year) - int(start_year) + 1

    total_possible_frames = n_years * 365 * 24 * 12

    print(f"Unique frames used: {n_unique_frames}")
    print(f"Total possible frames: {total_possible_frames}")
    print(f"Percentage of frames used: {n_unique_frames / total_possible_frames * 100:.2f}%")

def main():
    analysis_folder = os.path.join(config_DGMR.PROJECT_FOLDER, "data/analysis/")
    splits_folder = os.path.join(analysis_folder, "splits/")
    images_folder = os.path.join(analysis_folder, "images/")

    data_collection = collect_data(splits_folder)
    plot_data(data_collection, images_folder)
    # analyze_full_sequence(analysis_folder)

if __name__ == "__main__":
    main()
