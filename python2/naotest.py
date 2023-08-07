import naoqi
from naoqi import ALProxy

ip = "10.0.255.22"
port = 9559

text_to_say = "i dont know!"

animation_player = ALProxy("ALAnimationPlayer", ip, port)

# Replace "animations/Stand/Gestures/Hey_1" with the name of the animation you want NAO to perform
animation_name = "animations/Stand/Gestures/IDontKnow_1"
tts = ALProxy("ALTextToSpeech", ip, port)

animation_player.run(animation_name)
tts.say(text_to_say)
