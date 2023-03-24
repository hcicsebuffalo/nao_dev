import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver

class chat_dance_class(object):
   
    def __init__(self, app, nao):
        super(chat_dance_class, self).__init__()
        my_session=app.session
        app.start()
        self.my_memory = my_session.service("ALMemory")
        
        self.touch = self.my_memory.subscriber("FrontTactilTouched")
        self.touch_id=self.touch.signal.connect(self.onTouch)

        #self.face_detect = self.my_memory.subscriber("PeoplePerception/PeopleDetected")
        #self.face_id=self.face_detect.signal.connect(self.onDetect)

        self.just_arrived = self.my_memory.subscriber("PeoplePerception/JustArrived")
        self.just_arrived_id=self.just_arrived.signal.connect(self.onArrived)

        self.waving = self.my_memory.subscriber("WavingDetection/PersonWaving")
        self.waving_id = self.waving.signal.connect(self.onWaving)
        
        self.nao = nao
        print("Demo initialised")
               
    def onTouch(self,qwe):
        bool_okay=self.touch.signal.disconnect(self.touch_id)
        print("Touch Detected")
        self.nao.sayText("Hello")
        self.nao.sayText("I am Nao")
        self.nao.ledStartListening()
        self.nao.animation(2, 5)
        time.sleep(5)
        self.nao.ledStopListening()

        try:
            self.touch_id=self.touch.signal.connect(self.onTouch)
        except RuntimeError:
            print("Error in touch api" )
   
    
    def onDetect(self,qwe):
        bool_okay=self.face_detect.signal.disconnect(self.face_id)
        print("Face Detected")
        self.nao.sayText("Hello")
        self.nao.sayText("Who are you")
        self.nao.hello_movement()
        
        self.nao.ledStartListening()
        time.sleep(5)
        self.nao.ledStopListening()

        try:
            self.face_id=self.face_detect.signal.connect(self.onTouch)  
        except RuntimeError:
            print("Error in Face api" )

    def onArrived(self,qwe):
        bool_okay=self.just_arrived.signal.disconnect(self.just_arrived_id)
        print("New People arrived")
        self.nao.sayText("Hello")
        self.nao.sayText("Who are you")
        self.nao.hello_movement()
        
        self.nao.ledStartListening()
        time.sleep(5)
        self.nao.ledStopListening()

        try:
            self.just_arrived_id=self.just_arrived.signal.connect(self.onArrived)  
        except RuntimeError:
            print("Error in Face Arrived api" )

    def onWaving(self, qwe):
        bool_okay=self.waving.signal.disconnect(self.waving_id)
        
        print("Waving detected")
        
        self.nao.sayText("Hello")
        self.nao.hello_movement()
        
        self.nao.ledStartListening()
        time.sleep(5)
        self.nao.ledStopListening()

        try:
            self.waving_id=self.waving.signal.connect(self.onWaving)  
        except RuntimeError:
            print("Error in Waving api" )
    
    def kill(self):
        #self.my_tts.stopAll()
        #app.stop()
        #sys.exit(1)   
        #print("Test pt 1 ")
        #os._exit(1)
        pass