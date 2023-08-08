from naoqi import ALProxy
import time

ip = "10.0.255.22"
port = 9559

mm = ALProxy("ALTextToSpeech" , ip, port)
mm.say("Hi")


motion_service = ALProxy("ALMotion" , ip, port)
motion_service.move(1, 0, 0)
time.sleep(10)
motion_service.move(0, 0, 0)
