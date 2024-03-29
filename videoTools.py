"""
    Series of functions for manipulating and interacting with video. Requires installing ffmpeg and opencv.
"""

# Imports
import cv2 as cv  # openCV for interacting with video
import os
import sys
import pathlib
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt


def getFrame(vid_path, fr_num=1):
    """Reads a single video frame"""

    # Check for file existance
    if not os.path.isfile(vid_path):
        raise Exception("Video file does not exist")

    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Video duration (in frames)
    frame_count = int(vid.get(cv.CAP_PROP_FRAME_COUNT))

    if fr_num > frame_count:
        raise Exception('Frame number requested exceeds video duration')
    else:
        vid.set(cv.CAP_PROP_POS_FRAMES, fr_num)
        _, frame = vid.read()

        return frame


def vidFromSeq(frame_start, imQuality=0.75, prefix="DSC", num_dig=5, suffix="JPG"):
    """Creates a movie in parent directory from an image sequence in current directory
       frame_start - Frame number to begin
       imQuality - image quality (0 - 1)
       prefix - Text that the image filenames begin with
       num_dig - Number of digits in image filenames
    """
    print("test2")
    # p is a path object for current directory
    p = pathlib.Path().absolute() 

    # Define output as file with name of current directory
    out_path = str(p.parent) + os.path.sep + str(p.parts[-1]) + ".mp4" 

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define and run command at terminal
    command = f"ffmpeg -start_number {frame_start}  -i DSC%05d.{suffix} -an -r 15 -crf {qVal}  '{out_path}'"
    os.system(command)


def convertWhole(vid_path, out_path, imQuality=0.75):
    """Converts a movie (uncropped) into a grayscale and compressed mp4.
       imQuality - image quality (0 - 1)
       out_path - full path of video file, with .mp4 extension
    """

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define command that uses ffmpeg
    command = f"ffmpeg -i '{vid_path}' -an -crf {qVal} -vf format=gray '{out_path}'"
    os.system(command)


def trimDur(vid_path, out_path, tEnd, tStart="00:00:00", imQuality=0.75):
    """Creates a new video file with a trimmed duration"""

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define and execute ffmpeg command
    command = f"ffmpeg -i '{vid_path}' -ss {tStart} -to {tEnd} -y '{out_path}'"
    os.system(command)


def trimDurCropped(vid_path, out_path, r, tEnd, tStart="00:00:00", imQuality=0.75):
    """Creates a new video file with a trimmed duration and cropped dimensions"""

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define and execute ffmpeg command
    # command = f"ffmpeg -i '{vid_path}' -ss {tStart} -to {tEnd} -y '{out_path}'"

    # Define command that uses ffmpeg
    command = f"ffmpeg -i '{vid_path}' -ss {tStart} -to {tEnd} -y -an -crf {qVal} -vf " \
              f"\"crop= {r[2]}:{r[3]}:{r[0]}:{r[1]}" \
              f",hue=s=0\" '{out_path}'"

    # Run command
    os.system(command)


def convertCropped(vid_path, out_path, r, imQuality=0.75):
    """Converts a movie (cropped) into a grayscale and compressed mp4.
       imQuality - image quality (0 - 1)
       out_path - full path of video file, with .mp4 extension
       r - rectangle that specifies the roi
    """

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define command that uses ffmpeg
    command = f"ffmpeg -i '{vid_path}' -y -an -crf {qVal} -vf " \
              f"\"crop= {r[2]}:{r[3]}:{r[0]}:{r[1]}" \
              f",hue=s=0\" '{out_path}'"

    # Run command
    # subprocess.call(command, shell=True)
    os.system(command)

