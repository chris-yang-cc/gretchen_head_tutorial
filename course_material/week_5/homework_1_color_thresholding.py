#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

# Initalize camera
camera = Camera()
# Intalize point
point = (0,0)

#TODO: set the lower and upper limit for filtering the selected color

# Lower bound for the selected color
colorLower = (, , )
# Upper bound for the selected color
colorUpper = (, , )


def color_segmentation(frame):
    # convert it to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Use inRange to get the mask/color segmentation for the selected color
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    #Show color segmentation
    cv2.namedWindow("Filter", cv2.WINDOW_NORMAL)
    cv2.imshow("Filter", mask)

def main():
    global point
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        #performs color segmentation on image
        color_segmentation(img)

        # Show image
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
