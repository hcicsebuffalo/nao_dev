#!/usr/bin/env python

# import libraries
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import torch
from PIL import Image
from torchvision import transforms
use_cuda = torch.cuda.is_available()
print(use_cuda)
device = 'cuda' if use_cuda else 'cpu'
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from deepface import DeepFace


model=None

def recogniseEmotion(frame,faces):
  use_cuda = torch.cuda.is_available()
  device = 'cuda' if use_cuda else 'cpu'
#   points = points.T

  # for bbox,p in zip(bounding_boxes, points):
  #   box = bbox.astype(int)
  #   x1,y1,x2,y2=box[0:4] 
  for face in faces:
    (x1,y1) = face[0],face[1]
    (x2,y2) = face[2],face[3]   
    face_img=frame[y1:y2,x1:x2,:]
    #print(x1,y1,x2,y2,"X")
    idx_to_class={0: 'Sad', 1: 'Neutral', 2: 'Neutral', 3: 'Sad', 4: 'Happy', 5: 'Neutral', 6: 'Sad', 7: 'Neutral'}
    IMG_SIZE=224
    test_transforms = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE,IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    ]
    )
    img_tensor = test_transforms(Image.fromarray(face_img))
    img_tensor.unsqueeze_(0)
    scores = model(img_tensor.to(device))
    scores=scores[0].data.cpu().numpy()
    label = idx_to_class[np.argmax(scores)]
    try:
      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)
      cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)
    except:
      pass
  #cv2.imwrite("Output.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
  return frame #cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

##Face Detection and Emotion.
#Emotion modified to have only 3 classes
def faceDetection(frame):
  faces, confidences = cv.detect_face(frame)

  return recogniseEmotion(frame,faces)

  objs = DeepFace.analyze(img_path = frame, actions = ['emotion'],detector_backend = 'dlib')
  x1=objs[0]['region']['x']
  y1=objs[0]['region']['y']
  x2=x1+objs[0]['region']['w']
  y2=y1+objs[0]['region']['h']
  label=objs[0]['dominant_emotion']
  label=label.capitalize()

  
  if(label=="Anger"):
   label="Sad"
  elif(label=="Disgust"):
   label="Neutral"
  elif(label=="Fear"):
   label="Sad"
  elif(label=="Suprise"):
   label="Neutral"
  cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)
  cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
  #cv2.imwrite("Output.jpg",frame)
  return frame

  objs = DeepFace.analyze(img_path = frame, actions = ['emotion'],detector_backend = 'dlib')
  x1=objs[0]['region']['x']
  y1=objs[0]['region']['y']
  x2=x1+objs[0]['region']['w']
  y2=y1+objs[0]['region']['h']
  label=objs[0]['dominant_emotion']
  label=label.capitalize()


  
  if(label=="Anger"):
   label="Sad"
  elif(label=="Disgust"):
   label="Neutral"
  elif(label=="Fear"):
   label="Sad"
  elif(label=="Suprise"):
   label="Neutral"
  cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)
  cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
  #cv2.imwrite("Output.jpg",frame)
  return frame

def emotion_init():
  PATH='../models/enet_b2_8_best.pt'
  global model
  model = torch.load(PATH,map_location=torch.device('cpu'))
  model=model.to(device)
  model.eval()


#test
#fpath='/content/nao_dev/vision/2.jpg'
#frame_bgr=cv2.imread(fpath)
#print(frame_bgr)
#faceDetection(frame_bgr)