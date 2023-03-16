#! /home/sougato97/miniconda3/envs/hri/bin/python
# -*- encoding: UTF-8 -*-

import whisper
from voice_auth import *
from utils import *
import os
# import sys

def socket_connect(response):
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # bind the socket to a public host, and a well-known port
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(5)

    while True:
        # establish a connection
        clientsocket, addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))

        msg = response + "\r\n"
        clientsocket.send(msg.encode('ascii'))
        clientsocket.close()    


def main():
    # store the keys 
    openai_key = os.environ["OPENAI_API_KEY"]
    pyannote_key = os.environ["PYANNOTE_API_KEY"]
    voice_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/"
    # Importing the Whisper model
    model = whisper.load_model("medium.en")
    print("Whisper model import success")
    while (1):
        flag = input("Please give the input according to the provided options : \nUser Registration - 1 \nUser evaluate - 2 \nBypass Auth & use as guest - 3\nExit -4")
        if (flag == '1'):
            # code not implemented
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

if __name__ == "__main__":
    main()







