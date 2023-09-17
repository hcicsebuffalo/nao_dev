import pyaudio
import struct 
import requests
import json

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate= 16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=512)

while True:
    pcm = audio_stream.read(512)
    pcm = struct.unpack_from("h" * 512, pcm)

    serialized_data = json.dumps(pcm)
    response = requests.post("http://128.205.43.183:5006/wake_wprd", files={'audio': serialized_data } )
    if response.status_code == 200:
        transcription = response.json()

    if transcription >= 0:
        print("detected")
        print( transcription)