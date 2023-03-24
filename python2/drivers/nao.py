from tts import *
from leds import *
from touch import *
from face import *
from gesture import *

class nao_driver(tts, leds, touch, gesture):

    def __init__(self, ip, port):
        tts.__init__(self, ip, port)
        leds.__init__(self, ip, port)
        touch.__init__(self, ip, port)
        gesture.__init__(self, ip, port)
        self.ip = ip
        self.port = port        

    def initProxies(self):
        self.initTTS()
        self.initLEDS()
        self.initmotion()
        
        
