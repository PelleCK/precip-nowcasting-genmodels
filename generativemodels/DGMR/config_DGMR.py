from pathlib import Path

# Variables to set for the specific user
USER_FOLDER = Path("/vol/knmimo-nobackup/users/pkools/thesis-forecasting")
PROJECT_FOLDER = USER_FOLDER / "precip-nowcasting-genmodels/DGMR"

# When not rendering a new list with IDs, use the default option as listed below
basic_IDs_npy = 'list_IDs200621_avg001mm.npy'

# Global variables that point to the correct directory
path_data = USER_FOLDER / "data"

path_code = PROJECT_FOLDER

path_project = Path('//')

dir_basic_IDs = path_code / 'data' / basic_IDs_npy

dir_train_IDs = path_code / 'data/train_split.npy'
dir_val_IDs = path_code / 'data/val_split.npy'
dir_test_IDs = path_code / 'data/test_split.npy'

dir_rtcor = path_data / "rtcor-recent"

dir_prep = 'preprocessed'
dir_rtcor_prep = path_data / dir_prep / 'rtcor_prep'

dir_labels = path_data / dir_prep / 'rtcor_rain_labels'
dir_labels_heavy = path_data / dir_prep / 'rtcor_heavy_rain_labels'

prefix_rtcor = 'RAD_NL25_RAC_RT_'

temp_dir = Path('')
SPROG_dir = Path('')
