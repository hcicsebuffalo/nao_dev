import os
import sys
import time
from naoqi import ALProxy
import numpy as np
import cv2
import time
from datetime import datetime
import os
# import pika #1.1.0
import base64
import time 
import yaml
import cv2
import requests
import json
import numpy as np
import matplotlib.pyplot as plt



# using pepper ip and port though. :)
NAO_IP = "10.0.255.8" 
NAO_PORT = 9559

width = 1280
height = 960
channel = 3
 
fps = 30
sec = 5

def detect_traditional(frame):
  
  img = frame.copy()
  lower_red = np.array([0, 0, 90])
  upper_red = np.array([120, 60, 255])
  x,y,radius = None, None, None

  # Create a mask to isolate the red color region in the RGB image
  frame = cv2.inRange(frame, lower_red, upper_red)
  kernel = np.ones((3, 3), np.float32) / 9

  frame = cv2.erode(frame, kernel, iterations=3)

  contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # If contours are found
  if contours:
    # Get the largest contour (assuming it's the blob)
      largest_contour = max(contours, key=cv2.contourArea)
      
      # Find the minimum enclosing circle for the contour
      (x, y), radius = cv2.minEnclosingCircle(largest_contour)
      
      # Convert the coordinates to integers
      center = (int(x), int(y))
      radius = int(radius)
      
      # Draw the minimum enclosing circle on a color image
      frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert to color image
      cv2.circle(img, center, radius, (255, 0, 0), 2)  # Draw red circle
      
      #print("Radius of the blob:", radius)
  else:
      print("No blob found.")

      
  return img , x,y,radius

# we have to use the detect_YOLO fn on python3, this will not work here
def detect_YOLO(img):
    # load custom model
    model = yolov5.load('best.pt')    

    # set model parameters
    model.conf = 0.40  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    model.agnostic = False  # NMS class-agnostic 
    model.max_det = 1000  # maximum number of detections per image

    # Perform object detection
    results = model(img)

    # Get detected objects
    detected_objects = results.pred[0]
    no_of_detected_objects = len(detected_objects)

    boxes = detected_objects[:, :4] # x1, y1, x2, y2
    scores = detected_objects[:, 4]
    categories = detected_objects[:, 5]

    # Get the center coordinates
    boxes = boxes.squeeze(0)
    center_x = (boxes[0] + boxes[2]) / 2
    center_y = (boxes[1] + boxes[3]) / 2
    if (center_x.is_cuda):
        center_x = center_x.cpu()
        center_x = center_x.numpy()
        center_y = center_y.cpu()
        center_y = center_y.numpy()        
    else:
        center_x = center_x.numpy()
        center_y = center_y.numpy()

    # Save the image with bounding boxes
    img_with_boxes = results.render()[0]
    img_with_boxes_pil = Image.fromarray(img_with_boxes)

    return img_with_boxes_pil, center_x, center_y, no_of_detected_objects

# Define the video proxy
tts = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
camera_index = 0
resolution = 3
colourspace = 11
FPS = 5

subscriberID = tts.subscribeCamera("subscriberID", camera_index, resolution,colourspace, FPS)
print("id : " , subscriberID)
tts.openCamera(camera_index)
tts.startCamera(camera_index)

motion_service = ALProxy("ALMotion" , NAO_IP, NAO_PORT)
motion_service.setStiffnesses("Head", 1.0)

names = ["HeadYaw", "HeadPitch"]
fractionMaxSpeed = 0.1
kp_x = 0.0005
kd_x = 0.0
kp_y = 0.0005
kd_y = 0.0

prev_err_x = None
prev_err_y = None
timestep = 0.2
yaw_max = 2
yaw_min = -2

def track(x,y):
    global prev_err_x, prev_err_y, motion_service

    err_x = x - width/2
    err_y = y - height/2

    if prev_err_x == None:
        prev_err_x = err_x
        return

    if prev_err_y == None:
        prev_err_y = err_y
        return 
    
    angle_del_x = kp_x* err_x + kd_x*(err_x-prev_err_x)/timestep
    angle_del_y = kp_y* err_y + kd_y*(err_y-prev_err_y)/timestep

    angles = [angle_del_x,angle_del_y]
    motion_service.changeAngles(names,angles,fractionMaxSpeed)


def reset():
    angles = [0, 0.0]
    motion_service.setAngles(names,angles,fractionMaxSpeed)

reset()

time.sleep(5)
print("********** Started Tracking ********** ")


flag = 0 # 0-traditional, 1-YOLO

while True:

    try:
        nao_image = tts.getImageRemote(str(subscriberID))

        img = (np.reshape(np.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))
        img = np.array(img)
        img = np.flipud(img)
        # cv2.imwrite("img.jpg" , img)

        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) 

        # print( (nao_image[1], nao_image[0], nao_image[2]) , time.time())

        if flag == 0:
            img , x,y, radius = detect_traditional(img)
            
            if radius != None and radius > 50:
                track(x,y)

        elif flag == 1:
            img, x, y, no_of_detected_objects = detect_YOLO(img)
            
            if (no_of_detected_objects > 0):
                track(x,y)

        cv2.imshow("Output", img)

        k = cv2.waitKey(33)
        if k==27:    # Esc key to stop
            break

        time.sleep(timestep)
    
    except:
        tts.releaseImage(subscriberID)
        tts.unsubscribe(subscriberID)
  
tts.releaseImage(subscriberID)
tts.unsubscribe(subscriberID)

cv2.destroyAllWindows()