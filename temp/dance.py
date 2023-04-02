from naoqi import ALProxy

ip = "10.0.107.217"
port = 9559

tts = ALProxy("ALBehaviorManager" , ip, port)

path = "/home/nao/behavior.xar"

x = tts.getBehaviorNames()

#tts.preloadBehavior("System/animations/Stand/Waiting/ShowMuscles_3"
tts.startBehavior("System/animations/Stand/BodyTalk/Speaking/BodyTalk_2")  



# with open("animation.txt", "w") as f:

#     for elem in x:
#         f.write(elem)
#         f.write("            \n")
