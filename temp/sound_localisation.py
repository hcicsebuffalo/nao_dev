import threading
import qi
import sys
from naoqi import ALProxy

ip = "10.0.255.8"
port = 9559


def base( demo):
        try:
            app = qi.Application([str(demo) , "--qi-url=" + "tcp://" + str(ip) + ":" + str(port)])
        except RuntimeError:
            print ("Connection Failed for touch api")
            sys.exit(1)
        
        _ = demo(app)
        app.run()

class Sound:
    def __init__(self, app ):
        super(Sound, self).__init__()

        my_session=app.session
        app.start()

        self.my_memory = my_session.service("ALMemory")
        
        self.Fronttouch = self.my_memory.subscriber("SoundDetected")
        self.Fronttouch_id=self.Fronttouch.signal.connect(self.onSound)

    def onSound(self, qwe):
        print("Detected")
         
sound_ISR = threading.Thread(target= base, args=(Sound)  )
sound_ISR.start()