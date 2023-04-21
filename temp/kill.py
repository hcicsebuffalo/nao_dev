# -*- encoding: UTF-8 -*-
import qi
import sys

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
       
   
         
if __name__ == "__main__":
   
    try:
        app = qi.Application(["MyClass", "--qi-url=" + "tcp://10.0.255.22:9559"])
    except RuntimeError:
        print ("Verbindungsfehler")
        sys.exit(1)
       
    myC = MyClass(app)
    app.run()