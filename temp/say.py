from naoqi import ALProxy

PEPPER_IP = "10.0.52.247"
PEPPER_PORT = 9503


# tts = ALProxy("ALTextToSpeech", PEPPER_IP, PEPPER_PORT)
# tts.say("Hello, world!")


i = 0

run = True
while(i < 65536):

    try:
        PEPPER_PORT = i
        i = i +1
        print("------------------  ", i, "  -----------------------")
        tts = ALProxy("ALTextToSpeech", PEPPER_IP, i)
        tts.say("Hello, world!")
        run = False
        
    except:
        pass