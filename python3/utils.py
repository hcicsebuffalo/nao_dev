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
# from docx import Document
import re
import googlemaps
import requests

openai_key = os.environ["OPENAI_API_KEY"]
proc_audio_bool = False
file_path = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_secret_key.json'
API_KEY = 'AIzaSyCkPcrm28UTgbei5RZ0hXREM1dKKtVOci0'

import requests


path = "../content.txt"
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

prompt = read_text_file(path)

conversation=[{"role":"system","content":prompt}]

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
    print(" Google API Transcribing ")
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
        if "Can I help you" in question:
            question = question.replace("Can I help you", " ")
        if "Hello" in question:
            question = question.replace("Hello", " ")
        print(" Transcribed Text: " + question)

        #print(" Transcribed Text: {}".format(result.alternatives[0].transcript))
        out += question
        
    return out

def transcribe_whisper(recording_path, model):
    print(" Whisper Transcribing ")
    result = model.transcribe(recording_path) ## exception handling
    print("Transcription Done")
    question = result['text']
    question = str(question).lower()
    if "How can I help you".lower() in question:
        question = question.replace("How can I help you".lower(), " ")
    if "Can I help you".lower() in question:
        question = question.replace("Can I help you".lower(), " ")
    if "Hello".lower() in question:
        question = question.replace("Hello".lower(), " ")
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
        top_p=0.2
    )
    conversation.append({"role":"assistant","content":response['choices'][0]['message']['content']})
    answer = response['choices'][0]['message']['content']
    return answer



