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
from PIL import Image, ImageDraw, ImageFont
import cloudinary
import cloudinary.uploader
import cloudinary.api
import threading
import time

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
        self.proxy_name_tablet = "ALTabletService"
        self.display_thread_1 = threading.Thread(target= self.displayURL )
        self.display_thread_2 = threading.Thread(target= self.displayURL )
        self.last_used_thread = 1
        self.url = None
        
    
    def initTTS(self):
        self.tts = self.connect(self.proxy_name_tts , self.ip, self.port)
        self.atts = self.connect(self.proxy_name_atts , self.ip, self.port)
        self.tablet = self.connect(self.proxy_name_tablet , self.ip, self.port)
    
    def give_url(self, text):
        # Set image properties
        image_width = 1280
        image_height = 800
        background_color = (255, 255, 255)  # White
        text_color = (0, 0, 0)  # Black
        font_size = 60
        # Load a font
        font = ImageFont.truetype("FreeSans.ttf", font_size)
        
        max_text_width = image_width - 20  # Adjust padding as needed
        max_text_height = image_height - 20  # Adjust padding as needed

        # Create a blank image
        image = Image.new("RGB", (image_width, image_height), background_color)
        draw = ImageDraw.Draw(image)

        
        # Wrap the text into multiple lines
        lines = []
        current_line = ""
        words = text.split()
        for word in words:
            if draw.textsize(current_line + " " + word, font=font)[0] <= max_text_width:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())

        # Adjust font size if needed to fit the lines
        while any(draw.textsize(line, font=font)[0] > max_text_width for line in lines):
            font_size -= 1
            font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate the text position
        total_text_height = sum(draw.textsize(line, font=font)[1] for line in lines)
        text_y = (image_height - total_text_height) // 2

        # Draw the text on the image
        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            text_x = (image_width - text_width) // 2
            draw.text((text_x, text_y), line, font=font, fill=text_color)
            text_y += text_height

        # Save the image to a file
        image.save("text_image.png")

        cloudinary.config(
        cloud_name = 'dqflv49oz', 
        api_key = '958546157725331', 
        api_secret = 'ML519Ik_1kbfPo9tpkSvSifrUoc' 
        )

        response = cloudinary.uploader.upload("text_image.png")
        image_url = response['secure_url']

        return image_url


    def give_url_with_image(self, input_image_path, text):
        # Set image properties
        image_width = 1280
        image_height = 800
        background_color = (255, 255, 255)  # White
        text_color = (0, 0, 0)  # Black
        font_size = 60

        # Load a font
        font =ImageFont.truetype("FreeSans.ttf", font_size)

        max_text_width = image_width // 2 - 40  # Adjust padding as needed for left side
        max_text_height = image_height - 20  # Adjust padding as needed

        # Create a blank image
        image = Image.new("RGB", (image_width, image_height), background_color)
        draw = ImageDraw.Draw(image)

        # Load the input image
        input_img = Image.open(input_image_path)

        # Resize the input image to fit on the left side
        input_img = input_img.resize((image_width // 2, image_height))

        # Paste the input image on the left side of the output image
        image.paste(input_img, (0, 0))

        # Wrap the text into multiple lines
        lines = []
        current_line = ""
        words = text.split()
        for word in words:
            if draw.textsize(current_line + " " + word, font=font)[0] <= max_text_width:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())

        # Adjust font size if needed to fit the lines
        while any(draw.textsize(line, font=font)[0] > max_text_width for line in lines):
            font_size -= 1
            font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate the text position
        total_text_height = sum(draw.textsize(line, font=font)[1] for line in lines)
        text_y = (image_height - total_text_height) // 2

        # Draw the text on the right side of the image
        text_x = image_width // 2 + 20  # Place the text on the right side with padding
        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            draw.text((text_x, text_y), line, font=font, fill=text_color)
            text_y += text_height

        # Save the image to a file
        image.save("output_image.png")
        
        cloudinary.config(
        cloud_name = 'dqflv49oz', 
        api_key = '958546157725331', 
        api_secret = 'ML519Ik_1kbfPo9tpkSvSifrUoc' 
        )

        response = cloudinary.uploader.upload("output_image.png")
        image_url = response['secure_url']

        return image_url


    def give_logo_url(self):
        
        cloudinary.config(
        cloud_name = 'dqflv49oz', 
        api_key = '958546157725331', 
        api_secret = 'ML519Ik_1kbfPo9tpkSvSifrUoc' 
        )

        response = cloudinary.uploader.upload("logo.png")
        image_url = response['secure_url']

        return image_url

    

    def displayURL(self ):
        self.tablet.showWebview( str(self.url))
        time.sleep(25)
        self.tablet.hideWebview()
    
    def displayURL_nothread(self):
        self.tablet.showWebview( str(self.url))

    def display_givenURL(self, url):
        self.tablet.showWebview( str(url))

    def show_web(self):
        if self.last_used_thread == 1:
            self.display_thread_2.start()
            self.display_thread_1 = threading.Thread(target= self.displayURL )
            self.last_used_thread = 2
        else:
            self.display_thread_1.start()
            self.display_thread_2 = threading.Thread(target= self.displayURL )
            self.last_used_thread = 1

    def tab_reset(self):
        img_url = self.give_logo_url()
        self.tablet.showWebview( str(img_url))

    def sayText(self, text):
        url = self.give_url( text)
        self.url = str(url)
        #self.show_web()
        self.displayURL_nothread()
        #time.sleep(4)
        self.atts.say(text)

    def sayText_no_url(self, text):
        url = self.give_url( text)
        self.atts.say(text)
    
    def sayText_with_image(self, image_path, text):
        url = self.give_url_with_image(image_path, text)
        self.url = str(url)
        #self.show_web()
        self.displayURL_nothread()
        #time.sleep(4)
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


