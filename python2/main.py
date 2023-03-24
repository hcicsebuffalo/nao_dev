import threading
import time
import sys
sys.path.append("drivers")
from drivers.nao import nao_driver
from chat_dance_demo import chat_dance_class 

ip = "10.0.107.217"
port = 9559

nao = nao_driver(ip, port)

nao.initProxies()
nao.sayText("Setup complete")
#nao.animation(1, 2)


chat_dance = threading.Thread(target= nao.initTG , args=(chat_dance_class, nao))

chat_dance.start()
#face.start()

#dance = threading.Thread( target= nao.dance )
#play_song = threading.Thread( target=nao.play_song )
#led = threading.Thread(target= nao.led_eye)

## Natu Natu 
