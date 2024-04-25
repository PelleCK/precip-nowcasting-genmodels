#!/bin/bash
#SBATCH --account=cseduproject
#SBATCH --partition=csedu
#SBATCH --qos=csedu-large
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --output=./logs/basicrun-%j.out
#SBATCH --error=./logs/basicrun-%j.err

source ../../.dgmr-venv/bin/activate
python basic_run_pelle.py

