import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import argparse
import numpy as np
print(cv2.__version__)
sys.path.append('..')

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import rospy
from lib.camera_v2 import Camera

from lib.ros_environment import ROSEnvironment
from lib.robot import Robot

#TODO: set the path for the configuration, weight, and class names
cfg_path = "./yolov3-tiny.cfg"
weight_path= "./yolov3-tiny.weights"
class_name_path = "./yolov3.txt"

#Loads class names into an array
classes = None
with open(class_name_path, 'r') as file:
    classes = [line.strip() for line in file.readlines()]

#Creates different color for different colors
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


#draws bounding box on the image
def draw_boundingbox(img, class_id, confidence, x, y, x_end, y_end):
    class_name = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (int(x), int(y)), (int(x_end) ,int(y_end)), color, 2)
    cv2.putText(img, class_name, (int(x-10),int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    robot = Robot()
    robot.start()

    #loops
    while(True):
        #gets image from camera
        cam_image = camera.getImage()

        #Gets width and height of image
        input_image = cam_image
        width = input_image.shape[1]
        height = input_image.shape[0]

        #TODO: check deep neural network with weight and configure file
        net = cv2.dnn.readNet(weight_path, cfg_path)

        #creates a "bob" that is the input image after mean subtraction, normalizing, channel swapping
        #0.00392 is the scale factor
        #(416,416) is the size of the output image
        #(0,0,0) are the mean values that will be subtracted for each channel RGB
        blob = cv2.dnn.blobFromImage(input_image, 0.00392, (416,416), (0,0,0), True, crop=False)

        #Inputs blob into the neural network
        net.setInput(blob)

        #gets the output layers "yolo_82', 'yolo_94', 'yolo_106"
        #output layer contains the detection/prediction information
        layer_names = net.getLayerNames()
        #getUnconnectedOutLayers() returns indices of unconnected layers
        #layer_names[i[0] - 1] gets the name of the layers of the indices
        #net.getUnconnectedOutLayers() returns [[200], [227], [254]]
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        #Runs forward pass to compute output of layer
        #returns predictions/detections at 32, 16 and 8 scale
        preds = net.forward(output_layers)

        #Initialize list that contains class id, confidence values, bounding boxes
        class_ids = []
        confidence_values = []
        bounding_boxes = []

        #TODO: Change the values for conf_threshold and nms_threshold
        #Initialize confidence threshold and threshold for non maximal suppresion
        conf_threshold = 0.5
        nms_threshold = 0.4

        #for each scale, we go through the detections
        for pred in preds:
            for detection in pred:
                #Use the max score as confidence
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                #Check if confidence is greather than threshold
                if confidence > conf_threshold:
                    #Compute x,y, widht, height, class id, confidence value
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidence_values.append(float(confidence))
                    bounding_boxes.append([x, y, w, h])

        #TODO: check your threshold for non maximal suppression
        indices = cv2.dnn.NMSBoxes(bounding_boxes, confidence_values, conf_threshold, nms_threshold)

        #draw results
        #tracked_object flag for if object is already tracked
        tracked_object = 0
        for i in indices:
            i = i[0]
            box = bounding_boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            center_x = x+w/2.0
            center_y = y+h/2.0
            classid = class_ids[i]
            class_name = str(classes[classid])

            #If detected object equals to the object tracked
            #TODO: make if statement  for selecting the object you want to track
            if
                #TODO: convert the 2d point to a 3d point on the camera coordinates system
                () = camera.convert2d_3d(
                #TODO: convert the 3d point on the camera coordinates system to a 3d point on the robot coordinates system
                (x_3d,y_3d,z_3d) = camera.convert3d_3d()
                #TODO: command the robot to look at the point
                robot.lookatpoint()

                tracked_object = 1
                conf_value = confidence_values[i]
                draw_boundingbox(input_image, classid, conf_value, round(x), round(y), round(x+w), round(y+h))
                print("Traking "+class_name, conf_value)

        #show image
        cv2.imshow("Object Detection Window", input_image[...,::-1])
        key = cv2.waitKey(1)
        cv2.imwrite("detected_object.jpg", input_image)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
