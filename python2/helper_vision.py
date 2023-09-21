import os
import yaml
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


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param , "-----------")
    except yaml.YAMLError as e:
        print(e, "-------")
    
FACE_RECOG = True #param["face_recog"]
API_URL = "http://128.205.43.183:5006/face_recog" #param["face_recog_api"]  

NAO_IP = param["ip"]
NAO_PORT = param["port"]

width = 1280
hieght = 960
channel = 3 
fps = 30
sec = 5
camera_index = 0
resolution = 3
colourspace = 11
FPS = 5

tts = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
subscriberID = tts.subscribeCamera("subscriberID", camera_index, resolution,colourspace, FPS)

tts.openCamera(camera_index)
tts.startCamera(camera_index)

print("ID is :", subscriberID)
i = 0


def nao_vision():
    
    try: 

        while True:
            nao_image = tts.getImageRemote(str(subscriberID))

            img = (np.reshape(np.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))
            img = np.array(img)
            #img = np.flipud(img)  

            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) 
            if FACE_RECOG:
                _, image_encoded = cv2.imencode('.jpg', img)
                image_bytes = image_encoded.tobytes()

                # Send the image data to the server
                response = requests.post(API_URL, files={'image': ('image.jpg', image_bytes)})

                if response.status_code == 200:
                    processed_image_data = np.frombuffer(response.content, np.uint8)
                    img = cv2.imdecode(processed_image_data, cv2.IMREAD_UNCHANGED)
                else:
                    print("Face recog server error")

            cv2.imshow("video feed", img)

            k = cv2.waitKey(33)
            if k==27:    # Esc key to stop
                break

    except KeyboardInterrupt:
        print("\n ----- Python 2 Interupted ------")
        tts.releaseImage(subscriberID)
        tts.unsubscribe(subscriberID)

    tts.releaseImage(subscriberID)
    tts.unsubscribe(subscriberID)
    cv2.destroyAllWindows()