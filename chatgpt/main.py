#! /home/sougato97/miniconda3/envs/hri/bin/python
# -*- encoding: UTF-8 -*-

import whisper
import openai
import json
import pyaudio
import wave
import os
from voice_auth import *
import subprocess
import socket
# import sys

# store the keys 
# Get the openai token from "https://platform.openai.com/account/api-keys"
openai_key = ""
# Get the pyannote token from "https://huggingface.co/settings/tokens"
# Also you have to agree to some T&C. Preferably run it 1st time on jupyter, you will get the link there itself.
pyannote_key = ""

voice_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/"

# Function to record audio
def record_audio(path, filename, duration):
    # Set the parameters for the audio stream
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    
    # Initialize the PyAudio object
    p = pyaudio.PyAudio()
    
    # Open the audio stream
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    
    frames = []
    
    # Record the audio for the specified duration
    for i in range(int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    
    # Terminate the PyAudio object
    p.terminate()
    
    # Save the recorded audio as a WAV file
    file_path = os.path.join(path, filename)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert the WAV file to MP3
    # os.system(f"ffmpeg -i {filename} -acodec libmp3lame -aq 4 {filename[:-4]}.mp3")

def transcribe(openai_key,model):
    # model = whisper.load_model("large")
    print("Processing the question.......")
    result = model.transcribe("/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/recording.mp3")
    print("Question generated: "+result["text"])

    question=result['text']

    #this is the api key
    openai.api_key=openai_key
    # question=input("Enter your question: ")
    completion=openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
    response=completion.choices[0]['text']


    # socket_connect(response)
    #writing the output to a json file
    sorted_output=json.dumps(response)
    with open('/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/json_file.json', "w") as outfile:
        outfile.write(sorted_output)   

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
    
    model = whisper.load_model("large")
    print("Whisper model Import success")
    while (1):

        print("What do you want to know?")
        # Example usage: Record 7 seconds of audio and save it as "recording.mp3"
        record_audio(voice_clip_path, "recording.mp3", 7)
        print("Question recorded!!")
        flag = user_auth(voice_clip_path, "recording.mp3", pyannote_key)
        # flag = 1
        print("the value of flag is:",flag)
        # flag = user_auth(voice_clip_path, "recording_subhobrata_1.mp3", pyannote_key)
        if (flag):
            transcribe(openai_key,model)
        else:
            sorted_output=json.dumps("You are not an authorized user")
            with open('/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/json_file.json', "w") as outfile:
                outfile.write(sorted_output)
            # socket_connect("You are not an authorized user")

        # Dont know why this code is not working
        # subprocess.run(['python', 'nao_say.py']) 
        subprocess.run(['bash', 'chatgpt.sh'])
        # exec(open("nao_say.py").read())
        execute_flag = input("Do you want the code to exit? Yes, press:1 ; No, press:Any key ")
        if (execute_flag == '1'):
            return
        else:
            continue

if __name__ == "__main__":
    main()







