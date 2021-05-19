"""
Step thru workflow for prepping and running autotracking via tRex.
Note: Run in the 'video' environment
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

# Find coordinates for creating masks
do_maskCoords = False

# Make mask movies
do_makeMaskMovies = False


# --------------------------------------------------------------------------------
# IMPORT PACKAGES

import videoTools as vt
import numpy as np
import sys
import os

# --------------------------------------------------------------------------------
# FILE I/O

# Get the path info for video to be analyzed
file_name       = seq_name + ".mp4"
out_name        = seq_name + "_masked.mp4"
settings_name   = seq_name + ".settings" 

# Make full paths
in_path     = os.path.join(vid_root,file_name)
out_path    = os.path.join(vid_root,out_name)
set_path    = os.path.join(data_root,settings_name)


# --------------------------------------------------------------------------------
# CREATE MASKED VERSION OF THE VIDEO

if do_maskCoords:
    # Use code below to find coordinates for masking video
    print(" "); print("Select coordinates for the top mask")
    coord_top = vt.findCoord(vidPath,1,4)
    print(coord_top)

    print(" "); print("Select coordinates for the bottom mask")
    coord_bot = vt.findCoord(vidPath,1,4)
    print(coord_bot)
    #TODO: Save the data in files

# Coordinate values for masking testrun2 recordings
coord_top = [(0,93), (1280, 80), (1280, 0), (0,0)]
coord_bot = [(0, 214), (1280, 246), (1280, 296), (0, 296)]

# Export masked videos
if do_makeMaskMovies:
    vt.maskMovie(in_path, out_path, coord_top, coord_bot)



