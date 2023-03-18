from tts import *

class nao_driver(tts):

    def __init__(self, ip, port):
        tts.__init__(self, ip, port)
        self.ip = ip
        self.port = port        

    def initProxies(self):
        self.initTTS()

