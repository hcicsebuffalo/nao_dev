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
    
    def brokerConnect(self,name , listen_ip, port, parent_ip, parent_port):
        myBroker = None
        try:
            myBroker = naoqi.ALBroker(name, listen_ip,   # listen to anyone
                                    port,           # find a free port and use it
                                    parent_ip,          # parent broker IP
                                    parent_port)        # parent broker port
        except RuntimeError as e:
            print (" Error when creating ", name, " broker. ")
        
        return myBroker