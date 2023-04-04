"""
tts class object for text to speech conversion. class has following functions

    sayText(text) ->    its takes string input and pass it to Naos speaker
    
    setVolume(volume)-> set volume from 0 to 100

    initTTS -> to initialise proxy
    
    info() ->           provide info about nao
    
    RunSpeech() ->      This function runs a speech script saves as a *.csv file. Column
                        1contains the time in seconds, Column 2 contains the TTS input. This
                        function requires a TTS proxy.

"""

from base import *
import sys
import os
import csv

class tts(base):
    
    def __init__(self, ip, port):
        base.__init__(self)
        self.ip = ip
        self.port = port
        self.proxy_name_tts = "ALTextToSpeech"
        self.tts = None
        self.proxy_name_atts = "ALAnimatedSpeech"
        self.tts = None
        self.atts = None
        
    
    def initTTS(self):
        self.tts = self.connect(self.proxy_name_tts , self.ip, self.port)
        self.atts = self.connect(self.proxy_name_atts , self.ip, self.port)

    def sayText(self, text):
        self.atts.say(text)
    
    def setVolume(self, volume = 70):
        self.tts.setParameter("volume", volume)
        self.tts.setVolume(volume//100)

    def info(self):
        out = dict()
        out["voice"] = self.tts.getVoice()
        out["supported_languages"] = self.tts.getSupportedLanguages()
        out["available_voices"] = self.tts.getAvailableVoices()
        out["available_language"] = self.tts.getAvailableLanguages()
        out["volume"] = self.tts.getVolume()

        return out


## TODO:  Need to test
    ###########################################################################
    ## This function runs a speech script saves as a *.csv file. Column 1
    ## contains the time in seconds, Column 2 contains the TTS input. This
    ## function requires a TTS proxy.
    ###########################################################################

    def RunSpeech(self, file_path):
        """ file_name is the name containing the speech script."""
        list_path = sys.path
        file_found=False
        
        if os.path.exists(file_path):
            filefound=True
            
        if not filefound:
            print ("Speech file "+str(file_path)+" not found")
            return

        try:
            script_reader = csv.reader(open(file_path, 'rb'))
        except:
            print ("Failed to load script reader")
            return
        
        cur_line = script_reader.next()
        start_time = time()
        while True:
            try:
                cur_line = script_reader.next()
            except:
                break
            while float(cur_line[0])> (time()-start_time):
                time.sleep(0.1)
            self.tts.say(cur_line[1])


