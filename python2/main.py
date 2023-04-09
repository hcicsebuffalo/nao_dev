import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver
from chat_dance_demo import chat_dance_class 
import yaml
import os

# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param)
    except yaml.YAMLError as e:
        print(e)

ip = "10.0.107.217"
port = 9559
PORT_SOCKET = param["py_port"]

# Init Drivers
nao = nao_driver(ip, port, PORT_SOCKET)

# Init all Proxies
nao.initProxies()

# Initialisation method
nao.sayText("Hello, My Name is Aiko. Nice to meet you")

# Eye Animations
#nao.animation(2, 2)


dance = threading.Thread( target = nao.dance )
play_song = threading.Thread( target = nao.play_song )
#led = threading.Thread(target= nao.led_eye)
led = None

chat_dance = threading.Thread(target= nao.initTG , args=(chat_dance_class, nao, dance, play_song, led))

chat_dance.start()
