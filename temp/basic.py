from naoqi import ALProxy
import time

ip = "10.0.255.8"
port = 9559

motion_service = ALProxy("ALMotion" , ip, port)

motion_service.openHand('LHand')
time.sleep(5)
motion_service.closeHand('LHand')