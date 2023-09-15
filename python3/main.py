from helper_chatGPT import *
from helper_models import *
from helper_param import *

import socket
import pickle
import threading
import requests
import struct


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server Started ......')
print('Waiting for Connection ......')
conn, addr = server_socket.accept()
print('Connection Established ......')


while True:

    # Read a frame of audio
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm)

    # If the wake word is detected
    if keyword_index >= 0:
        
        ret = {"func" : "chat_no_url" , "arg" : "Hello"}
        conn.sendall(pickle.dumps([ret] , protocol = 2))

        record_audio("recording.wav", audio_clip_path, RECORDING_TIME)

        auth = True
        if AUDIO_RECOG:
            auth = False
            response = requests.post(AUDIO_RECOG_API, files={'audio': open(audio_clip_path, 'rb')})
            if response.status_code == 200:
                transcription = response.json()
                if str(transcription['Detected']).lower() == str(AUDIO_AUTH_USER).lower():
                    if transcription['Sim'] < 0.8:
                        auth = True
            else:
                print('Error in Audio recog:', response.status_code)
                
        
        if auth :
            # ret = {"func" : "chat_no_url" , "arg" : "Give me some time, I am working on it"}
            # start_time = time.time()
            # conn.sendall(pickle.dumps([ret] , protocol = 2))
            
            func, arg = process_audio(model, TRANSCRIBE_API)

            if func == "enable":
                AUDIO_RECOG = True
            
            if func == "disable":
                AUDIO_RECOG = False

            ret = {"func" : func , "arg" : arg}
            conn.sendall(pickle.dumps([ret] , protocol = 2))
        else:
            ret = {"func" : "chat_no_url" , "arg" : "You are not authorized user"}
            conn.sendall(pickle.dumps([ret] , protocol = 2))
    
