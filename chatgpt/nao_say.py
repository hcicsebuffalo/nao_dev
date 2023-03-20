#! /usr/bin/python2
# -*- encoding: UTF-8 -*-

# Hash bang line added at top 

import naoqi
import json
from naoqi import ALProxy
import socket 

json_data = open('/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/json_file.json')
data = json.load(json_data)
data_string = data.encode()
NAO_IP = "10.0.107.217"
NAO_PORT = 9559
PEPPER_IP = "10.0.52.247"
PEPPER_PORT = 9503

tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.say(data_string)

# print(data_string)
