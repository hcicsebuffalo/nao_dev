# -*- encoding: UTF-8 -*-

from base import *
import sys
import os
import csv
import qi


class MyClass(object):
   
    def __init__(self, app):
        super(MyClass, self).__init__()
        my_session=app.session
        app.start()
        self.my_tts=my_session.service("ALTextToSpeech")
        self.my_memory = my_session.service("ALMemory")
        self.touch = self.my_memory.subscriber("FrontTactilTouched")
        self.id=self.touch.signal.connect(self.killSwitch)
        print("Initialised")
        self.mySpeak()
        
               
    def killSwitch(self,qwe):
        #bool_okay=self.touch.signal.disconnect(self.id)
        print("Test")
        try:
            #self.my_tts.stopAll()
            #app.stop()
            #sys.exit(1)   
            print("Test pt 1 ")
            #os._exit(1)   
        except RuntimeError:
            print("Fehler:" )
   
   
    def mySpeak(self):
        self.my_tts.setVolume(0.1)
        self.my_tts.say("Hallo ", _async=True)
       
   

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
        
        try:
            app = qi.Application(["MyClass", "--qi-url=" + "tcp://" + str(ip) + ":" + str(port)])
        except RuntimeError:
            print ("Verbindungsfehler")
            sys.exit(1)
        
        self.myC = MyClass(app)
        app.run()
    
        
        


    
