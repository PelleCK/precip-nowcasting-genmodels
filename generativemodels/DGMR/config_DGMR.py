import os

# Variables to set for the specific user
USER_FOLDER = "/vol/knmimo-nobackup/users/pkools/thesis-forecasting"
PROJECT_FOLDER = os.path.join(USER_FOLDER.strip(), "precip-nowcasting-genmodels/generativemodels/DGMR")

# When not rendering a new list with IDs, use the default option as listed below
basic_IDs_npy = 'list_IDs200621_avg001mm.npy'

# Global variables that point to the correct directory
path_data = os.path.join(USER_FOLDER.strip(), "data")

path_code = PROJECT_FOLDER

path_project = '//'

dir_basic_IDs = os.path.join(path_code.strip(), 'data', basic_IDs_npy.strip('/'))

dir_train_IDs = os.path.join(path_code.strip(), 'data/train_split.npy')
dir_val_IDs = os.path.join(path_code.strip(), 'data/val_split.npy')
dir_test_IDs = os.path.join(path_code.strip(), 'data/test_split.npy')

dir_rtcor = os.path.join(path_data.strip(), "rtcor-recent")

dir_prep = 'preprocessed'
dir_rtcor_prep = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_prep')

dir_labels = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_rain_labels')
dir_labels_heavy = os.path.join(path_data.strip(), dir_prep.strip('/'), 'rtcor_heavy_rain_labels')

prefix_rtcor = 'RAD_NL25_RAC_RT_'

temp_dir = ''
SPROG_dir = ''
