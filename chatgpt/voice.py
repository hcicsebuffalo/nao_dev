#! /home/sougato97/miniconda3/envs/hri/bin/python
# -*- encoding: UTF-8 -*-

from pyannote.audio import Model
from pyannote.audio import Inference
import os
from scipy.spatial.distance import cdist
import numpy as np
import torch
import subprocess
from utils import *

def get_command(voice_clip_path, model, nao_say_path,json_file_path):
  
  file_name = "extract_command.mp3"
  while (1):
    record_audio(voice_clip_path, file_name)
    text = transcribe(voice_clip_path + file_name, model)
    chatgpt_module = ["chat", "talk", "conversation"]
    dance_module = ["dance", "show me something", "perform something"]
    flag = 0 # means null
    # print()
    print("Outside the for condition")
    for substring in chatgpt_module:
      if substring.lower() in text.lower():
        flag = 1 # means execute gpt 
        print ("ChatGPT ---- The value of flag is:", flag)
        return flag

    for substring2 in dance_module:
      if substring2.lower() in text.lower():
        flag = 2 # means execute gpt 
        print ("Dance ---- The value of flag is:", flag)
        return flag
      
    # else condition 
    text_data = '''I am not able to understand you. Please say something like do you want to have a conversation with me or would you like to watch me perform?'''
    writing_response_to_json_file(text_data,json_file_path)
    subprocess.run(['python2',nao_say_path])   
    # print(text_data)
    

  # # code failing here
  # if flag == 0 : # invalid i/p 
  #   text_data = '''I am not able to understand you. Please say something like do you want to have a conversation with me or would you like to watch me perform?'''
  #   writing_response_to_json_file(text_data,json_file_path)
  #   subprocess.run(['python2',nao_say_path])
  #   flag = get_command(voice_clip_path, file_name, model)

  # return flag


def user_auth(voice_clip_path, name,pyannote_key):
  
  pyannote_model = Model.from_pretrained("pyannote/embedding", use_auth_token = pyannote_key) ## exception handling
  # Define device to be used (GPU or CPU)
  Device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  inference = Inference(pyannote_model, window="whole", device = Device) 

  flag = 0 
  # list all files in directory
  for filename in os.listdir(voice_clip_path):
    # check if the current file name contains the substring
    if 'template' in filename:
      ref = inference(voice_clip_path + filename)
      recording = inference(voice_clip_path + name)

      # Convert these 1d Numpy to 2d numpy array 
      unsqueezed_ref = np.expand_dims(ref, axis=0)
      unsqueezed_rec = np.expand_dims(recording, axis=0)

      # Compute the distance
      distance1 = cdist(unsqueezed_ref, unsqueezed_rec, metric="cosine")[0,0]

      if (distance1 < 0.50):
        flag = 1
  return flag

def register_user(pyannote_key,voice_clip_path,model, nao_say_path):

  writing_response_to_json_file("Please tell me your 1st name, but wait for the prompt")
  # subprocess.run(['bash', 'chatgpt.sh'])
  subprocess.run(['python2', nao_say_path])
# # record_audio_with_fixed_duration(voice_clip_path, "temp.mp3", 5) ## exception handling
  record_audio(voice_clip_path, "temp.mp3")
  print("Name recorded!!")
  name = transcribe(voice_clip_path + "temp.mp3", model)
  print("The name is ",name)
  os.rename(voice_clip_path + '/temp.mp3', voice_clip_path + '/' + name + '_template.mp3')
