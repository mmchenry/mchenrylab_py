import argparse
import cv2

coords = []
drawing = False

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="Path to the image")
    args = vars(ap.parse_args())
    image_source = args["image"] if args["image"] else 0
    # now get our image from either the file or built-in webcam
    image = get_image(image_source)
    if image is not None:
        # show the captured image in a window
        cv2.namedWindow('CapturedImage', cv2.WINDOW_NORMAL)
        cv2.imshow('CapturedImage', image)
        # specify the callback function to be called when the user
        # clicks/drags in the 'CapturedImage' window
        cv2.setMouseCallback('CapturedImage', click_and_crop, image)
        while True:
            # wait for Esc or q key and then exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                print('Image cropped at coordinates: {}'.format(coords))
                cv2.destroyAllWindows()
                break

def get_image(source):
    # open the camera, grab a frame, and release the camera
    cam = cv2.VideoCapture(source)
    image_captured, image = cam.read()
    cam.release()
    if (image_captured):
        return image
    return None

def click_and_crop(event, x, y, flag, image):
    """
    Callback function, called by OpenCV when the user interacts
    with the window using the mouse. This function will be called
    repeatedly as the user interacts.
    """
    # get access to a couple of global variables we'll need
    global coords, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        # user has clicked the mouse's left button
        drawing = True
        # save those starting coordinates
        coords = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        # user is moving the mouse within the window
        if drawing is True:
            # if we're in drawing mode, we'll draw a green rectangle
            # from the starting x,y coords to our current coords
            clone = image.copy()
            cv2.rectangle(clone, coords[0], (x, y), (0, 255, 0), 2)
            cv2.imshow('CapturedImage', clone)
    elif event == cv2.EVENT_LBUTTONUP:
        # user has released the mouse button, leave drawing mode
        # and crop the photo
        drawing = False
        # save our ending coordinates
        coords.append((x, y))
        if len(coords) == 2:
            # calculate the four corners of our region of interest
            ty, by, tx, bx = coords[0][1], coords[1][1], coords[0][0], coords[1][0]
            # crop the image using array slicing
            roi = image[ty:by, tx:bx]
            height, width = roi.shape[:2]
            if width > 0 and height > 0:
                # make sure roi has height/width to prevent imshow error
                # and show the cropped image in a new window
                cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
                cv2.imshow("ROI", roi)

if __name__ == "__main__":
    main()