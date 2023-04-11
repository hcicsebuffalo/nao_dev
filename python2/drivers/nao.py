from tts import *
from leds import *
from touch import *
from face import *
from gesture import *
from socket_driver import *
from audio import *

class nao_driver(tts, leds, touch, gesture, chatGPT, audio):

    def __init__(self, ip, port, PORT_SOCKET, PORT_GUI):
        tts.__init__(self, ip, port)
        leds.__init__(self, ip, port)
        touch.__init__(self, ip, port)
        gesture.__init__(self, ip, port)
        audio.__init__(self, ip, port)
        chatGPT.__init__(self, '127.0.0.1', 5091)

        self.ip = ip
        self.port = port 
        self.stop_all = False
        self.PORT = PORT_SOCKET  
        self.GUI_PORT = PORT_GUI  
        self.gpt_request = False

        self.behave = None
        #my_session=app.session
        #app.start()
        #self.my_memory = my_session.service("ALMemory")
        #self.beh = ALProxy("ALBehaviorManager" , "10.0.107.217", 9559)


    def initProxies(self):
        self.initTTS()
        self.initLEDS()
        self.initmotion()
        self.initAudio()
        self.initSocket(self.PORT)
        self.initGui(self.GUI_PORT)
        
        
