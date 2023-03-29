from base import *
import sys
import os
import csv

class leds(base):
    
    def __init__(self, ip, port):
        base.__init__(self)
        self.ip = ip
        self.port = port
        self.proxy_name_led = "ALLeds"
        self.leds = None
        
    
    def initLEDS(self):
        self.leds = self.connect(self.proxy_name_led , self.ip, self.port)


    # 1 -> rastanao.animation(1, 2)
    # 2 -> rotateEyes
    # 3 -> randomEyes
    def animation(self, type, duration):
        if type == 1:
            self.leds.rasta(duration)
        if type == 2:
            self.leds.rotateEyes(0x000000FF, 1, duration)
        if type == 3:
            self.leds.randomEyes(duration)
        if type == 4:
            self.leds.earLedsSetAngle(270, duration, False)
    
    def ledStartListening(self):
        self.leds.on("EarLeds")
    
    def ledStopListening(self):
        self.leds.off("EarLeds")






# TODO 
""""
createGroupledStartListening

earLedsSetAngle -. ear animation

fade -. leds

fadeListRGB

fadeRGB

off


listLEDs

on

randomEyes

rasta

rotateEyes

setIntensity

"""