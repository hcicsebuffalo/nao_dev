from tts import *
from leds import *
from touch import *
from face import *
from gesture import *
from socket_driver import *
from audio import *

class nao_driver(tts, leds, touch, gesture, chatGPT, audio):

    def __init__(self, ip, port, PORT_SOCKET):
        tts.__init__(self, ip, port)
        leds.__init__(self, ip, port)
        touch.__init__(self, ip, port)
        gesture.__init__(self, ip, port)
        audio.__init__(self, ip, port)
        chatGPT.__init__(self, '127.0.0.1', 0000)

        self.ip = ip
        self.port = port 
        self.stop_all = False
        self.PORT = PORT_SOCKET    

    def initProxies(self):
        self.initTTS()
        self.initLEDS()
        self.initmotion()
        self.initAudio()
        self.initSocket(self.PORT)
        
        
