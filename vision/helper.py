import os
import yaml


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-6] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param , "-----------")
    except yaml.YAMLError as e:
        print(e, "-------")
    
FACE_RECOG = param["face_recog"]
API_URL = param["face_recog_api"]  

NAO_IP = param["ip"]
NAO_PORT = param["port"]

width = 1280
hieght = 960
channel = 3 
fps = 30
sec = 5
camera_index = 0
resolution = 3
colourspace = 11
FPS = 5
