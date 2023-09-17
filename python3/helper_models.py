from helper_param import *
from helper_chatGPT import gptResponse

# Transcription -----------------
import whisper

if param["model"] == "Whisper":
    model = whisper.load_model("medium.en")
    print(" Whisper Model is loaded")

elif param["model"] == "Server":
    model = "Server"
    print(" Server will be used ")

else:
    print(" Error in yaml file, Please check model type")


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


# Wake word detection -----------
import pvporcupine
import pyaudio
import os
import wave

pico_key = os.environ["PICOVOICE_API_KEY"]
#porcupine = pvporcupine.create(access_key=pico_key, keyword_paths=[porc_model_path_ppn], model_path= porc_model_path_pv)
porcupine = pvporcupine.create(access_key=pico_key, keyword_paths=[porc_model_path_ppn])

print(porcupine.frame_length, " Sample rate")

# Initialize PyAudio and open a stream
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length)

print(" Procupine initialised")


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

# Audio clip name 
audio_clip_path = os.getcwd() + "/recording.wav"


# -------------
import requests

def process_audio(model, API_URL):

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
        try:
            func, arg = gptResponse(out)
        except:
            func = None
            arg = None
        
        print(f'{func} \n {arg}')
        
    return func, arg
