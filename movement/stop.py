import threading
import driver as nao

ip = "10.0.107.217"
port = 9559

nao.InitProxy(ip)
nao.StopPlay()
