from naoqi import ALProxy
import time

ip = "10.0.255.22"
port = 9559

motion_service = ALProxy("ALMotion" , ip, port)

tts = ALProxy("ALTextToSpeech" , ip, port)
#tts.setVoice("naoenu")

    
def openhand(inp):
    motion_service.openHand(inp)

openhand('LHand')
time.sleep(5)
openhand('RHand')
time.sleep(5)

def closehand(inp):
    motion_service.closeHand(inp)

closehand('LHand')
time.sleep(5)
closehand('RHand')
time.sleep(5)

tts.say("Task complete")