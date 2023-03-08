import threading
import driver as nao
import time

ip = "10.0.107.217"
port = 9559


nao.InitProxy(ip)

dance = threading.Thread( target= nao.dance )
play_song = threading.Thread( target=nao.play_song )
#led = threading.Thread(target= nao.led_eye)

nao.say(" Hello Everyone ")

dance.start()
play_song.start()
#led.start()

while True:

    if play_song.is_alive() and not dance.is_alive():
        dance = threading.Thread( target= nao.dance )
        dance.start()

    if not play_song.is_alive() and not dance.is_alive():
        break
    
    time.sleep(1)
    nao.led_eye()

    #led.start()
    
# nao.StopPlay()
