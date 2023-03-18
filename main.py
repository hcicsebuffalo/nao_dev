import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver

ip = "10.0.107.217"
port = 9559

nao = nao_driver(ip, port)

nao.initProxies()
nao.sayText("Hello")

#dance = threading.Thread( target= nao.dance )
#play_song = threading.Thread( target=nao.play_song )
#led = threading.Thread(target= nao.led_eye)
