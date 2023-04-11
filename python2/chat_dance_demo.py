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
        self.beh = ALProxy("ALBehaviorManager" , "10.0.107.217", 9559)
        nao.behave = self.beh
        # Face Interrupts

        #self.face_detect = self.my_memory.subscriber("PeoplePerception/PeopleDetected")
        #self.face_id=self.face_detect.signal.connect(self.onDetect)

        #self.just_arrived = self.my_memory.subscriber("PeoplePerception/JustArrived")
        #self.just_arrived_id=self.just_arrived.signal.connect(self.onArrived)

        #self.waving = self.my_memory.subscriber("WavingDetection/PersonWaving")
        #self.waving_id = self.waving.signal.connect(self.onDetect)

        # Touch Interrupts 

        self.touch = self.my_memory.subscriber("MiddleTactilTouched")
        self.touch_id=self.touch.signal.connect(self.onMiddleTouch)

        self.Fronttouch = self.my_memory.subscriber("FrontTactilTouched")
        self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)

        self.Reartouch = self.my_memory.subscriber("RearTactilTouched")
        self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)

        self.HandRLtouch = self.my_memory.subscriber("HandRightLeftTouched")
        self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)

        self.HandRRtouch = self.my_memory.subscriber("HandRightRightTouched")
        self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)

        self.HandLLtouch = self.my_memory.subscriber("HandLeftLeftTouched")
        self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)

        self.HandLRtouch = self.my_memory.subscriber("HandLeftRightTouched")
        self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)

        #self.HandRBtouch = self.my_memory.subscriber("HandRightBackTouched")
        #self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)

        #self.HandLBtouch = self.my_memory.subscriber("HandLeftBackTouched")
        #self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)

        self.nao = nao
        self.dance = dance
        self.play_song = play_song
        self.led = led
        self.res_thread = threading.Thread(target= self.get_response_thread)
        self.response = None
        # Initialisation complete
        self.nao.sayText("You can ask me questions now")
        print("Demo initialised")
    
    def get_response_thread(self):
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        self.response = str(self.nao.get_response())
        return 
        #print("====================================")
    def reset_thread(self):
        self.res_thread = threading.Thread(target= self.get_response_thread)
               
    def onMiddleTouch(self,qwe):
        bool_okay=self.touch.signal.disconnect(self.touch_id)
        print("Touch Detected")
        start_time = time.time()
        self.nao.gpt_request = True
        self.nao.send_request()
        self.res_thread.start()
        self.nao.sayText("Hello")
        self.beh.startBehavior("System/animations/Stand/Gestures/JointHands_1")
        self.nao.sayText("How can I help you")
        
        self.nao.ledStartListening()
        self.nao.animation(2, 12)
        
        first_wait = True
        wait = 3
        while self.res_thread.is_alive():
            if (time.time() - start_time) > wait:
                start_time = time.time()
                if first_wait:
                    #self.nao.sayText("Working on it")
                    first_wait = False
                    wait = 5
                else:
                    #self.nao.sayText("Still Working on it")
                    break

        self.reset_thread()
        res = self.response
        #print(res)
        
        if res == "[u'Dance']":
            print("I am Dancing")
            self.nao.stop_all = False
            self.dance.start()
            self.play_song.start()
            # while self.play_song.is_alive():
            #     if not self.dance.is_alive():
            #         self.dance.start()
        else:
            res = self.process_res(res)
            print('Response : ------------------------- \n')
            print('\n')
            print(res)
            try:
                self.nao.sayText(res)
            except:
                self.nao.sayText("Sorry I am not able to process your request for a moment")
        self.nao.ledStopListening()
        self.nao.gpt_request = False
        try:
            self.touch_id=self.touch.signal.connect(self.onMiddleTouch)
        except RuntimeError:
            print("Error in touch api" )
   
    def process_res(self, res):
        out = ''
        try:
            res = res[2:-2]
            for elem in res:
                if elem.isalnum() or elem == ' ' or elem == ".":
                    out += elem 
        except:
            pass
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
            self.beh.startBehavior("boot-config/animations/hello")
            print(" Front Touch detected ")  
            self.Fronttouch_id=self.Fronttouch.signal.connect(self.onFrontTouch)
        except:
            pass

    def onRearTouch(self,qwe):
        try:
            bool_okay=self.Reartouch.signal.disconnect(self.Reartouch_id)
            self.beh.startBehavior("animations/Stand/Waiting/MysticalPower_1")
            print(" Rear Touch detected ")
            self.Reartouch_id=self.Reartouch.signal.connect(self.onRearTouch)
        except:
            pass 
    
    def onHandRightBackTouch(self,qwe):
        try:
            bool_okay=self.HandRBtouch.signal.disconnect(self.HandRBtouch_id)
            self.beh.startBehavior("animations/Stand/Waiting/AirGuitar_1")
            print(" Hand Right Back Touch detected ")
            self.HandRBtouch_id=self.HandRBtouch.signal.connect(self.onHandRightBackTouch)
        except:
            pass

    def onHandRightLeftTouch(self,qwe):
        try:
            bool_okay=self.HandRLtouch.signal.disconnect(self.HandRLtouch_id)
            self.beh.startBehavior("animations/Stand/Waiting/AirJuggle_1")
            print(" Hand Right Left Touch detected")
            self.HandRLtouch_id=self.HandRLtouch.signal.connect(self.onHandRightLeftTouch)
        except:
            pass

    def onHandRightRightTouch(self,qwe):
        try:
            bool_okay=self.HandRRtouch.signal.disconnect(self.HandRRtouch_id)
            self.beh.startBehavior("animations/Stand/Waiting/FunnyDancer_1")
            print(" Hand Right Right Touch detected")
            self.HandRRtouch_id=self.HandRRtouch.signal.connect(self.onHandRightRightTouch)
        except:
            pass
    
    def onHandLeftBackTouch(self,qwe):
        try:
            bool_okay=self.HandLBtouch.signal.disconnect(self.HandLBtouch_id)
            self.beh.startBehavior("animations/Stand/Waiting/ShowMuscles_2")
            print(" Hand Left Back Touch detected")
            self.HandLBtouch_id=self.HandLBtouch.signal.connect(self.onHandLeftBackTouch)
        except:
            pass
    
    def onHandLeftLeftTouch(self,qwe):
        try:
            bool_okay=self.HandLLtouch.signal.disconnect(self.HandLLtouch_id)
            print(" Hand Left Left Touch detected")
            self.beh.startBehavior("animations/Stand/Waiting/AirGuitar_1")
            self.HandLLtouch_id=self.HandLLtouch.signal.connect(self.onHandLeftLeftTouch)
        except:
            pass

    def onHandLeftRightTouch(self,qwe):
        try:
            bool_okay=self.HandLRtouch.signal.disconnect(self.HandLRtouch_id)
            print(" Hand Left Right Touch detected")
            self.beh.startBehavior("animations/Stand/Waiting/KungFu_1")
            self.HandLRtouch_id=self.HandLRtouch.signal.connect(self.onHandLeftRightTouch)
        except:
            pass