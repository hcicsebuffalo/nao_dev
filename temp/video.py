import os
import sys
import time
from naoqi import ALProxy
import numpy as np
import cv2
import time
from datetime import datetime
import os
import socket
import numpy as np
import pickle

import pika
import base64

# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()


NAO_IP = "10.0.107.217"
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

tts.openCamera(camera_index)
tts.startCamera(camera_index)

print("ID is :", subscriberID)
i = 0
# stop = False
ref_time = datetime.now()
present_time = datetime.now()
diff_in_time = 0

#client_socket, addr = s.accept()


# Declare the queue to consume from
channel.queue_declare(queue='image_queue')

while i<10:
    #while diff_in_time != 5:
    i += 1 # ninad
    nao_image = tts.getImageRemote(str(subscriberID))

    img = (np.reshape(np.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))
    img = np.array(img)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) 
    #print( (nao_image[1], nao_image[0], nao_image[2]))
    print(len(img))
    image_str = base64.b64encode(img.tobytes()).decode('utf-8')
    channel.queue_declare(queue='image_queue')
    channel.basic_publish(exchange='', routing_key='image_queue', body=image_str)

tts.releaseImage(subscriberID)
tts.unsubscribe(subscriberID)
connection.close()