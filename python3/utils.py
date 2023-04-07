import socket
import pickle
import pyaudio
import wave
import os
from google.cloud import speech
# import whisper
import os
import io
import openai
import json
import os

openai_key = os.environ["OPENAI_API_KEY"]


# file_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/python3"
# file_path = "/home/hri/dev/python3"
# file_path = "/home/hri/Human_Robot_Interaction/nao_dev/python3"
file_path = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'

# Load the Google API client
# client = speech.SpeechClient()
# This GPT Conversation variable should be a global 
conversation=[{"role":"system","content":"You are a helpful assistant"}]
# Load the whisper model 
# model = whisper.load_model("medium.en")
# # Audio clip name 
# audio_clip_path = "/home/sougato97/Human_Robot_Interaction/nao_dev/python3/recording.wav"
# audio_clip_path = "/home/hri/Human_Robot_Interaction/nao_dev/python3/recording.wav"
audio_clip_path = os.getcwd() + "/recording.wav"



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
    print("------------------------" , file_path)
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
    print(" Transcribed Text: " + result["text"])
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
    # sorted_output = json.dumps(answer)
    return answer


def process_audio(model):
    record_audio(file_path, audio_clip_path, 7)
    # out = transcribe_google_api()
    out = transcribe_whisper(audio_clip_path,model)
    prompt = "Give answer in two sentences. Respond like you are Humanoid robot name Aiko. \
    Decription about yourself. You are working in Davis Hall in University at Buffalo, under professor \
    Nalini Ratha. President of this university is Satish K tripathi. Dean of school of engineering in univerity at \
    buffalo is Kemper Lewis. Here Onwards just give responses and nothing else. "
    out = prompt  + out
    if "dance" in out.lower():
        ans = "Dance"
    else:
        ans = gptReq(out)
    return ans


