
from base import *
import sys
import os
import csv
import qi

class FrontTouch(naoqi.ALModule):
    def __init__(self, name, ip, port):
        naoqi.ALModule.__init__(self, name)
        

    def onTouched(self, strVarName, value):
        
        #self.memory.unsubscribeToEvent("FrontTactilTouched",
        #    "FrontTouch")
            
        print("---------------------------------------")
        
        #self.memory.subscribeToEvent("FrontTactilTouched",
        #    "FrontTouch",
        #    "onTouched")

class touch(base):
    
    def __init__(self, ip, port):
        global FrontTouch

        base.__init__(self)
        self.ip = ip
        self.port = port
        self.proxy_name_tg = None
        self.tg = None
        self.s1 = None
        self.s2 = None
        self.broker = self.brokerConnect("touch", "0.0.0.0" , 0 , self.ip , self.port)
        
        self.memory = naoqi.ALProxy("ALMemory", ip, port)
        Ft = FrontTouch("FrontTatilToched" , self.ip , self.port)
        self.memory.subscribeToEvent("FrontTactilTouched","self", "headTouch")
        
    
    def initTG(self):
        #self.tg = self.connect(self.proxy_name_tg , self.ip, self.port)
        pass

    def headTouch(self):
        print("hii")
        self.memory.subscribeToEvent("FrontTactilTouched","self", "headTouch")
        #print("touch", "0.0.0.0" , 0 , self.ip , self.port)
        
        


    
