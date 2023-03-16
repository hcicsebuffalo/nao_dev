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

def user_auth(voice_clip_path, name,pyannote_key):
  
  pyannote_model = Model.from_pretrained("pyannote/embedding", use_auth_token = pyannote_key)
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

def register_user(pyannote_key,voice_clip_path,model):

  writing_response_to_json_file("Please tell me your 1st name, but wait for the prompt")
  # subprocess.run(['bash', 'chatgpt.sh'])
  subprocess.run(['python2','/home/sougato97/Human_Robot_Interaction/nao_dev/chatgpt/nao_say.py'])
  record_audio(voice_clip_path, "temp.mp3", 5)
  print("Name recorded!!")
  name = transcribe(voice_clip_path + "temp.mp3", model)
  print("The name is ",name)
  os.rename(voice_clip_path + '/temp.mp3', voice_clip_path + '/' + name + '_template.mp3')
