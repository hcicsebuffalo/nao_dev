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


# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
rabbit_channel = connection.channel()
rabbit_channel.queue_declare(queue='image_queue')

# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-6] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param , "-----------")
    except yaml.YAMLError as e:
        print(e, "-------")
    
FACE_RECOG = param["face_recog"]
API_URL = param["face_recog_api"]  

NAO_IP = "10.0.255.22"
NAO_PORT = 9559
PEPPER_IP = "10.0.52.247"
PEPPER_PORT = 9503

width = 1280
hieght = 960
channel = 3
 
fps = 30
sec = 5

tts = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
camera_index = 0
resolution = 3
colourspace = 11
FPS = 5
subscriberID = tts.subscribeCamera("subscriberID", camera_index, resolution,colourspace, FPS)
#subscriberID = "subscribeid_1"
tts.openCamera(camera_index)
tts.startCamera(camera_index)

print("ID is :", subscriberID)
i = 0
# stop = False
ref_time = datetime.now()
present_time = datetime.now()
diff_in_time = 0



while True:
#while diff_in_time != 5:
  i += 1 # ninad
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

  print( (nao_image[1], nao_image[0], nao_image[2]) , time.time())
  
  #cv2.imshow("Input", img)

  # Encode image to base64 string
  retval, buffer = cv2.imencode('.jpg', img)
  #image_str = base64.b64encode(buffer)#.decode('utf-8')
  image_str = buffer.tobytes()
  rabbit_channel.basic_publish(exchange='', routing_key='image_queue', body=image_str)
  #print( len(image_str) , " :  " , i)

  # k = cv2.waitKey(33)
  # if k==27:    # Esc key to stop
  #   break
  
connection.close()
tts.releaseImage(subscriberID)
tts.unsubscribe(subscriberID)
cv2.destroyAllWindows()