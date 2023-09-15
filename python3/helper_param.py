# Load config parameters ---------------------------------------------

import os
import yaml

current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"

#porc_model_path_ppn = current_path[:-7] + "models/hey_aiko_ja_linux_v2_1_0.ppn"
porc_model_path_ppn = current_path[:-7] + "models/hello-kai_en_linux_v2_2_0.ppn"
#porc_model_path_pv = current_path[:-7] + "models/porcupine_params_ja.pv"

with open(yml_path, 'r') as ymlfile:
    try:
        param = yaml.safe_load(ymlfile)

    except yaml.YAMLError as e:
        print("Error in loading yaml file")

    
HOST =                '127.0.0.1'
PORT =                param["py_port"]
TRANSCRIBE_API =      param["transcribe_api"]
AUDIO_RECOG =         param["audio_recog"]
AUDIO_RECOG_API =     param["audio_authen_api"]
AUDIO_AUTH_USER =     param["audio_authe_user"]
openai_key =          os.environ["OPENAI_API_KEY"]


ChatGPT_API_KEY = 'AIzaSyCkPcrm28UTgbei5RZ0hXREM1dKKtVOci0'

RECORDING_TIME = 5