functions = [
        {
            "name": "get_directions",
            "description": "Give direction to some location. ",
            "parameters": {
                "type": "object",
                "properties": {
                    "end_location": {
                        "type": "string",
                        "description": "Location person wants to go to. This is end location. This location can be in University at buffalo",
                    },
                    "start_location": {
                        "type": "string",
                        "description": "This is start location person to start journey from. Return None if start location is not specified ",
                    },
                },
                "required": ["end_location"],
            },
        }, 

        {
            "name": "president_ub",
            "description": "who is president of University of Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }, 
        
        {
            "name": "chair_ub",
            "description": "who is Chair of Computer Science department of University of Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }, 

        {
            "name": "provost_ub",
            "description": "who is Provost of University of Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

        {
            "name": "Dean_ub",
            "description": "who is Dean of school of engineering and applied science of University of Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        
        {
            "name": "VPR_ub",
            "description": "who is VPR, Vice President for Research, of University of Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

        {
            "name": "Intro",
            "description": "When someone ask to introduce yourself with questions like introduce yourself or Tell me something about yourself. Dont trigger when someask anything else ",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

        {
            "name": "Coffee",
            "description": "Where Can I find best coffee shop at University at Buffalo",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

        {
            "name": "Disable",
            "description": "When someone ask to disable authentication i.e to stop audio authentication",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

        {
            "name": "Enable",
            "description": "When someone ask to enable authentication i.e to start audio authentication",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },

    ]


def VPR_ub():
    return " Dr. Venu Govindraju is Vice President of Research and Economic Developement at the University at Buffalo. "

def Dean_ub():
    return "Dr. Kemper Lewis is Dean of School of Engineering and Applied Sciences at the University at Buffalo."

def provost_ub():
    return " Dr. Scott Weber is Provost at the University at Buffalo."

def chair_ub():
    return " Dr. Jinhui Xu is a Chair of CSE department at the University at Buffalo."

def president_ub():
    return " Dr. Satish Tripathi is President of the University at Buffalo."

def intro():
    return ""

def enable():
    return ""

def disable():
    return ""

def Coffee():
    return get_directions("Davis Hall, University at Buffalo", "Student Union, University at Buffalo")

def get_directions(start_location, end_location):
    api_key = API_KEY
    gmaps = googlemaps.Client(key=api_key)

    # Geocode the start and end locations to get their latitude and longitude
    start_geocode = gmaps.geocode(start_location)
    end_geocode = gmaps.geocode(end_location)

    if not start_geocode or not end_geocode:
        return "Error: Invalid start or end location."

    start_latlng = start_geocode[0]['geometry']['location']
    end_latlng = end_geocode[0]['geometry']['location']

    # Get directions between the start and end locations
    directions = gmaps.directions(start_location, end_location, mode="walking")

    map_image_url = f"https://maps.googleapis.com/maps/api/staticmap?" \
                    f"size=1200x1800&" \
                    f"markers=color:red|label:S|{start_latlng['lat']},{start_latlng['lng']}&" \
                    f"markers=color:green|label:E|{end_latlng['lat']},{end_latlng['lng']}&" \
                    f"path=color:blue|enc:{directions[0]['overview_polyline']['points']}&" \
                    f"key={api_key}"

    return  map_image_url

def get_directions_old(start_location, end_location):
    api_key = API_KEY
    gmaps = googlemaps.Client(key=api_key)

    # Geocode the start and end locations to get their latitude and longitude
    start_geocode = gmaps.geocode(start_location)
    end_geocode = gmaps.geocode(end_location)

    if not start_geocode or not end_geocode:
        return "Error: Invalid start or end location."

    start_latlng = start_geocode[0]['geometry']['location']
    end_latlng = end_geocode[0]['geometry']['location']

    # Get directions between the start and end locations
    directions = gmaps.directions(start_location, end_location, mode="walking")

    # if not directions:
    #     return "Error: No directions found."

    # # Extract and format the steps of the directions
    # steps = directions[0]['legs'][0]['steps']
    # directions_text = "Directions:\n"

    # total_distance = 0  # Track the total walking distance

    # for step in steps:
    #     # Remove HTML tags using regular expressions
    #     html_tags_removed = re.sub('<.*?>', '', step['html_instructions'])
    #     directions_text += html_tags_removed + "\n"

    #     # Get the distance of the step and convert it from meters to kilometers
    #     distance = step['distance']['value']
    #     distance_km = distance / 1000.0

    #     # Append the distance of the step to the directions text
    #     directions_text += f"Distance: {distance_km:.2f} km\n\n"

    #     # Add the distance of the step to the total distance
    #     total_distance += distance

    # # Convert the total distance from meters to kilometers
    # total_distance_km = total_distance / 1000.0

    # # Append the total walking distance to the directions text
    # directions_text += f"Total walking distance: {total_distance_km:.2f} km\n"

    # Generate a static map image with the start and end markers and the route
    
    map_image_url = f"https://maps.googleapis.com/maps/api/staticmap?" \
                    f"size=1400x800&" \
                    f"markers=color:red|label:S|{start_latlng['lat']},{start_latlng['lng']}&" \
                    f"markers=color:green|label:E|{end_latlng['lat']},{end_latlng['lng']}&" \
                    f"path=color:blue|enc:{directions[0]['overview_polyline']['points']}&" \
                    f"key={api_key}"

    return map_image_url


def check_functions_question(question):
    flag = 0
    name = None
    function_mapping = {"Intro" : "intro", "Coffee": "Coffee", "Enable": "enable","Disable": "disable"}  
    key_list = list(function_mapping.keys())
    val_list = list(function_mapping.values())
    for item in val_list:
        if item.lower() in question.lower():
            function_name = key_list[val_list.index(item)]
            flag = 1            
    return function_name,flag   

def check_functions_answer(answer):
    flag = 0
    name = None
    function_mapping = {"VPR_ub" : "Govindaraju", "president_ub" : "Satish", "chair_ub": "Jinhui", "provost_ub": "Scott" , "Dean_ub": "Kemper"}  
    key_list = list(function_mapping.keys())
    val_list = list(function_mapping.values())
    for item in val_list:
        if item.lower() in answer.lower():
            function_name = key_list[val_list.index(item)]
            flag = 1            
    return function_name,flag       

def gptReq_withfunctions(question):
    # using the openai api key
    # openai.api_key=openai_key
    #response_message = response["choices"][0]["message"]
    function_name,flag = check_functions_question(question)
    if flag !=1:
        data = {'question':question,}
        api_url = 'http://128.205.43.182:5106/chat' 
        response = requests.post(api_url, json=data)
        elapsed_time = response.elapsed.total_seconds()
        print(elapsed_time)
        if response.status_code == 200:
            result = response.json()
            answer = result.get('answer', 'No answer provided')
        else:
            print("Error:", response.text)
        function_name,flag = check_functions_answer(answer)
    if flag == 1:        
        available_functions = { "president_ub" : president_ub, "chair_ub": chair_ub, "provost_ub": provost_ub , "Dean_ub": Dean_ub , "VPR_ub" : VPR_ub , "Intro" : intro, "Coffee": Coffee, "Enable" : enable , "Disable" : disable }  
        #function_name = response_message["function_call"]["name"]

        if function_name == "get_directions":
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])

            
            if function_args.get("start_location") == None:
                s_location = "Davis Hall, University at Buffalo"
            
            e_location = function_args.get("end_location")

            function_response = fuction_to_call(
            start_location=s_location,
            end_location= e_location,
            )
            print(f'Start location is {s_location}')
            print(f"---")
            print(f'Destination is {e_location}')
        
            return "map", function_response
        
        elif function_name == "president_ub":
            fuction_to_call = available_functions[function_name]  
            function_response = fuction_to_call()
            return "president", function_response
        
        elif function_name == "chair_ub":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "chair", function_response
        
        elif function_name == "provost_ub":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "provost", function_response
        
        elif function_name == "Dean_ub":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "dean", function_response
        
        elif function_name == "VPR_ub":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "vpr", function_response
        
        elif function_name == "Intro":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "intro", function_response
        
        elif function_name == "Coffee":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "coffee", function_response
        
        elif function_name == "Enable":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "enable", function_response
        
        elif function_name == "Disable":
            fuction_to_call = available_functions[function_name]
            function_response = fuction_to_call()        
            return "disable", function_response
    else:
        return "chat" , answer

def process_audio(model, API_URL):
    global proc_audio_bool

    # record_audio(file_path, audio_clip_path, 7)
    if model == "Server":

        response = requests.post(API_URL, files={'audio': open(audio_clip_path, 'rb')})

        if response.status_code == 200:
            transcription = response.json()
            out = transcription['results'][0]
            print(out)
        else:
            out = " Error in transcription "
            print("Error In transcription")
            
    else:
        out = transcribe_whisper(audio_clip_path,model)
    
    prompt = ". Answer this in two or less sentences "
    out += prompt
    if "dance" in out.lower():
        func = "Dance"
        arg = None

    elif "reset" in out.lower():
        func = "Reset"
        arg = None

    else:
        print("Getting Response from GPT")
        # try:
        func, arg = gptReq_withfunctions(out)
        # except:
        #     func = None
        #     arg = None
        
        print(f'{func} : {arg}')
        
    proc_audio_bool = True
    return func, arg


