from google.cloud import speech
client=speech.SpeechClient.from_service_account_file('google_secret_key.json')

file_name="/home/hri/nao_dev/temp/recording.wav"

with open(file_name,'rb') as f:
    wav_data=f.read()


audio_file=speech.RecognitionAudio(content=wav_data)

config=speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US'
)

response=client.recognize(
    config=config,
    audio=audio_file
)

# print(response)

for result in response.results:
    print(" {}".format(result.alternatives[0].transcript))