def maskMovie(vid_path, out_path, coord_top, coord_bot):

    # Check for file existance
    if not os.path.isfile(vid_path):
        raise Exception("Video file does not exist")

    # Define input video object
    vid = cv.VideoCapture(vid_path)

    # Video writer class to output video with pre-processing
    fourcc = cv.VideoWriter_fourcc(*'MP4V')    
    # fourcc = cv.VideoWriter_fourcc(*'DIVX')
    # fourcc = cv.VideoWriter_fourcc(*'MJPG')
    # fourcc = cv.VideoWriter_fourcc(*'XVID')
    # fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    # fourcc = cv.VideoWriter_fourcc(*'mpv4')  

    # Video duration (in frames), frame rate, and frame numbers
    frame_count = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
    fps         = vid.get(cv.cv2.CAP_PROP_FPS)
    frNums      = list(range(frame_count))
    # frNums = list(range(5))

    # Get first frame, define mask
    im0 = getFrame(vid_path, 1)

    # Extract image dimensions
    h, w, d = im0.shape

    # Create video output object
    out = cv.VideoWriter(out_path,fourcc, fps, (int(w),int(h)))

    # Loop thru frames
    for frNum in frNums:

        # Read current frame
        im0 = getFrame(vid_path, frNum)
        # ret, im0 = vid.read()

        # Blank mask image
        imMask = np.zeros(im0.shape, np.uint8)

        # Make shape from points for lower mask
        pts_bot = np.array([[coord_bot]],np.int32)
        cv.fillPoly(imMask,pts_bot,(255,255,255))

        # Make shape from points for upper mask
        pts_top = np.array([[coord_top]],np.int32)
        cv.fillPoly(imMask,pts_top,(255,255,255))

        # Apply mask to image
        im0 = cv.bitwise_or(im0,imMask)

        # Visual check
        # plt.imshow(im0)
        # plt.show()

        # Write current processed frame to output object
        out.write(im0)

        print("Completed frame " + str(frNum) + " out of " + str(frame_count))


    # Clean up
    vid.release()
    out.release()

    # Closes all the frames
    cv.destroyAllWindows()

    # Report conclusion
    print(" ")
    print("Masked movie created:")
    print("    " + out_path)
    print(" ")


def findROI(vid_path, fr_num=1, show_crosshair=True, from_center=True):
    """Reads frame of video and prompts to interactively select a roi"""
    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Get frame and select roi
    im0 = getFrame(vid_path, fr_num)

    # Create named window
    cv.namedWindow("ROI_Select", cv.WINDOW_NORMAL)
    cv.startWindowThread()

    # Select ROI
    r = cv.selectROI("ROI_Select", im0, show_crosshair, from_center)

    # Release video capture and close window
    vid.release()
    cv.waitKey(1)
    cv.destroyAllWindows()

    return r


def findCoord(vid_path, poly_overlay=False, num_pts=inf, fr_num=1):
    """Reads frame of video and prompts to interactively select coordinates"""

    # get access to a couple of global variables we'll need
    global coords, drawing

    # Initialize container for coordinates
    coords = []

    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Get frame
    im0 = getFrame(vid_path, fr_num)

    # Create named window
    cv.namedWindow("Coord_Select", cv.WINDOW_GUI_EXPANDED)
    cv.startWindowThread()

    # Select coordinates
    cv.setMouseCallback('Coord_Select', clickCoords, im0)

    # Loop for collecting coordinates/keyboard inputs
    while 1==1:
        cv.imshow("Coord_Select",im0)
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break
        elif len(coords)==num_pts:
            break

    # Release video capture and close window
    vid.release()
    cv.waitKey(1)
    cv.destroyAllWindows()

    if poly_overlay:
        # Overlay points on video
        cv.imshow("Coord_Display", cv.WINDOW_NORMAL)
        cv.startWindowThread()

        # Construct polgon
        polygon = [np.int32(coords)]
        im0 = cv.polylines(im0, polygon, False, (0, 255, 0), thickness=2)

        # Interactive mode
        while True:
            cv.imshow("Coord_Display",im0)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break

        # Release video capture and close window
        vid.release()
        cv.waitKey(1)
        cv.destroyAllWindows()
    

    return coords


def clickCoords(event, x, y, flag, image):
    """
    Callback function, called by OpenCV when the user interacts
    with the window using the mouse. This function will be called
    repeatedly as the user interacts.
    """
    # get access to a couple of global variables we'll need
    global coords, drawing

    if event == cv.EVENT_LBUTTONDOWN:
        # user has clicked the mouse's left button
        drawing = True

        # Marker at the selected coordinates
        cv.circle(image,(x,y),3,(0,255,0),-1)

        # Add coordinates
        coords.append((x, y))


