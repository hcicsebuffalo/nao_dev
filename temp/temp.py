
dance = threading.Thread( target= nao.dance )
play_song = threading.Thread( target=nao.play_song )
led = threading.Thread(target= nao.led_eye)




say.start()
hello.start()

while say.is_alive() and hello.is_alive():
    pass

time.sleep(3)

def temp2():
    while 1:
        detected, timestamp, facePosition = nao.DetectFace() 
        if detected:
            nao.say("Hello, How are you")
        time.sleep(3)


face = threading.Thread(target= temp2)

face.start()
#########################################

# dance.start()
# play_song.start()
# led.start()


# while True:

#     if play_song.is_alive() and not dance.is_alive():
#         dance = threading.Thread( target= nao.dance )
#         dance.start()

#     if not play_song.is_alive() and not dance.is_alive():
#         break
    
#     time.sleep(1)
#     nao.led_eye()

#     #led.start()
    
# # nao.StopPlay()
