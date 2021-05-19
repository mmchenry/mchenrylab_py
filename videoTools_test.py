import videoTools as vt
import os

# testPath = "/home/mmchenry/Documents/video/geotaxis/"
testPath = "/home/mmchenry/Videos/"

# vt.vidFromSeq(541)

# Parameters
# vIn = "STUDIO10_S007_S001_T020.MOV"
vIn = "testrun_C001H001S0002.mp4"
vOut = "testrun_test.mp4"

# Pull together complete path
vPath = os.path.join(testPath,vIn)


# r = vt.findROI(vPath)
print(" ")
print("Select mask area")
coords = vt.findCoord(vPath, True)
print(" ")
print("Selected coordinates:")
print(coords)
# crop_image(vPath)