import threading
import driver as nao

ip = "10.0.255.22"
port = 9559

nao.InitProxy(ip)
nao.StopPlay()
