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

from helper import *

# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
rabbit_channel = connection.channel()
rabbit_channel.queue_declare(queue='image_queue')

tts = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
subscriberID = tts.subscribeCamera("subscriberID", camera_index, resolution,colourspace, FPS)

tts.openCamera(camera_index)
tts.startCamera(camera_index)

print("ID is :", subscriberID)
i = 0

try: 

  while True:
    i += 1 
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

    retval, buffer = cv2.imencode('.jpg', img)
    image_str = buffer.tobytes()
    rabbit_channel.basic_publish(exchange='', routing_key='image_queue', body=image_str)

    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
      break

    if i % 10 == 0:
       print("\t vision running")

except KeyboardInterrupt:
    print("\n ----- Python 2 Interupted ------")
    tts.releaseImage(subscriberID)
    tts.unsubscribe(subscriberID)

connection.close()
tts.releaseImage(subscriberID)
tts.unsubscribe(subscriberID)
cv2.destroyAllWindows()