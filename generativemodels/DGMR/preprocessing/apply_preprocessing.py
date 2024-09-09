import sys
sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/')
sys.path.append('/vol/knmimo-nobackup/users/pkools/thesis-forecasting/precip-nowcasting-genmodels/generativemodels/DGMR/preprocessing')

from preprocessing_rtcor import *
import config_DGMR
from tqdm import tqdm

# Location where all IDs of the 'rainy' images are specified (complete so not split is applied)
# location_list_IDs = config_DGMR.dir_basic_IDs

# dir_train_IDs = config_DGMR.dir_vae_train_IDs
# dir_val_IDs = config_DGMR.dir_vae_val_IDs
# dir_test_IDs = config_DGMR.dir_vae_test_IDs

# List the names of all the images
# fn_rtcor_train = np.load(dir_train_IDs, allow_pickle = True)
# fn_rtcor_val = np.load(dir_val_IDs, allow_pickle = True)
# fn_rtcor_test = np.load(dir_test_IDs, allow_pickle = True)

# dir_all_ids = config_DGMR.dir_basic_IDs
analysis_folder = os.path.join(config_DGMR.PROJECT_FOLDER, "data/analysis")
#TODO: specify the folder where the list of all sequences is stored (fixed mask)
dir_all_sequences = os.path.join(analysis_folder, todo)

# filenames_rtcor = np.append(fn_rtcor_train, fn_rtcor_val) # , fn_rtcor_test)
filenames_rtcor = np.load(dir_all_sequences, allow_pickle = True).ravel()
filenames_rtcor = [item for sublist in filenames_rtcor for item in sublist]
# only unique filenames
filenames_rtcor = np.unique(filenames_rtcor)

# #print((filenames_rtcor[0]))
print(f"Total number of listedID radar images: {len(filenames_rtcor)}")

# # Run preprocessing steps (files will be saved in the specified folder in the config
rtcor2npy(config_DGMR.dir_rtcor_prep, overwrite = False, preprocess = True, filenames = filenames_rtcor)

#----------
from os import listdir
from os.path import isfile, join

#print(config_DGMR.dir_rtcor_prep)
files_prep = sorted([f[:12] for f in listdir(config_DGMR.dir_rtcor_prep) if isfile(join(config_DGMR.dir_rtcor_prep, f))])
#print(files_prep[0])
print(f"Total number of prepped radar images: {len(files_prep)}")

print("Difference")
print(len(filenames_rtcor)-len(files_prep))
print(len(np.setdiff1d(np.array(filenames_rtcor), np.array(files_prep))))
#print(len(np.setdiff1d(np.array(files_prep), np.array(filenames_rtcor))))
print((np.setdiff1d(np.array(filenames_rtcor), np.array(files_prep))))

np.save(os.path.join(config_DGMR.PROJECT_FOLDER, 'data/listIDs_24seq_prepped_20082024_fixed_mask.npy'), files_prep)
