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


# Writing the output to a json file
def writing_response_to_json_file(answer):
    sorted_output=json.dumps(answer)
    with open('/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/json_file.json', "w") as outfile:
        outfile.write(sorted_output)

def transcribe(recording_path,model):
    print("Processing the question.......")
    result = model.transcribe(recording_path)
    print("Question generated: "+result["text"])
    question=result['text']
    return question

# Function to generate chatgpt response
def gpt(question,model,openai_key,voice_clip_path):

    conversation=[{"role":"system","content":"You are a helpful assistant"}]
    # using the openai api key
    openai.api_key=openai_key

    while(True):
        conversation.append({"role":"user","content": question})
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.2,
            max_tokens=1000,
            top_p=0.9
        )
        conversation.append({"role":"assistant","content":response['choices'][0]['message']['content']})
        answer=response['choices'][0]['message']['content']
        writing_response_to_json_file(answer)
        # subprocess.run(['python','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
        subprocess.run(['bash', 'chatgpt.sh'])
        confirmation=input("Do you wish to continue asking questions? Enter Y or y for yes || Enter N or n for no: ")
        if(confirmation=='y' or confirmation=='Y'):
            print("What do you want to know? ")
            record_audio(voice_clip_path, "recording.mp3", 7)
            print("Question recorded")
            print("Transcribing audio")
            question=transcribe(voice_clip_path + "recording.mp3",model)
            print("Audio Transcribed and question generated")
            print(question)
        elif(confirmation=='n' or confirmation=='N'):
            break
        else:
            print("Please enter valid options from the following:(Y/y/N/n)")

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
    # Get the openai token from "https://platform.openai.com/account/api-keys"
    openai_key = "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"
    # Get the pyannote token from "https://huggingface.co/settings/tokens"
    # Also you have to agree to some T&C. Preferably run it 1st time on jupyter, you will get the link there itself.
    pyannote_key = "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"
    voice_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/recordings/"
    # Importing the Whisper model
    model = whisper.load_model("large")
    print("Whisper model import success")
    while (1):
        flag = input("Please give the input according to the provided options : \nUser Registration - 1 \nUser evaluate - 2 \nBypass Auth & use as guest - 3\nExit -4 \nDefault options - Any other keys")
        if (flag == '1'):
            # code not implemented
            register_user(pyannote_key,voice_clip_path)
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
                subprocess.run(['bash', 'chatgpt.sh'])
                # subprocess.run(['python','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
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







