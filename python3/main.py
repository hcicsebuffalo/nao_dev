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


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"
porc_model_path_ppn = current_path[:-7] + "models/hey_aiko_ja_linux_v2_1_0.ppn"
porc_model_path_pv = current_path[:-7] + "models/porcupine_params_ja.pv"

#print(yml_path)

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param , "-----------")
    except yaml.YAMLError as e:
        print(e, "-------")
    
HOST = '127.0.0.1'
PORT = param["py_port"]

if param["model"] == "Whisper":
    # Load the whisper model 
    model = whisper.load_model("large")
    print("Whisper model import success")
else:
    model = None
    print("Google APIs in use .. ")

#model = whisper.load_model("large")

# Listening -----
if param["use_wake_flag"] == 1:
    pico_key = os.environ["PICOVOICE_API_KEY"]
    porcupine = pvporcupine.create(access_key=pico_key, keyword_paths=[porc_model_path_ppn], model_path= porc_model_path_pv)
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
        request = conn.recv(1024).decode()
        
        if request:
            print('Request : ------------------------- \n')
            #print( request)
            #print('\n')
            out = process_audio(model)
            print("Response : \n")
            print(out)
            ret = out
            print('\n')
            conn.sendall(pickle.dumps([ret] , protocol = 2))

def wake_word():
    global conn
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
            ret = "Hello"
            conn.sendall(pickle.dumps([ret] , protocol = 2))
            print('Request : ------------------------- \n')
            #print( request)
            #print('\n')
            out = process_audio(model)
            print("Response : \n")
            print(out)
            ret = out
            print('\n')
            conn.sendall(pickle.dumps([ret] , protocol = 2))

            # break

gpt_thread = threading.Thread(target= gpt_socket )
wake_wrd_thread = threading.Thread(target= wake_word)

gpt_thread.start()
wake_wrd_thread.start()

