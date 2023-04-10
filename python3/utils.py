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

file_path = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'

# Load the Google API client
# client = speech.SpeechClient()
# This GPT Conversation variable should be a global 
conversation=[{"role":"system","content":"Respond like you are Humanoid robot name Aiko. \
    Remember following information - You are working in Davis Hall in University at Buffalo, under professor Nalini Ratha. President of this university is Satish K tripathi. Dean of school of engineering in univerity at buffalo is Kemper Lewis. \
    Furnas Hall is a building at the University at Buffalo in New York that houses the School of Engineering and Applied Sciences, with classrooms, labs, offices, and research facilities. It is named after Clifford C. Furnas, a former UB professor and administrator who was an early advocate for the development of engineering programs at the university \
    Davis Hall is a building at the University at Buffalo in New York that houses the Department of Computer Science and Engineering, with classrooms, labs, offices, and research facilities. It is named after Clifford C. Furnas, a former UB professor and administrator who was instrumental in the development of computer science programs at the university           \
    Capen Hall is a historic building located on the North Campus of the University at Buffalo in Buffalo, New York. It was completed in 1923 and named after the university's first chancellor, Samuel P. Capen. Originally, Capen Hall served as the main administrative building for the university. Today, it houses a variety of offices, including the offices of the President and Provost, the Office of Admissions, and the Office of Financial Aid. The building is known for its impressive architecture, featuring a large central dome, sweeping staircases, and grand hallways\
    Jarvis Hall at the University at Buffalo was named after Gregory Jarvis, a UB alumnus who died in the 1986 Challenger space shuttle disaster. Jarvis graduated from UB's electrical engineering program in 1967 and was selected to fly on Challenger STS 51-L as a payload specialist. Today, Jarvis Hall stands as a tribute to Jarvis's legacy and to UB's commitment to honoring its accomplished alumni.      \
    Here onwards just give responses like humanoid robot and nothing else."}]
# Load the whisper model 
# model = whisper.load_model("medium.en")
# # Audio clip name 
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
    #print("------------------------" , file_path)
    
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
        question = result.alternatives[0].transcript
        
        if "How can I help you" in question:
            question = question.replace("How can I help you", " ")
        print(" Transcribed Text: " + question)

        #print(" Transcribed Text: {}".format(result.alternatives[0].transcript))
        out += question
        
    return out

def transcribe_whisper(recording_path,model):
    print(" Transcribing ")
    result = model.transcribe(recording_path) ## exception handling
    question = result['text']
    if "How can I help you" in question:
        question = question.replace("How can I help you", " ")
    print(" Transcribed Text: " + question)
    return question

def gptReq_old(question):
    print(" requesting gpt model for response ")
    #this is the api key
    openai.api_key=openai_key
    # question=input("Enter your question: ")
    completion = openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
    response=completion.choices[0]['text']

    # socket_connect(response)
    #writing the output to a json file
    sorted_output = json.dumps(response)
    return sorted_output

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
    return answer


def process_audio(model):
    record_audio(file_path, audio_clip_path, 7)
    if model != None:
        out = transcribe_whisper(audio_clip_path,model)
    else:
        out = transcribe_google_api()
        
    prompt = ""#". Give answer in two sentence"
    out += prompt
    if "dance" in out.lower():
        ans = "Dance"
    else:
        ans = gptReq(out)
    return ans


