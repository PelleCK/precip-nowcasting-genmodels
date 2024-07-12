import os

# Variables to set for the specific user
USER_FOLDER = "/vol/knmimo-nobackup/users/pkools/thesis-forecasting"
PROJECT_FOLDER = os.path.join(USER_FOLDER.strip(), "precip-nowcasting-genmodels/generativemodels/DGMR")

# When not rendering a new list with IDs, use the default option as listed below
basic_IDs_npy = 'list_IDs_200822_avg001mm_all.npy'

# Global variables that point to the correct directory
path_data = "/scratch/pkools/thesis-forecasting/data"

path_code = PROJECT_FOLDER

path_project = '//'

dir_basic_IDs = os.path.join(path_code.strip(), 'data', basic_IDs_npy.strip('/'))

dir_train_IDs = os.path.join(path_code.strip(), 'data/train_split.npy')
dir_val_IDs = os.path.join(path_code.strip(), 'data/val_split.npy')
dir_test_IDs = os.path.join(path_code.strip(), 'data/test_split.npy')

dir_vae_train_IDs = os.path.join(path_code.strip(), 'data/list_IDs_200920_avg001mm_train_vae.npy')
dir_vae_val_IDs = os.path.join(path_code.strip(), 'data/list_IDs_200808_avg001mm_val_vae.npy')
dir_vae_test_IDs = os.path.join(path_code.strip(), 'data/list_IDs_202121_avg001mm_test_vae.npy')

dir_rtcor = os.path.join(path_data, "dataset_rtcor_complete")

dir_prep = 'preprocessed'
dir_rtcor_prep = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_prep')

dir_labels = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_rain_labels')
dir_labels_heavy = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_heavy_rain_labels')

prefix_rtcor_archive = 'RAD_NL25_RAC_5M_'
prefix_rtcor_recent = 'RAD_NL25_RAC_RT_'

temp_dir = ''
SPROG_dir = ''
