#! /home/sougato97/miniconda3/envs/hri/bin/python
# -*- encoding: UTF-8 -*-

import whisper
from voice_auth import *
from utils import *
import os
# import sys




def main():
    # store the keys 
    openai_key = os.environ["OPENAI_API_KEY"]
    pyannote_key = os.environ["PYANNOTE_API_KEY"]
    voice_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/"
    # Importing the Whisper model
    model = whisper.load_model("medium.en")
    print("Whisper model import success")
    
    # ******* Prev Flow of command, using a while 1 *******
    while (1):
        flag = input("Please give the input according to the provided options : \nUser Registration - 1 \nUser evaluate - 2 \nBypass Auth & use as guest - 3\nExit -4")
        if (flag == '1'):
            register_user(pyannote_key,voice_clip_path,model)
            continue
        elif (flag == '2'):
            print("What do you want to know?")
            record_audio(voice_clip_path, "recording.mp3", 7)
            print("Question recorded!!")
            # Checking the user
            flag = user_auth(voice_clip_path, "recording.mp3", pyannote_key)
            if (flag):
                question = transcribe(voice_clip_path + "recording.mp3",model)
                gpt(question,model,openai_key,voice_clip_path)
            else:
                writing_response_to_json_file("You are not an authorized user")
                # subprocess.run(['bash', 'chatgpt.sh'])
                subprocess.run(['python2','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
        elif (flag == '3'):
            print("What do you want to know?")
            record_audio(voice_clip_path, "recording.mp3", 7)
            print("Question recorded!!")
            question = transcribe(voice_clip_path + "recording.mp3",model)
            gpt(question,model,openai_key,voice_clip_path)          
        elif (flag == '4'):
            return
        else:
            continue
            # socket_connect("You are not an authorized user")
    # **************************** End **************************** 

if __name__ == "__main__":
    main()



# **** Name Suggestions ****
# Aiko - Japanese for “beloved child”
# Amelia - Latin for “industrious”
# Ava - Latin for “life”
# Buddy - English for “friend”
# Eva - Hebrew for “life”
# Kai - Hawaiian for “sea”
# Lila - Arabic for “night”
# Luna - Latin for “moon”
# Nova - Latin for “new”
# Zara - Arabic for “princess”



