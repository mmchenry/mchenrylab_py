# video pre-processing script for collective motion videos
# written by Alberto P. Soto, McHenry Lab, 2020

# Add modules
import numpy as np
import cv2
import sys

# Set codec for output video
codec = 'mp4v'
# Set scaling factor
scaling = 1

# Set max index for background model
ind_max = 300

# use a circular mask to ignore area outside the tank
# mask_offset represents offset of circle from centre of the frame
mask_offset_x = -5
mask_offset_y = 10

# Set radius (pixels) of circular mask
mask_radius = 970

# name of source video and paths
video = 'rasbora-long-test'
input_vidpath = '/home/experimentalist/Documents/ONR-Schooling/2019-10-17/' + video + '.MOV'
output_vidpath = '/home/experimentalist/Documents/DeepPoseKit-schooling/test-videos' + video + '-bgSub-filt.mp4'
output_imgpath = '/home/experimentalist/Documents/idtracker-schooling/' + video + '-bgImage.png'

# # Open background and convert to grayscale image
# bg = cv2.imread('/home/experimentalist/Documents/DeepPoseKit-schooling/test-background/rasbora-bkgrnd.png')
# bg_gray = cv2.cvtColor(bg.copy(), cv2.COLOR_BGR2GRAY)
#
# # Take complement of background
# bg_inv = cv2.bitwise_not(bg_gray)

## Open video
cap = cv2.VideoCapture(input_vidpath)
if not cap.isOpened():
    sys.exit(
        'Video file cannot be read! Please check input_vidpath to ensure it is correctly pointing to the video file')

## Video writer class to output video with preprocessing
fourcc = cv2.VideoWriter_fourcc(*codec)

# Output frame size set by mask radius, which will be used for cropping video
output_framesize = (mask_radius * 2, mask_radius * 2)

# Create video output object
out = cv2.VideoWriter(filename=output_vidpath, fourcc=fourcc, fps=30.0, frameSize=output_framesize, isColor=False)

# Create a CLAHE object for histogram equalization
clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(61, 61))

# Create window for viewing background model
cv2.namedWindow('bg Model', cv2.WINDOW_NORMAL)

# Get first frame for setting up output video
ret, frame_init = cap.read()

# Initialize mask to ignore area outside the tank
mask = np.zeros((frame_init.shape[0], frame_init.shape[1]))

# Set circle center for mask
mask_center = (mask.shape[1] // 2 + mask_offset_x, mask.shape[0] // 2 + mask_offset_y)

# Make circle mask by calling circle function in cv2
cv2.circle(mask, mask_center, mask_radius, 255, -1)

# Image dimensions for cropping
crop_x = (mask_center[0] - mask_radius, mask_center[0] + mask_radius)
crop_y = (mask_center[1] - mask_radius, mask_center[1] + mask_radius)

# Resize dimensions (for image preview only)
resize_dim = (int(frame_init.shape[1] // 3), int(frame_init.shape[0] // 3))

# Create background object
bgmodel = cv2.createBackgroundSubtractorMOG2()

# Initialize variable to break while loop when last frame is achieved
last = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert current frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract current frame number
    frame_curr = cap.get(1)

    if ret:
        # Apply background model, returns binary foreground image
        fgmask = bgmodel.apply(frame)

        # Get background image
        bgImage = bgmodel.getBackgroundImage()

        # Show background model
        cv2.imshow('bg Model', cv2.resize(bgImage, resize_dim))

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Save background image and Break loop after max frames
    if frame_curr >= ind_max:
        # Write background image
        # cv2.imwrite(output_imgpath, bgImage)
        break

# Reset the counter for the video capture object
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Create window for viewing current output frame
cv2.namedWindow('frame_curr', cv2.WINDOW_NORMAL)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Extract current frame number
    this_frame = cap.get(1)

    if ret:
        # Convert current frame to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Take complement of background
        bg_inv = cv2.bitwise_not(bgImage)

        # Background subtraction (by adding inverse of background)
        frame_sub = cv2.add(frame, bg_inv)

        # Apply mask to current frame with background subtraction
        frame_sub[mask == 0] = 0

        # Apply histogram equalization to masked image
        frame_adjust = clahe.apply(frame_sub)

        # Apply smoothing filter
        frame_adjust = cv2.bilateralFilter(frame_adjust, 5, 40, 40)

        # cv2.imshow('Background Subtract', cv2.resize(frame_adjust, resize_dim))
        # k = cv2.waitKey(30) & 0xff
        # if k == 27:
        #     break

        # Crop image
        frame_crop = frame_adjust[crop_y[0]:crop_y[1], crop_x[0]:crop_x[1]].copy()

        # Write current processed frame to output object
        # out.write(frame_crop)

        # Display output image (bgSubtract + processed + cropped)
        cv2.imshow('frame_curr', frame_crop)
        if cv2.waitKey(1) == 27:
            break

    if last >= this_frame:
        break

    last = this_frame

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)