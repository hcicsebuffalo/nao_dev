# Load Config --------------------------------------------------------------
import os
import yaml

current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    try:
        param = yaml.safe_load(ymlfile)
        print(param)
    except yaml.YAMLError as e:
        print(e)

ip = param["ip"]
port = param["port"]
PORT_SOCKET = param["py_port"]
PORT_GUI = param["gui_port"]

# Load Nao functions ------------------------------------------------------
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver

# Init Drivers
nao = nao_driver(ip, port, PORT_SOCKET, PORT_GUI)

def initialise_nao():
    # Init all Proxies
    nao.initProxies()
    
def nao_startup_routine():
    # Go to stand posture
    nao.posture.goToPosture("Stand" , 0.4)

    # Tab reset
    nao.tab_reset()

    # Say Text
    nao.sayText_no_url("Hello, My Name is Kai. Nice to meet you")
    
    # Stop listening 
    nao.ledStopListening()


# Threading functions ----------------------------------------------------
import threading

dance = threading.Thread( target = nao.dance )
play_song = threading.Thread( target = nao.play_song )
#led = threading.Thread(target= nao.led_eye)
led = None

def attach_thread_functions():
    nao.load_function(nao, dance, play_song)


# Touch interrupts -------------------------------------------------------

import time
from naoqi import ALProxy

class Touch_interrupts(object):
   
    def __init__(self, app, nao,  dance, play_song, led):
        super(Touch_interrupts, self).__init__()

        my_session=app.session
        app.start()

        self.my_memory = my_session.service("ALMemory")
        self.beh = ALProxy("ALBehaviorManager" , "10.0.255.8", 9559)
        nao.behave = self.beh

        self.nao = nao
        self.dance_cht = dance
        self.play_song_cht = play_song
        self.led = led
        self.response = None
        
        # Touch Interrupts 
        # self.touch = self.my_memory.subscriber("MiddleTactilTouched")
        # self.touch_id=self.touch.signal.connect(self.onMiddleTouch)

        self.Fronttouch = self.my_memory.subscriber("FrontTactilTouched")
        self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)

        # self.Reartouch = self.my_memory.subscriber("RearTactilTouched")
        # self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)

        # self.HandRLtouch = self.my_memory.subscriber("HandRightLeftTouched")
        # self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)

        # self.HandRRtouch = self.my_memory.subscriber("HandRightRightTouched")
        # self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)

        # self.HandLLtouch = self.my_memory.subscriber("HandLeftLeftTouched")
        # self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)

        # self.HandLRtouch = self.my_memory.subscriber("HandLeftRightTouched")
        # self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)

        #self.HandRBtouch = self.my_memory.subscriber("HandRightBackTouched")
        #self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)

        #self.HandLBtouch = self.my_memory.subscriber("HandLeftBackTouched")
        #self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)

        
    def onMiddleTouch(self,qwe):
        bool_okay=self.touch.signal.disconnect(self.touch_id)
        self.beh.startBehavior("animations/Stand/Waiting/WakeUp_1")
        print(" Middle Touch detected ") 
        time.sleep(4)
        try: 
            self.touch_id=self.touch.signal.connect(self.onMiddleTouch)
        except:
            print("error ---")
    
    def onFrontTouch(self,qwe):
        bool_okay=self.Fronttouch.signal.disconnect(self.Fronttouch_id)
        self.beh.startBehavior("boot-config/animations/hello")
        print(" Front Touch detected ") 
        time.sleep(4)
        try: 
            self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)
        except:
            print("error touch ")

    def onRearTouch(self,qwe):
        bool_okay=self.Reartouch.signal.disconnect(self.Reartouch_id)
        self.beh.startBehavior("animations/Stand/Waiting/MysticalPower_1")
        print(" Rear Touch detected ")
        time.sleep(4)
        try:
            self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)
        except:
            print("error ---")
    
    def onHandRightBackTouch(self,qwe):
        bool_okay=self.HandRBtouch.signal.disconnect(self.HandRBtouch_id)
        self.beh.startBehavior("animations/Stand/Waiting/AirGuitar_1")
        print(" Hand Right Back Touch detected ")
        time.sleep(4)
        try:
            self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)
        except:
            print("error ---")

    def onHandRightLeftTouch(self,qwe):
        bool_okay=self.HandRLtouch.signal.disconnect(self.HandRLtouch_id)
        self.beh.startBehavior("animations/Stand/Waiting/AirJuggle_1")
        print(" Hand Right Left Touch detected")
        time.sleep(4)
        try:
            self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)
        except:
            print("error ---")

    def onHandRightRightTouch(self,qwe):
        bool_okay=self.HandRRtouch.signal.disconnect(self.HandRRtouch_id)
        self.beh.startBehavior("animations/Stand/Waiting/FunnyDancer_1")
        print(" Hand Right Right Touch detected")
        time.sleep(4)
        try:
            self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)
        except:
            print("error ---")
    
    def onHandLeftBackTouch(self,qwe):
        bool_okay=self.HandLBtouch.signal.disconnect(self.HandLBtouch_id)
        self.beh.startBehavior("animations/Stand/Waiting/ShowMuscles_2")
        print(" Hand Left Back Touch detected")
        time.sleep(4)
        try:
            self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)
        except:
            print("error ---")
    
    def onHandLeftLeftTouch(self,qwe):
        bool_okay=self.HandLLtouch.signal.disconnect(self.HandLLtouch_id)
        print(" Hand Left Left Touch detected")
        self.beh.startBehavior("animations/Stand/Waiting/AirGuitar_1")
        time.sleep(4)
        try:
            self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)
        except:
            print("error ---")

    def onHandLeftRightTouch(self,qwe):
        bool_okay=self.HandLRtouch.signal.disconnect(self.HandLRtouch_id)
        print(" Hand Left Right Touch detected")
        self.beh.startBehavior("animations/Stand/Waiting/KungFu_1")
        time.sleep(4)
        try:
            self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)
        except:
            print("error ---")