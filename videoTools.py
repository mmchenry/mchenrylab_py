"""Usage: import videoTools as vt
    Requires ffmpeg and opencv

"""


# Imports
import cv2 as cv        # openCV for interacting with video
import subprocess       # For running ffmpeg at the shell

def getFrame(vid_path, fr_num=1):
    """Reads a single video frame"""

    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Video duration (in frames)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if fr_num>frame_count:
        raise Exception('Frame number requested exceeds video duration')
    else:
        vid.set(cv.CAP_PROP_POS_FRAMES, fr_num)
        _, frame = vid.read()

        return frame

def convertWhole(vid_path,out_path,imQuality=0.75):
    """Converts a movie (uncropped) into a grayscale and compressed mp4.
       imQuality - image quality (0 - 1)
       out_path - full path of video file, with .mp4 extension
    """

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51*(1 - imQuality)

    # Define command that uses ffmpeg
    command = f"ffmpeg -i '{vid_path}' -an -crf {qVal} -vf format=gray '{out_path}'"

    # Run command
    subprocess.call(command, shell=True)

def convertCropped(vid_path,out_path,r,imQuality=0.75):
    """Converts a movie (cropped) into a grayscale and slightly mp4.
       imQuality - image quality (0 - 1)
       out_path - full path of video file, with .mp4 extension
       r - rectangle that specifies the roi
    """

    # Quality value, on the 51-point scale used by ffmpeg
    qVal = 51 * (1 - imQuality)

    # Define command that uses ffmpeg
    command = f"ffmpeg -i '{vid_path}' -an -crf 13 -vf " \
              f"\"crop= {r[2]}:{r[3]}:{r[0]}:{r[1]}" \
              f",hue=s=0\" '{out_path}'"

    # Run command
    subprocess.call(command, shell=True)

def findROI(vid_path, fr_num=1):
    """Reads frame of video and prompts to interactively select a roi"""

    im = getFrame(vid_path,fr_num)
    r = cv.selectROI(im)
    cv.destroyAllWindows()

    return r

