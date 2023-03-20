import openai
import json
import pyaudio
import wave
import os
import subprocess
import socket
import pyglet
import functools

# Function to record audio when spacebar is pressed
def record_audio(path, filename):
    # Set the parameters for the audio stream
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100 # sampling rate
    
    # Initialize the PyAudio object
    p = pyaudio.PyAudio()
    
    # Open the audio stream
    # stream = p.open(format=sample_format,
    #                 channels=channels,
    #                 rate=fs,
    #                 frames_per_buffer=chunk,
    #                 input=True)
   
    frames = []
    
    # Create a key event handler for starting and stopping recording
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            print("Recording started")
            global stream 
            stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)     
            pyglet.clock.schedule_interval(on_update, 1 / 60.0)
    
    def on_key_release(symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            print("Recording stopped")
            pyglet.clock.unschedule(on_update)
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

            window.close()
    
    # Create a clock event handler for recording audio
    def on_update(dt):
        data = stream.read(chunk)
        frames.append(data)
    
    # Create a window and attach the key event handlers 
    window = pyglet.window.Window()
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release


    # Creating the label to display the message
    label_text = "Press and hold SPACEBAR to START recording\nRelease SPACEBAR to STOP recording"
    label = pyglet.text.Label(label_text,
                          font_name="Arial",
                          font_size=24,
                          x=window.width//2, y=window.height//2,
                          multiline=True,
                          width=window.width,
                          height=window.height,
                          anchor_x="center", anchor_y="center")

    # Define the on_draw function
    @window.event
    def on_draw():
        window.clear()
        label.draw()
    
    # Start the Pyglet event loop
    pyglet.app.run()




# # Function to record audio with a fixed duration
def record_audio_with_fixed_duration(path, filename, duration): ## exception handling
    # Set the parameters for the audio stream
    chunk = 1024 
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100 # sampling rate 
    
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
def writing_response_to_json_file(answer,json_file_path):
    sorted_output=json.dumps(answer)
    with open(json_file_path, "w") as outfile:
        outfile.write(sorted_output)

def transcribe(recording_path,model):
    print("Processing the question.......")
    result = model.transcribe(recording_path) ## exception handling
    print("Question generated: "+result["text"])
    question=result['text']
    return question

# Function to generate chatgpt response
def gpt(question,model,openai_key,voice_clip_path,nao_say_path):

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
        subprocess.run(['python2',nao_say_path])
        # subprocess.run(['bash', 'chatgpt.sh'])
        while(1):
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

