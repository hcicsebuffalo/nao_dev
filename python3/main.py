import socket
import pickle
import pyaudio
import wave
import os
from google.cloud import speech
import whisper
import io
import openai
import json
import os
from utils import *
import yaml
import pvporcupine
import struct
import sys
import threading
import time


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"
#porc_model_path_ppn = current_path[:-7] + "models/hey_aiko_ja_linux_v2_1_0.ppn"
porc_model_path_ppn = current_path[:-7] + "models/hello-kai_en_linux_v2_2_0.ppn"
#porc_model_path_pv = current_path[:-7] + "models/porcupine_params_ja.pv"

#print(yml_path)

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        #print(param , "-----------")
    except yaml.YAMLError as e:
        print(e, "-------")
    
HOST = '127.0.0.1'
PORT = param["py_port"]
TRANSCRIBE_API = param["transcribe_api"]
AUDIO_RECOG = param["audio_recog"]
AUDIO_RECOG_API = param["audio_authen_api"]
AUDIO_AUTH_USER = param["audio_authe_user"]

if param["model"] == "Whisper":
    # Load the whisper model 
    model = whisper.load_model("medium.en")
    print("Whisper model import success")

elif param["model"] == "Server":
    model = "Server"
    #print("Server will be used for ml models")
else:
    model = None
    #print("Google APIs in use .. ")

#model = whisper.load_model("large")

# Listening -----
if param["use_wake_flag"] == 1:
    pico_key = os.environ["PICOVOICE_API_KEY"]
    #porcupine = pvporcupine.create(access_key=pico_key, keyword_paths=[porc_model_path_ppn], model_path= porc_model_path_pv)
    porcupine = pvporcupine.create(access_key=pico_key, keyword_paths=[porc_model_path_ppn])
    
    # Initialize PyAudio and open a stream
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

# ------


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server Started ......')
print('Waiting for Connection ......')

conn, addr = server_socket.accept()
print('Connection Established ......')

def gpt_socket():
    global conn, model
    while True:
        request = conn.recv(2048).decode()
        
        if request:
            print('Request : ------------------------- \n')
            #print( request)
            #print('\n')
            record_audio(file_path, audio_clip_path, 7)
            func, arg = process_audio(model, None)
            print("Response : \n")
            print(out)
            #ret = out
            ret = {"func" : func , "arg" : arg}
            print('\n')
            conn.sendall(pickle.dumps([ret] , protocol = 2))

out = None
# def get_response_gpt():
#     global out, model
#     out = process_audio(model, None)
#     return

#get_res_thread = threading.Thread(target= get_response_gpt)

def wake_word():
    global conn , out, get_res_thread , AUDIO_RECOG
    print("Listening for wake word...")
    while True:
        # Read a frame of audio
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        # Process the frame with Porcupine
        keyword_index = porcupine.process(pcm)

        # If the wake word is detected, break the loop
        if keyword_index >= 0:
            print("Wake word detected!")
            ret = {"func" : "chat_no_url" , "arg" : "Hello"}
            #start_time = time.time()
            conn.sendall(pickle.dumps([ret] , protocol = 2))

            record_audio(file_path, audio_clip_path, 5)

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
        

# gpt_thread = threading.Thread(target= gpt_socket )
wake_wrd_thread = threading.Thread(target= wake_word)

# gpt_thread.start()
wake_wrd_thread.start()



# get_res_thread.start()
# first = True
# wait = 8
# while get_res_thread.is_alive():
#     delay = time.time() - start_time
#     if delay > wait:
#         if first:
#             first = False
#             start_time = time.time()
#             ret = "Working on it"
#             wait = 15
#             conn.sendall(pickle.dumps([ret] , protocol = 2))
#         else:
#             start_time = time.time()
#             ret = "Still Working on it"
#             conn.sendall(pickle.dumps([ret] , protocol = 2))


# get_res_thread = threading.Thread(target= get_response_gpt)
# print("Response : \n \n ")
# print(out , "\n \n" )