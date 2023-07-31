from naoqi import ALProxy

ip = "10.0.255.22"
port = 9559

tts = ALProxy("ALTextToSpeech" , ip, port)
tts.setVoice("naoenu")
tts.say(" Give me some time, I am working on it")