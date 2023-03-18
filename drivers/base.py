import naoqi
import time

class base(object):

    def __init__(self):
        self.connect_wait_time = 0.01
    
    def connect(self, proxy_name, ip, port):
        
        proxy = None
        try:
            proxy = naoqi.ALProxy(proxy_name, ip, port)
            time.sleep( self.connect_wait_time )
        except RuntimeError as e:
            print (" Error when creating ", proxy_name, " proxy. ")
        
        return proxy 