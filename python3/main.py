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

openai_key = os.environ["OPENAI_API_KEY"]

file_path = "/home/hri/dev/python3"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'

client = speech.SpeechClient()

#This GPT Conversation variable should be a global 
conversation=[{"role":"system","content":"You are a helpful assistant"}]

# Function to record audio
def record_audio(path, filename, duration):
    # Set the parameters for the audio stream
    print(" Recording audio ")
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

def transcribe_google_api():
    print(" Transcribing ")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'

    client = speech.SpeechClient()

    file_name = "recording.wav"
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)


    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        audio_channel_count=1,
        language_code="en-US",
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})
    # Reads the response
    out = ''
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        out += str(result.alternatives[0].transcript + ' ')
        
    return out

def transcribe_whisper(recording_path,model):
    print(" Transcribing ")
    result = model.transcribe(recording_path) ## exception handling
    print(" Transcribed Text: "+ result["text"])
    question = result['text']
    return question

# def gptReq(question):
#     print(" requesting gpt model for response ")
#     #this is the api key
#     openai.api_key=openai_key
#     # question=input("Enter your question: ")
#     completion = openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
#     response=completion.choices[0]['text']

#     # socket_connect(response)
#     #writing the output to a json file
#     sorted_output = json.dumps(response)
#     return sorted_output

# Function to generate chatgpt response
def gptReq(question):

    # using the openai api key
    openai.api_key=openai_key

    conversation.append({"role":"user","content": question})
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.2,
        max_tokens=1000,
        top_p=0.9
    )
    conversation.append({"role":"assistant","content":response['choices'][0]['message']['content']})
    answer = response['choices'][0]['message']['content']
    #writing the output to a json file
    sorted_output = json.dumps(answer)
    return sorted_output


def process_audio():
    record_audio(file_path, "recording.wav", 7)
    # out = transcribe_google_api()
    out = transcribe_whisper("recording.wav",model)
    if "dance" in out.lower():
        ans = "Dance"
    else:
        ans = gptReq(out)
    return ans


def handle_request(request):
    if request == 'chatGPT':
        return chatGPT
    else:
        return None

HOST = '127.0.0.1'
PORT = 9993
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
model = whisper.load_model("medium.en")
print('Server is running...')

conn, addr = server_socket.accept()
print('Connected by', addr)
    
while True:
    request = conn.recv(1024).decode()
    
    if request:
        print('Request:', request)
        out = process_audio()
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