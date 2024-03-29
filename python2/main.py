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
    try:
        param = yaml.safe_load(ymlfile)
        print(param)
    except yaml.YAMLError as e:
        print(e)

# IPs and Ports

ip = "10.0.255.8"
port = 9559
PORT_SOCKET = param["py_port"]
PORT_GUI = param["gui_port"]

# Init Drivers
nao = nao_driver(ip, port, PORT_SOCKET, PORT_GUI)

# Init all Proxies
nao.initProxies()
nao.posture.goToPosture("Stand" , 0.4)
# Initialisation method
nao.tab_reset()
nao.sayText_no_url("Hello, My Name is Kai. Nice to meet you")
nao.posture.goToPosture("Stand" , 0.4)
# Eye Animations
#nao.animation(2, 2)
nao.ledStopListening()


dance = threading.Thread( target = nao.dance )
play_song = threading.Thread( target = nao.play_song )
#led = threading.Thread(target= nao.led_eye)
led = None

nao.load_function(nao, dance, play_song)

gui_thread = threading.Thread(target= nao.socket_loop, args=(nao , True))
# chat_dance = threading.Thread(target= nao.initTG , args=(chat_dance_class, nao, dance, play_song, led))
wake_thread = threading.Thread(target= nao.wake_wrd_loop, args=(nao , True))

# chat_dance.start()
gui_thread.start()
wake_thread.start()

