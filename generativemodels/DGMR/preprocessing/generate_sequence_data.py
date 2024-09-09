import multiprocessing
import subprocess
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

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
        return (y_length, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        return (f"An error occurred while running generate_ids.py with y_length={y_length}: {e}", e.stdout, e.stderr)

def main():
    start_date = '2008-01-01 00:00'
    end_date = '2024-04-11 08:00'
    x_length = 4
    filter_no_rain = 'avg0.01mm'
    split_name = 'analysis_split_final'

    y_lengths = np.arange(10, 21, 2)

    num_cores = multiprocessing.cpu_count()
    max_workers = num_cores  # Set this to the number of CPU cores requested in SLURM job script

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_generate_ids, start_date, end_date, x_length, y_length, filter_no_rain, split_name): y_length for y_length in y_lengths}
        for future in tqdm(as_completed(futures), total=len(y_lengths), desc="Processing y_length values"):
            y_length, stdout, stderr = future.result()
            print(f"Results for y_length={y_length}:")
            print(stdout)
            print(stderr)

if __name__ == "__main__":
    main()
