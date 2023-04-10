import socket
import pickle
import pyaudio
import wave
import os
from google.cloud import speech
import whisper
import os
import io
import openai
import json
import os
from utils import *
import yaml


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"
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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server Started ......')
print('Waiting for Connection ......')

conn, addr = server_socket.accept()
print('Connection Established ......')
    
while True:
    request = conn.recv(1024).decode()
    
    if request:
        print('Request : ------------------------- \n')
        print( request)
        print('\n')
        out = process_audio(model)
        print("Response : \n")
        print(out)
        print('\n')
        conn.sendall(pickle.dumps([out] , protocol = 2))