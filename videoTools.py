"""
    Requires ffmpeg and opencv
"""

# Imports
import cv2 as cv  # openCV for interacting with video
import os
import sys


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
    """Converts a movie (cropped) into a grayscale and slightly mp4.
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


def findROI(vid_path, fr_num=1):
    """Reads frame of video and prompts to interactively select a roi"""
    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Get frame and select roi
    im0 = getFrame(vid_path, fr_num)

    # Create named window
    cv.namedWindow("ROI_Select", cv.WINDOW_NORMAL)
    cv.startWindowThread()

    # Select ROI
    r = cv.selectROI("ROI_Select", im0)

    # Release video capture and close window
    vid.release()
    cv.waitKey(1)
    cv.destroyAllWindows()

    return r


def getbackground(vid_path, out_path, max_frames):
    """Computes background of video and outputs as png"""
    # Open video, check if it exists
    cap = cv.VideoCapture(vid_path)
    if not cap.isOpened():
        sys.exit(
            'Video cannot be read! Please check vid_path to ensure it is correctly pointing to the video file')

    # Create background object
    bgmodel = cv.createBackgroundSubtractorMOG2()

    # Get first frame for setting up output video
    ret, frame_init = cap.read()

    # Resize dimensions (for image preview only)
    resize_dim = (int(frame_init.shape[1] // 2), int(frame_init.shape[0] // 2))

    # Set max index for background model
    ind_max = max_frames

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

            # Show background model progress
            cv.imshow('bg Model', cv.resize(bgImage, resize_dim))

            # Close window and break loop with 'esc' key
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break

        # Save background image and Break while loop after max frames
        if frame_curr >= ind_max:
            # Write background image
            cv.imwrite(out_path + 'bgImage.png', bgImage)
            break

        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()
        cv.waitKey(1)

        return bgImage

    # TODO: fix issue with closing windows after executing routine

def bgsubtract(vid_path, out_path, r):
    """Perform background subtraction and image smoothing to video"""

# TODO: Check output of finfROI and use this to generate mask
    # Open video, check if it exists
    cap = cv.VideoCapture(vid_path)
    if not cap.isOpened():
        sys.exit(
            'Video cannot be read! Please check vid_path to ensure it is correctly pointing to the video file')

    # Set codec for output video
    codec = 'mp4v'

    # Output frame size set by mask radius, which will be used for cropping video
    output_framesize = (mask_radius * 2, mask_radius * 2)

    # Video writer class to output video with preprocessing
    fourcc = cv.VideoWriter_fourcc(*codec)

    # Create video output object
    out = cv.VideoWriter(filename=out_path, fourcc=fourcc, fps=30.0, frameSize=output_framesize, isColor=False)

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
            bg_inv = cv.bitwise_not(bgImage)

            # Background subtraction (by adding inverse of background)
            frame_sub = cv.add(frame, bg_inv)

            # Apply mask to current frame with background subtraction
            frame_sub[mask == 0] = 0

            # Apply histogram equalization to masked image
            frame_adjust = clahe.apply(frame_sub)

            # Apply smoothing filter
            frame_adjust = cv.bilateralFilter(frame_adjust, 5, 40, 40)

            # cv2.imshow('Background Subtract', cv2.resize(frame_adjust, resize_dim))
            # k = cv2.waitKey(30) & 0xff
            # if k == 27:
            #     break

            # Crop image
            frame_crop = frame_adjust[crop_y[0]:crop_y[1], crop_x[0]:crop_x[1]].copy()

            # Write current processed frame to output object
            # out.write(frame_crop)

            # Display output image (bgSubtract + processed + cropped)
            cv.imshow('frame_curr', frame_crop)
            if cv.waitKey(1) == 27:
                break

        if last >= this_frame:
            break

        last = this_frame

    # When everything done, release the capture
    cap.release()
    out.release()
    cv.destroyAllWindows()
    cv.waitKey(1)

# def convertGIF(vid_path,out_path)
# TODO: Implement these lines to export gifs
# ffmpeg -i input_vid.mp4 -filter_complex "[0:v] palettegen" palette.png
# ffmpeg -i input_vid.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse,scale=640:-1,fps=15" output_vid.gif
