"""
The aim here is to read a video, prompt a user to select landmarks 
for a central trapazoidal area, and then to output a masked version of the video.
"""

import videoTools as vt
# import numpy as np
import sys
# import cv2 as cv
import os

# Get the path info
file_name = "testrun2_C001H001S0001.mp4"
out_name = "testrun2_C001H001S0001_masked.mp4"
root_path = "/home/mmchenry/Videos/"
vid_path = os.path.join(root_path,file_name)
out_path = os.path.join(root_path,out_name)

#TODO: Get the 4 coordinates for marking out the polygon using vt.findCoord
# coords = vt.findCoord(vidPath,1,4)
# print(coords)

# Video frame dimensions: 296, 1280

coord_top = [(0,93), (1280, 80), (1280, 0), (0,0)]
coord_bot = [(0, 214), (1280, 246), (1280, 296), (0, 296)]

# coords = [(6, 226), (1157, 291), (1273, 50), (2, 68)]
# coords = [(4, 214), (1275, 245), (1276, 81), (2, 88)]

vt.maskMovie(vid_path, out_path, coord_top, coord_bot)

#TODO: Use the coordinates to read video files, apply the mask, and  export the video


sys.exit()


# Create a VideoCapture object
cap = cv.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
 
while(True):
  ret, frame = cap.read()
 
  if ret == True:
    # Write the frame into the file 'output.avi'
    out.write(frame)
    # Display the resulting frame   
    cv.imshow('frame',frame)
    # Press Q on keyboard to stop recording
    if cv.waitKey(1) & 0xFF == ord('q'):
      break
  # Break the loop
  else:
    break 

# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv.destroyAllWindows()
