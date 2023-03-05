import threading
import driver as nao
import time

ip = "10.0.107.217"
port = 9559


nao.InitProxy(ip)

dance = threading.Thread( target= nao.dance )
play_song = threading.Thread( target=nao.play_song )

nao.say("I will start dance now")

dance.start()
play_song.start()

while True:

    if play_song.is_alive() and not dance.is_alive():
        dance = threading.Thread( target= nao.dance )
        dance.start()

    if not play_song.is_alive() and not dance.is_alive():
        break

    time.sleep(1)
    
nao.StopPlay()
