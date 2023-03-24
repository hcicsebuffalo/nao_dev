from base import *
import sys
import os
import csv
import qi


class face(base):
    
    def __init__(self, ip, port):
        
        base.__init__(self)
        self.ip = ip
        self.port = port
        
    def initface(self, demo, nao):
        try:
            app = qi.Application([str(demo) , "--qi-url=" + "tcp://" + str(self.ip) + ":" + str(self.port)])
        except RuntimeError:
            print ("Connection Failed for Face api")
            sys.exit(1)
        
        self.myC = demo(app, nao)
        app.run()
    
        
        


    
