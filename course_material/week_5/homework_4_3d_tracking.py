#!/usr/bin/env python
import cv2
import sys
from homework_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

#initalize camera
camera = Camera()
#initalize robot
robot = Robot()

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Start robot
    robot.start()
    # Initalize ball detector
    ball_detector = BallDetector()

    #loop
    while True:
        # Get image from camera
        img = camera.getImage()
        # Detect ball
        (img, center) = ball_detector.detect(img)
        # Show ball
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break
        # Track ball
        if(center!= None):
            #TODO convert a 2d point to a 3d point on the camera coordinate system
            (x,y,z) =
            print (x,y,z,'on camera axis')

            #TODO convert a 3d point camera coordinate system to a 3d point on the robot coordinates system
            (x,y,z) =
            print (x,y,z,'on robot axis')

            #TODO: move robot to look at a 3d point
            robot.lookatpoint()

if __name__ == '__main__':
    main()
