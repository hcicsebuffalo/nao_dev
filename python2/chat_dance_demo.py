import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver

from naoqi import ALProxy
from animations import anims

class chat_dance_class(object):
   
    def __init__(self, app, nao,  dance, play_song, led):
        super(chat_dance_class, self).__init__()
        my_session=app.session
        app.start()
        self.my_memory = my_session.service("ALMemory")
        
        self.touch = self.my_memory.subscriber("MiddleTactilTouched")
        self.touch_id=self.touch.signal.connect(self.onMiddleTouch)

        #self.face_detect = self.my_memory.subscriber("PeoplePerception/PeopleDetected")
        #self.face_id=self.face_detect.signal.connect(self.onDetect)

        #self.just_arrived = self.my_memory.subscriber("PeoplePerception/JustArrived")
        #self.just_arrived_id=self.just_arrived.signal.connect(self.onArrived)

        #self.waving = self.my_memory.subscriber("WavingDetection/PersonWaving")
        #self.waving_id = self.waving.signal.connect(self.onDetect)

        # -----------------------------------------------------------

        self.Fronttouch = self.my_memory.subscriber("FrontTactilTouched")
        self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)

        self.Reartouch = self.my_memory.subscriber("RearTactilTouched")
        self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)


        #self.HandRBtouch = self.my_memory.subscriber("HandRightBackTouched")
        #self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)

        self.HandRLtouch = self.my_memory.subscriber("HandRightLeftTouched")
        self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)

        self.HandRRtouch = self.my_memory.subscriber("HandRightRightTouched")
        self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)


        #self.HandLBtouch = self.my_memory.subscriber("HandLeftBackTouched")
        #self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)

        self.HandLLtouch = self.my_memory.subscriber("HandLeftLeftTouched")
        self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)

        self.HandLRtouch = self.my_memory.subscriber("HandLeftRightTouched")
        self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)



        self.nao = nao
        
        self.dance = dance
        self.play_song = play_song
        self.led = led

        self.beh = ALProxy("ALBehaviorManager" , "10.0.107.217", 9559)

        self.nao.sayText("You can ask me questions now")
        print("Demo initialised")
               
    def onMiddleTouch(self,qwe):
        bool_okay=self.touch.signal.disconnect(self.touch_id)
        print("Touch Detected")
        self.nao.send_request()
        _beh = "System/animations/Stand/Gestures/JointHands_1"
        self.nao.sayText("Hello")
        self.beh.startBehavior(_beh)
        self.nao.sayText("How can I help you")
        self.nao.ledStartListening()
        self.nao.animation(2, 7)
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
            #res = res[0:]
            res = self.process_res(res)
            print("response is " , res)
            try:
                #_beh = "System/animations/LED/CircleEyes"
                #self.beh.startBehavior(_beh)
                #beh = "System/animations/Stand/BodyTalk/Speaking/BodyTalk_2"
                #self.beh.startBehavior(_beh)
                self.nao.sayText(res)
            except:
                self.nao.sayText("Sorry I am not able to process your request for a moment")
        
        self.nao.ledStopListening()
            
        try:
            self.touch_id=self.touch.signal.connect(self.onMiddleTouch)
        except RuntimeError:
            print("Error in touch api" )
   
    def process_res(self, res):
        out = ''
        res = res[2:-2]
        for elem in res:
            if elem.isalnum() or elem == ' ' or elem == ".":
                out += elem 

        return out
    
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

    def onFrontTouch(self,qwe):
        try:
            bool_okay=self.Fronttouch.signal.disconnect(self.Fronttouch_id)
            _behavior = "boot-config/animations/hello"
            self.beh.startBehavior(_behavior)
            print(" Front Touch detected")    
            self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)
        except:
            pass

    def onRearTouch(self,qwe):
        try:
            bool_okay=self.Reartouch.signal.disconnect(self.Reartouch_id)
            _behavior =  "animations/Stand/Waiting/MysticalPower_1"
            self.beh.startBehavior(_behavior)
            print(" Rear Touch detected")

            self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)
        except:
            pass 
    
    def onHandRightBackTouch(self,qwe):
        try:
            bool_okay=self.HandRBtouch.signal.disconnect(self.HandRBtouch_id)
            _behavior = "animations/Stand/Waiting/AirGuitar_1"
            self.beh.startBehavior(_behavior)
            print(" Hand Right Back Touch detected")
            self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)
        except:
            pass

    def onHandRightLeftTouch(self,qwe):
        try:
            bool_okay=self.HandRLtouch.signal.disconnect(self.HandRLtouch_id)
            _behavior = "animations/Stand/Waiting/AirJuggle_1"
            self.beh.startBehavior(_behavior)
            print(" Hand Right Left Touch detected")
            self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)
        except:
            pass

    def onHandRightRightTouch(self,qwe):
        try:
            bool_okay=self.HandRRtouch.signal.disconnect(self.HandRRtouch_id)
            _behavior = "animations/Stand/Waiting/FunnyDancer_1"
            self.beh.startBehavior(_behavior)
            print(" Hand Right Right Touch detected")
            self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)
        except:
            pass
    
    def onHandLeftBackTouch(self,qwe):
        try:
            bool_okay=self.HandLBtouch.signal.disconnect(self.HandLBtouch_id)
            _behavior = "animations/Stand/Waiting/ShowMuscles_2"
            self.beh.startBehavior(_behavior)
            print(" Hand Left Back Touch detected")
            self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)
        except:
            pass
    
    def onHandLeftLeftTouch(self,qwe):
        try:
            bool_okay=self.HandLLtouch.signal.disconnect(self.HandLLtouch_id)
            _behavior = "animations/Stand/Waiting/AirGuitar_1"
            print(" Hand Left Left Touch detected")
            self.beh.startBehavior(_behavior)
            self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)
        except:
            pass

    def onHandLeftRightTouch(self,qwe):
        try:
            bool_okay=self.HandLRtouch.signal.disconnect(self.HandLRtouch_id)
            _behavior = "animations/Stand/Waiting/KungFu_1"
            print(" Hand Left Right Touch detected")
            self.beh.startBehavior(_behavior)
            self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)
        except:
            pass