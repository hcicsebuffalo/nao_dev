from naoqi import ALProxy
import time

from animations import *

ip = "10.0.107.217"
port = 9559

tts = ALProxy("ALBehaviorManager" , ip, port)

# path = "/home/nao/behavior.xar"

# x = tts.getInstalledBehaviors()

# #print(x)
# #tts.preloadBehavior("System/animations/Stand/Waiting/AirGuitar_1")



tts.startBehavior(anims[897])  

#------------------

# with open("animations.txt", "w") as f:

#     for i , elem in enumerate(x):
#         out = str(i) + " : \"" + str(elem) + "\"  , "
#         print(out)
#         f.write(out)
#         f.write("            \n")


# tts = ALProxy("ALAutonomousBlinking" , ip, port)

# path = "/home/nao/behavior.xar"

# x = tts.setEnabled(False)


# tts = ALProxy("ALSpeakingMovement" , ip, port)

# path = "/home/nao/behavior.xar"

# x = tts.setEnabled(True)




# tts = ALProxy("ALAnimatedSpeech" , ip, port)

# path = "/home/nao/behavior.xar"

# x = tts.say("I am Aiko a humanoid robot working in Davis Hall at the University at Buffalo under Professor Nalini Ratha I am designed to assist and provide support to students and faculty members in various tasks")


# motion_service = ALProxy("ALMotion" , ip, port)

# motion_service.setStiffnesses("Head", 1.0)

# # Simple command for the HeadYaw joint at 10% max speed
# names            = "HeadYaw"
# angles           = 1
# fractionMaxSpeed = 1
# motion_service.setAngles(names,angles,fractionMaxSpeed)

# names            = "HeadPitch"
# angles           = 0
# fractionMaxSpeed = 1
# motion_service.setAngles(names,angles,fractionMaxSpeed)

# time.sleep(3.0)
# motion_service.setStiffnesses("Head", 0.0)