from naoqi import ALProxy

ip = "10.0.107.217"
port = 9559

tts = ALProxy("ALTextToSpeech" , ip, port)
tts.setVoice("naoenu")
tts.say(" Hello")