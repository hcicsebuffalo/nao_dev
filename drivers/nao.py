from tts import tts

class Nao(tts):

    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def initProxy(self):
        tts.connect(self.ip, self.port)
