#!/bin/bash
#SBATCH --account=cseduproject
#SBATCH --partition=csedu
#SBATCH --qos=csedu-large
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem=4G
#SBATCH --job-name=labeling_2020_2022
#SBATCH --output=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/labeling_%A_%a.out
#SBATCH --error=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/labeling_%A_%a.err
#SBATCH --array=0-3
#SBATCH --mail-type=ALL
#SBATCH --mail-user=pelle.kools@ru.nl

year=$((2019 + SLURM_ARRAY_TASK_ID))

python ./preprocessing/heavy_rain_labeler.py $year