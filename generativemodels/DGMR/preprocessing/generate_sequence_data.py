import subprocess

import numpy as np
from tqdm import tqdm

def run_generate_ids(start_date, end_date, x_length, y_length, filter_no_rain, split_name):
    args = [
        'python', 'create_split_ids.py',
        '--start_date', start_date,
        '--end_date', end_date,
        '--x_length', str(x_length),
        '--y_length', str(y_length),
        '--filter_no_rain', filter_no_rain,
        '--split_name', split_name,
        '--analysis'
    ]
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running generate_ids.py with y_length={y_length}: {e}")
        print(e.stdout)
        print(e.stderr)

def main():
    start_date = '2008-01-01 00:00'
    end_date = '2022-12-31 23:55'
    x_length = 4
    filter_no_rain = 'avg0.01mm'
    split_name = 'analysis_split'

    y_lengths = np.arange(10, 21, 2)

    for y_length in tqdm(y_lengths, desc="Processing y_length values"):
        run_generate_ids(start_date, end_date, x_length, y_length, filter_no_rain, split_name)

if __name__ == "__main__":
    main()
