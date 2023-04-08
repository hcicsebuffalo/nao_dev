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

HOST = '127.0.0.1'
PORT = 9791

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'

# Load the Google API client
# client = speech.SpeechClient()
# This GPT Conversation variable should be a global 
conversation=[{"role":"system","content":"You are a helpful assistant"}]
# Load the whisper model 
model = whisper.load_model("medium.en")
print("Whisper model import success")




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server is running...')

conn, addr = server_socket.accept()
print('Connected by', addr)
    
while True:
    request = conn.recv(1024).decode()
    
    if request:
        print('Request:', request)
        out = process_audio(model)
        print(out)
        conn.sendall(pickle.dumps([out] , protocol = 2))
    
    #function = handle_request(request)
    #if function:
    #    result = int(function())
    #    print(result)
    #else:
        #conn.sendall(b'Invalid request')
    #   pass 
    #conn.close()