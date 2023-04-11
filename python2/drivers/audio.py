from base import *
import sys
import os
import csv

class audio(base):
    
    def __init__(self, ip, port):
        base.__init__(self)
        self.ip = ip
        self.port = port
        self.proxy_name_audio = "ALAudioPlayer"
        self.audio = None
    
    def initAudio(self):
        self.audio = self.connect(self.proxy_name_audio , self.ip, self.port)

    def play_song(self):#playProxy.post.playFile("song.mp3")
        self.audio.playFile("/home/nao/dance_30sec.mp3")