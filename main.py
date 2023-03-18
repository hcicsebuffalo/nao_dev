import threading
import driver as nao
import time

ip = "10.0.107.217"
port = 9559


nao.InitProxy(ip)

dance = threading.Thread( target= nao.dance )
play_song = threading.Thread( target=nao.play_song )
led = threading.Thread(target= nao.led_eye)
