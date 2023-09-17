import pyaudio
import struct 
import wave
import requests
import json
import os

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate= 16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=512)



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
    print('done recording')

# Audio clip name 
audio_clip_path = os.getcwd() + "/recording.wav"

AUDIO_RECOG =         True
AUDIO_RECOG_API =     "http://128.205.43.183:5006/audio_recog"
AUDIO_AUTH_USER =     "ninad"
TRANSCRIBE_API =     "http://128.205.43.183:5006/transcribe"

model = None

def process_audio( API_URL):


    response = requests.post(API_URL, files={'audio': open(audio_clip_path, 'rb')})

    if response.status_code == 200:
        transcription = response.json()
        out = transcription['results'][0]
        print(out)
    else:
        out = " Error in transcription "
        print("Error In transcription")
        
    
    
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
            func, arg = "gpt" , "ans"#gptResponse(out)
        except:
            func = None
            arg = None
        
        print(func, arg)
        
    return func, arg



while True:
    pcm = audio_stream.read(512)
    pcm = struct.unpack_from("h" * 512, pcm)

    serialized_data = json.dumps(pcm)
    response = requests.post("http://128.205.43.183:5006/wake_word", files={'audio': serialized_data } )
    if response.status_code == 200:
        transcription = response.json()

    if transcription >= 0:
        print("detected")
        print( transcription)

        record_audio("recording.wav", audio_clip_path, 5)

        auth = True
        if AUDIO_RECOG:
            auth = False
            response = requests.post(AUDIO_RECOG_API, files={'audio': open(audio_clip_path, 'rb')})
            if response.status_code == 200:
                print('if case')
                transcription = response.json()
                if str(transcription['Detected']).lower() == str(AUDIO_AUTH_USER).lower():
                    if transcription['Sim'] < 0.8:
                        auth = True
                    print('detected')
            else:
                print('Error in Audio recog:', response.status_code)
                
        
        if auth :
            # ret = {"func" : "chat_no_url" , "arg" : "Give me some time, I am working on it"}
            # start_time = time.time()
            # conn.sendall(pickle.dumps([ret] , protocol = 2))
            
            func, arg = process_audio( TRANSCRIBE_API)

            if func == "enable":
                AUDIO_RECOG = True
            
            if func == "disable":
                AUDIO_RECOG = False

            
        else:
            print( "You are not authorized user" )
            