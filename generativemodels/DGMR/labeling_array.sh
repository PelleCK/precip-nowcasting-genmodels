#!/bin/bash
#SBATCH --account=cseduproject
#SBATCH --partition=csedu
#SBATCH --qos=csedu-large
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem=4G
#SBATCH --job-name=labeling_202324_fixed_loading
#SBATCH --output=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/labeling_fixed_loading_%A_%a.out
#SBATCH --error=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/labeling_fixed_loading_%A_%a.err
#SBATCH --array=0-1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=pelle.kools@ru.nl

year=$((2023 + SLURM_ARRAY_TASK_ID))

python ./preprocessing/heavy_rain_labeler.py $year