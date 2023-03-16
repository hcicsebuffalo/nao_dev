import openai
import json
import pyaudio
import wave
import os
import subprocess
import socket

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
        subprocess.run(['python2','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
        # subprocess.run(['bash', 'chatgpt.sh'])
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

