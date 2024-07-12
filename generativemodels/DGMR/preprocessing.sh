#!/bin/bash
#SBATCH --account=cseduproject
#SBATCH --partition=csedu
#SBATCH --qos=csedu-large
#SBATCH --mem=2G
#SBATCH --time=24:00:00
#SBATCH --job-name=preprocess_all_data
#SBATCH --output=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/%x-%j.out
#SBATCH --error=/vol/knmimo-nobackup/users/pkools/thesis-forecasting/data/logs/%x-%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=pelle.kools@ru.nl

source /vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/.dgmr-venv/bin/activate

srun python preprocessing/apply_preprocessing.py