from util import *
from helper import *
from helper_vision import *


# Initialise nao class
initialise_nao()

# Nao startup routine
nao_startup_routine()

# Attach nao's thread funtions
attach_thread_functions()

# Robot body Touch thread
# Touch_ISR = threading.Thread(target= nao.initTG, args=(Touch_interrupts, nao, dance, play_song, led)  )
# Touch_ISR.start()

# Vision Threas
Vision_ISR = threading.Thread(target= nao_vision )
Vision_ISR.start()


while True:
    server = False
    pcm = audio_stream.read(512)
    pcm = struct.unpack_from("h" * 512, pcm)
    serialized_data = json.dumps(pcm)

    response = requests.post("http://128.205.43.183:5006/wake_word", files={'audio': serialized_data } )
    if response.status_code == 200:
        transcription = response.json()

    if transcription >= 0:
        print("Wake Word detected")
        # print( transcription)

        record_audio("audio/recording.wav", audio_clip_path, 5)

        start_time = time.time()

        try:
            response = requests.post(MAIN_API, data= {'user': AUDIO_AUTH_USER}  ,  files={'audio': open(audio_clip_path, 'rb') })
            if response.status_code == 200:
                    out = response.json()
                    # for key, value in out.items():
                    #     print ( '{}\t : \t {}'.format(key, value) )
        except:
            print("Server Down")
        end_time = time.time()
        elapsed_time = end_time - start_time        
        # print('\n Total Server Time taken: {:.4f} seconds'.format(elapsed_time))


        if not out['Auth']:
            nao.sayText( "You are not authorized user" ) 
            nao.posture.goToPosture("Stand" , 0.4)
            nao.ledStopListening()  
        else :         
            start_time = time.time()
            nao_do(out)
            elapsed_time = time.time() - start_time
            # print('Total Time taken by robot : {:.4f} seconds'.format(elapsed_time))

