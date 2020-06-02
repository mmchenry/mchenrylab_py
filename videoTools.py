"""
    Requires ffmpeg and opencv
"""

# Imports
import cv2 as cv        # openCV for interacting with video
import os

def getFrame(vid_path, fr_num=1):
    """Reads a single video frame"""

    # Check for file existance
    if not os.path.isfile(vid_path):
        raise Exception("Video file does not exist")

    # Define video object &  video frame
    vid = cv.VideoCapture(vid_path)

    # Video duration (in frames)
    frame_count = int(vid.get(cv.CAP_PROP_FRAME_COUNT))

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
    os.system(command)

def trimDur(vid_path,out_path,tEnd,tStart="00:00:00",imQuality=0.75):
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

def convertCropped(vid_path,out_path,r,imQuality=0.75):
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
    im0 = getFrame(vid_path,fr_num)
    r = cv.selectROI(im0)
    cv.destroyAllWindows()

    return r



# def convertGIF(vid_path,out_path)
# TODO: Implement these lines to export gifs
# ffmpeg -i input_vid.mp4 -filter_complex "[0:v] palettegen" palette.png
# ffmpeg -i input_vid.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse,scale=640:-1,fps=15" output_vid.gif

