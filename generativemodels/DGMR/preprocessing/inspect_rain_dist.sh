#!/bin/bash
#SBATCH --job-name=rain_dist_analysis_variations
#SBATCH --account=cseduproject
#SBATCH --partition=csedu
#SBATCH --qos=csedu-large
#SBATCH --mem=2G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=17
#SBATCH --time=10:00:00
#SBATCH --output=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/%x-%j.out
#SBATCH --error=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/%x-%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=pelle.kools@ru.nl

source /vol/knmimo-nobackup/restore/knmimo/thesis_pelle/.dgmr_venv/bin/activate

declare -a arguments=(
    "--process-raw-data --statistic avg"
    "--process-raw-data --filter-clutter --statistic avg"
    "--process-raw-data --statistic peak"
    "--process-raw-data --filter-clutter --statistic peak"
    "--use-unique --statistic avg"
    "--statistic avg"
    "--use-unique --statistic peak"
    "--statistic peak"
)

for args in "${arguments[@]}"
do
    srun python inspect_rain_dist.py $args
done
