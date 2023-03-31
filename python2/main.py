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

nao.sayText("Hello, My Name is Aiko. Nice to meet you")

nao.animation(1, 2)

dance = threading.Thread( target = nao.dance )
play_song = threading.Thread( target = nao.play_song )
#led = threading.Thread(target= nao.led_eye)
led = None

chat_dance = threading.Thread(target= nao.initTG , args=(chat_dance_class, nao, dance, play_song, led))

chat_dance.start()

#face.start()


## Natu Natu 

# Google api vs whisper comparison -> done
# Microphone  - Sougato 
# look straight - Ninad 
# Sound - funtion write 
# person recognition with ourself -> 
# Latest ChatGPT -> Done | need to flush out the conversation variable maybe after 15 responses (otherwise chatgpt may crash) 