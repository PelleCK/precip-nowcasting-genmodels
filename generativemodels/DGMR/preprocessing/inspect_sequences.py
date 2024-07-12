from collections import defaultdict
import os
import sys
sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR')

import matplotlib.pyplot as plt
import numpy as np

import config_DGMR

analysis_folder = os.path.join(config_DGMR.PROJECT_FOLDER, "data/analysis")

# Function to extract the year from a timestamp
def extract_year(timestamp):
    return timestamp[:4]

# Function to split the array by the starting year
def split_by_start_year(data):
    year_dict = defaultdict(list)
    for sequence in data:
        start_timestamp = sequence[0][0]
        start_year = extract_year(start_timestamp)
        year_dict[start_year].append(sequence)
    return year_dict

def n_sequences(data):
    return len(data)

# Collect all data for plotting
data_collection = {}

# Loop over files in analysis folder
for file in os.listdir(analysis_folder):
    if file.endswith(".npy"):
        seq_str = file.split('_')[4]
        seq_name = f'{seq_str[:1]} inputs, {seq_str[-3:-1]} outputs'
        print(seq_name)

        sequence_ids = np.load(os.path.join(analysis_folder, file), allow_pickle=True)
        yearly_data = split_by_start_year(sequence_ids)
        yearly_data = {year: np.array(sequences) for year, sequences in yearly_data.items()}

        data_collection[seq_name] = yearly_data

# Sort the data_collection keys for consistent ordering
sorted_keys = sorted(data_collection.keys(), key=lambda x: (int(x.split()[0]), int(x.split()[-2])))

# Consolidate all years for x-axis
all_years = sorted({year for data in data_collection.values() for year in data.keys()})

# Prepare data for grouped bar plot
bar_width = 0.15
index = np.arange(len(all_years))

fig, ax = plt.subplots(figsize=(14, 7))

# Colorblind-friendly color palette using the updated method
colormap = plt.colormaps['tab20c']

# Plot data for each sequence type
for i, seq_name in enumerate(sorted_keys):
    yearly_data = data_collection[seq_name]
    sequences_counts = [n_sequences(yearly_data.get(year, [])) for year in all_years]
    bar_position = index + i * bar_width
    ax.bar(bar_position, sequences_counts, bar_width, label=seq_name, color=colormap(i / len(sorted_keys)))

# Add labels, title, and legend
ax.set_xlabel('Year')
ax.set_ylabel('Number of sequences')
ax.set_title('Number of Sequences per Year for Different Sequence Lengths')
ax.set_xticks(index + bar_width * (len(sorted_keys) - 1) / 2)
ax.set_xticklabels(all_years)
ax.legend()

# Increase space between groups of bars (years)
ax.set_xlim([-0.5, len(all_years) - 0.5 + len(sorted_keys) * bar_width])

# Save and display the plot
plt.tight_layout()
plt.savefig(os.path.join(analysis_folder, "sequences_comparison.png"))
plt.show()

full_seq = np.load(os.path.join(analysis_folder, "list_IDs_200822_avg001mm_4x20y_analysis_split.npy"), allow_pickle=True)
full_seq_flat = full_seq.flatten()
full_seq_all_flat = np.array([timestamp for sequence in full_seq_flat for timestamp in sequence])

n_unique_frames = len(np.unique(full_seq_all_flat))

start_year = extract_year(full_seq_flat[0][0])
end_year = extract_year(full_seq_flat[-1][-1])

n_years = int(end_year) - int(start_year) + 1

# total amount of frames that could be present in the dataset
# 365 days * 24 hours * 12 5-minute intervals
total_possible_frames = n_years * 365 * 24 * 12

print(f"Unique frames used: {n_unique_frames}")
print(f"Total possible frames: {total_possible_frames}")
print(f"Percentage of frames used: {n_unique_frames / total_possible_frames * 100:.2f}%")
