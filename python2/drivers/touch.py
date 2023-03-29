# -*- encoding: UTF-8 -*-

from base import *
import sys
import os
import csv
import qi


class touch(base):
    
    def __init__(self, ip, port):
        
        base.__init__(self)
        self.ip = ip
        self.port = port
        self.proxy_name_tg = None
        
    def initTG(self, demo, nao, dance, play_song, led):
        try:
            app = qi.Application([str(demo) , "--qi-url=" + "tcp://" + str(self.ip) + ":" + str(self.port)])
        except RuntimeError:
            print ("Connection Failed for touch api")
            sys.exit(1)
        
        self.myC = demo(app, nao, dance, play_song, led)
        app.run()
    
        
        


    
