"""
Runs TGrabs and TRex
Note: Be sure to run in the 'tracking' environment
"""

# --------------------------------------------------------------------------------
# PARAMETER VALUES

# Name of sequence to be analyzed
seq_name = "testrun2_C001H001S0001"

# Root directories
vid_root        = "/home/mmchenry/Videos/schooling_test"
data_root       = "/home/mmchenry/Documents/schooling_test"


# --------------------------------------------------------------------------------
# EXECUTION CONTROL

# Include deep learning in tRex analysis
do_deepanalysis = False

# Overwrite existing .pv file
do_rerun_tgrabs = False

# --------------------------------------------------------------------------------
# IMPORT PACKAGES

import sys
import os

# --------------------------------------------------------------------------------
# PATHS

# Get the path info for video to be analyzed
file_name       = seq_name + "_masked.mp4"
out_name        = seq_name + "_masked"
settings_name   = seq_name + ".settings" 

# Make full paths
in_path     = os.path.join(vid_root,file_name)
out_path    = os.path.join(vid_root,out_name)
set_path    = os.path.join(data_root,settings_name)


# --------------------------------------------------------------------------------
# CREATE SETTINGS FILE FOR TGRABS

# Run TGrabs, if there is no .pv file
if not os.path.exists(out_path + ".pv") or do_rerun_tgrabs:
    runStr = "tgrabs -i " + in_path + " -o " + out_path
    os.system(runStr)


# --------------------------------------------------------------------------------
# CREATE SETTINGS FILE FOR TREX

# Initialize settings file
set_file = open(set_path,"w")

# Path to pv video file
set_file.write("filename = " + out_path + " \n")

# Path for writing data
set_file.write("fishdata_dir = " + data_root + " \n")

# Calibration constant, given as the width of the video frame in cm
set_file.write("meta_real_width = 183 \n")

# Ouput format for coordinate data [either csv or npz]
set_file.write("output_format = npz \n")

# Max number of fish in recording
set_file.write("track_max_individuals = 10 \n")

# Output posture data (e.g. midline coordinates)
set_file.write("output_posture_data = true \n")

# Save statistical data for the analysis
set_file.write("output_statistics = true \n")

# Whether to include deep learning
if do_deepanalysis:
    set_file.write("auto_train = true \n")
    set_file.write("recognition_enable = true \n")
else:
    set_file.write("auto_train = false \n")
    set_file.write("recognition_enable = false \n")

# Misc other parameters
L = ["gui_show_posture = false \n", \
    "output_invalid_value = nan \n", 
         ]
set_file.writelines(L)

# Wrap up the text file
set_file.close()

# Compose string to JUST LAUNCH TREX
# runStr = "trex -i " + out_path + " -o " + data_root + " -s " + set_path 

# Compose string to EXPORT DATA AND QUIT THE GUI
runStr = "trex -i " + out_path + " -o " + data_root + " -s " + set_path + " -auto_quit "

# Execute terminal command
os.system(runStr)

# Stop script
# sys.exit()