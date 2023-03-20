#! /home/sougato97/miniconda3/envs/hri/bin/python
# -*- encoding: UTF-8 -*-

import whisper
from voice import *
from utils import *
import os
# import sys

def nao_intro(json_file_path):
    text_data = '''Welcome to you all, my name is Aiko & I am a proud member of this lab. My friends are in the progress of making me intelligent day by day. 
        I have limited capabilities but I can be you assistant by helping you with your queries. I can also present a dance if you like.'''
    # text_data = "Welcome to you all."
    writing_response_to_json_file(text_data,json_file_path)
    subprocess.run(['python2','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])


def main():
    # store the keys 
    openai_key = os.environ["OPENAI_API_KEY"]
    pyannote_key = os.environ["PYANNOTE_API_KEY"]
    voice_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/"
    dance_file_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/movement/dance_main.py"
    nao_say_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py"
    json_file_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/json_file.json"
    # Importing the Whisper model
    model = whisper.load_model("medium.en") ## exception handling
    print("Whisper model import success")
    nao_intro(json_file_path)


    # record_audio(voice_clip_path, "extract_command.mp3")
    command = get_command(voice_clip_path, model, nao_say_path, json_file_path)
    if command == 1:
        print("What do you want to know?")
        record_audio(voice_clip_path, "recording.mp3")
        print("Question recorded!!")
        question = transcribe(voice_clip_path + "recording.mp3",model)
        gpt(question,model,openai_key,voice_clip_path,nao_say_path,json_file_path) 
    elif command == 2:
        subprocess.run(['python2',dance_file_path])      

    # ******* Prev Flow of command, using a while 1 *******
    # while (1):
    #     flag = input("Please give the input according to the provided options : \nUser Registration - 1 \nUser evaluate - 2 \nBypass Auth & use as guest - 3\nExit -4")
    #     if (flag == '1'):
    #         register_user(pyannote_key,voice_clip_path,model, nao_say_path)
    #         continue
    #     elif (flag == '2'):
    #         print("What do you want to know?")
    #         # record_audio_with_fixed_duration(voice_clip_path, "recording.mp3", 7)
    #         record_audio(voice_clip_path, "recording.mp3")
    #         print("Question recorded!!")
    #         # Checking the user
    #         flag = user_auth(voice_clip_path, "recording.mp3", pyannote_key)
    #         if (flag):
    #             question = transcribe(voice_clip_path + "recording.mp3",model)
    #             gpt(question,model,openai_key,voice_clip_path)
    #         else:
    #             writing_response_to_json_file("You are not an authorized user",json_file_path)
    #             # subprocess.run(['bash', 'chatgpt.sh'])
    #             subprocess.run(['python2','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
    #     elif (flag == '3'):
    #         print("What do you want to know?")
    #         # record_audio_with_fixed_duration(voice_clip_path, "recording.mp3", 7)
    #         record_audio(voice_clip_path, "recording.mp3")
    #         print("Question recorded!!")
    #         question = transcribe(voice_clip_path + "recording.mp3",model)
    #         gpt(question,model,openai_key,voice_clip_path)          
    #     elif (flag == '4'):
    #         return
    #     else:
    #         continue
            # socket_connect("You are not an authorized user")
    # **************************** End **************************** 

if __name__ == "__main__":
    main()