def getbackground(vid_path, out_path, max_frames):
    """Computes background of video and outputs as png"""
    # Create video capture object, check if video exists
    cap = cv.VideoCapture(vid_path)
    if not cap.isOpened():
        sys.exit(
            'Video cannot be read! Please check vid_path to ensure it is correctly pointing to the video file')

    # Create background object
    bgmodel = cv.createBackgroundSubtractorMOG2()

    # Get first frame for setting up output video
    ret, frame_init = cap.read()

    # Resize dimensions (for image preview only)
    resize_dim = (int(frame_init.shape[1] // 3), int(frame_init.shape[0] // 3))

    # Video duration (in frames)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # Set max index for background model
    if frame_count >= max_frames:
        ind_max = max_frames
    else:
        ind_max = frame_count

    # Create window for viewing current output frame
    cv.namedWindow("bg Model", cv.WINDOW_NORMAL)

    # Text and parameters for frame number overlay
    font = cv.FONT_HERSHEY_SIMPLEX
    text_pos = (400, 100)
    font_scale = 2
    font_color = (155, 155, 155)
    font_thickness = 2

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert current frame to grayscale
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Extract current frame number
        frame_curr = cap.get(1)

        if ret:
            # Apply background model, returns binary foreground image
            fgmask = bgmodel.apply(frame)

            # Get background image
            bgImage = bgmodel.getBackgroundImage()

            # Copy background image and add text for showing progress
            bg_copy = bgImage.copy()
            cv.putText(bg_copy, 'Frame: ' + str(frame_curr),
                       text_pos,
                       font,
                       font_scale,
                       font_color,
                       font_thickness, cv.LINE_AA)

            # Show background model progress
            cv.imshow("bg Model", cv.resize(bg_copy, resize_dim))
            cv.waitKey(20)

            # Close window and break loop with 'esc' key
            k = cv.waitKey(20) & 0xff
            if k == 27:
                break

        # Save background image and Break while loop after max frames
        if frame_curr >= ind_max:
            # Write background image
            cv.imwrite(out_path, bgImage)
            break

    print('Background image complete')

    # When everything done, release the capture
    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.waitKey(1)
    cv.waitKey(1)

    return bgImage


def bgsubtract(vid_path, out_path, roi):
    """Perform background subtraction and image smoothing to video"""

    # Open video, check if it exists
    cap = cv.VideoCapture(vid_path)

    if not cap.isOpened():
        sys.exit(
            'Video cannot be read! Please check vid_path to ensure it is correctly pointing to the video file')

    # Set codec for output video
    # codec = 'mp4v'
    codec = 'MJPG'

    # Open background image
    bgImg = cv.imread(out_path + '-bgImg.png')

    # Check if background image was loaded
    if bgImg is None:
        sys.exit("Could not read the image. Pathname incorrect OR needs to run getbackground")

    # Convert background image to grayscale
    bg_gray = cv.cvtColor(bgImg.copy(), cv.COLOR_BGR2GRAY)

    x1 = roi[0]
    y1 = roi[1]
    x2 = roi[2]
    y2 = roi[3]

    out_vid_path = out_path + '-bgSub.mp4'

    # Output frame size set by mask radius, which will be used for cropping video
    output_framesize = (int(y2), int(x2))

    # Video writer class to output video with pre-processing
    fourcc = cv.VideoWriter_fourcc(*codec)

    # Create video output object
    out = cv.VideoWriter(filename=out_vid_path, fourcc=fourcc, fps=30.0, frameSize=output_framesize, isColor=False)

    # Create a CLAHE object for histogram equalization
    clahe = cv.createCLAHE(clipLimit=6.0, tileGridSize=(61, 61))

    # Create window for viewing current output frame
    cv.namedWindow('frame_curr', cv.WINDOW_NORMAL)

    # Initialize variable to break while loop when last frame is achieved
    last = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Extract current frame number
        this_frame = cap.get(1)

        if ret:
            # Convert current frame to grayscale
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # Take complement of background
            bg_inv = cv.bitwise_not(bg_gray)

            # Background subtraction (by adding inverse of background)
            frame_sub = cv.add(frame, bg_inv)

            # Apply histogram equalization to background subtracted image
            frame_adjust = clahe.apply(frame_sub)

            # Apply smoothing filter
            frame_adjust = cv.bilateralFilter(frame_adjust, 5, 40, 40)

            # Crop image
            frame_crop = frame_adjust[int(y1):int(y1 + y2), int(x1):int(x1 + x2)]

            # Write current processed frame to output object
            out.write(frame_crop)

            # Display output image (bgSubtract + processed + cropped)
            cv.imshow('frame_curr', frame_crop)
            if cv.waitKey(1) == 27:
                break

        if last >= this_frame:
            break

        last = this_frame

    print("Background subtraction complete")

    # When everything done, release the capture
    cap.release()
    out.release()
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.waitKey(1)
    cv.waitKey(1)


