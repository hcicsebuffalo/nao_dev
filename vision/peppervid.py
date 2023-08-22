import os
import sys
import time
from naoqi import ALProxy
import numpy as np
import cv2
import time
from datetime import datetime
import os
import pika #1.1.0
import base64
import time 
import yaml
import cv2
import requests
import json
import numpy as np

# Connect to Pepper
PEPPER_IP = "10.0.255.8"
PEPPER_PORT = 9559

width = 1280
hieght = 960
channel = 3
 
fps = 30
sec = 5

tts = ALProxy("ALVideoDevice", PEPPER_IP, PEPPER_PORT)
tabletService = ALProxy("ALTabletService" , PEPPER_IP, PEPPER_PORT)

camera_index = 0
resolution = 3
colourspace = 11
FPS = 5
subscriberID = tts.subscribeCamera("subscriberID", camera_index, resolution,colourspace, FPS)
#subscriberID = "subscribeid_1"
tts.openCamera(camera_index)
tts.startCamera(camera_index)

# Access the camera service
# camera_service = session.service("ALVideoDevice")

# Subscribe to the camera feed
# camera_id = camera_service.subscribeCamera("my_camera", camera_name, resolution, color_space, fps)

try:
    while True:
        # Retrieve a camera image
        image = tts.getImageRemote(subscriberID)
        
        # Convert the image data to a numpy array
        width = image[0]
        height = image[1]
        image_data = np.frombuffer(image[6], dtype=np.uint8)
        image_np = image_data.reshape((height, width, 3))
        
        # Convert the image to JPEG format (required for tablet display)
        _, image_jpeg = cv2.imencode(".jpg", image_np)
        
        # Display the image on the tablet
        tabletService.showImage(image_jpeg.tostring())
        
        # Process the image using OpenCV or other libraries
        # For example, you can display the image using OpenCV
        cv2.imshow("Camera Feed", image_np)
        cv2.waitKey(1)  # Display the frame for a short duration

        

except KeyboardInterrupt:
    pass

# Unsubscribe and disconnect
# tts.unsubscribe(camera_id)
# session.close()
tts.releaseImage(subscriberID)
tts.unsubscribe(subscriberID)
cv2.destroyAllWindows()
tabletService.hideImage()