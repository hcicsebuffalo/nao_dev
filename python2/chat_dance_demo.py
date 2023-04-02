import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver

from naoqi import ALProxy


class chat_dance_class(object):
   
    def __init__(self, app, nao,  dance, play_song, led):
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
        
        self.dance = dance
        self.play_song = play_song
        self.led = led

        self.beh = ALProxy("ALBehaviorManager" , "10.0.107.217", 9559)

        print("Demo initialised")
               
    def onTouch(self,qwe):
        bool_okay=self.touch.signal.disconnect(self.touch_id)
        print("Touch Detected")
        self.nao.send_request()
        _beh = "System/animations/Stand/Gestures/JointHands_1"
        self.nao.sayText("Hello")
        self.beh.startBehavior(_beh)
        self.nao.sayText("How can I help you")
        self.nao.ledStartListening()
        self.nao.animation(2, 7)
        #time.sleep(7)
        res = str(self.nao.get_response())
        print(res)
        if res == "[u'Dance']":
            print("I am Dancing")
            self.nao.stop_all = False
            self.dance.start()
            #self.led.start()
            self.play_song.start()
            #timer1 = threading.Timer(10.0, self.dance.cancel)
            #timer2 = threading.Timer(10.0, self.led.cancel)
            #timer3 = threading.Timer(10.0, self.play_song.cancel)
            #timer1.start()
            #timer2.start()
            #timer3.start()
            time.sleep(10)
            
        else:
            res = res[4:]
            print("response is " , res)
            try:
                _beh = "System/animations/LED/CircleEyes"
                self.beh.startBehavior(_beh)
                _beh = "System/animations/Stand/BodyTalk/Speaking/BodyTalk_2"
                self.beh.startBehavior(_beh)
                self.nao.sayText(res)
            except:
                self.nao.sayText("Sorry I am not able to process your request for a moment")
        
        self.nao.ledStopListening()
            
        try:
            self.touch_id=self.touch.signal.connect(self.onTouch)
        except RuntimeError:
            print("Error in touch api" )
   
    
    def onDetect(self,qwe):
        bool_okay=self.face_detect.signal.disconnect(self.face_id)
        print("Face Detected")
        self.nao.sayText("Hello")
        self.nao.sayText("My Name is Aiko, Nice to meet you")
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