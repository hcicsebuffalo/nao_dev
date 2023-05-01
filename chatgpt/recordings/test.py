import os
import sys
import time
from naoqi import ALProxy

NAO_IP = "10.0.107.217"
NAO_PORT = 9559
PEPPER_IP = "10.0.52.247"
PEPPER_PORT = 9503


tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.say("Hello, world!")

try:
  videoRecorderProxy = ALProxy("ALVideoRecorder", NAO_IP, NAO_PORT)
except Exception, e:
  print "Error when creating ALVideoRecorder proxy:"
  print str(e)
  exit(1)

videoRecorderProxy.setFrameRate(10.0)
videoRecorderProxy.setResolution(2) # Set resolution to VGA (640 x 480)

# We'll save a 5 second video record in /home/nao/recordings/cameras/
videoRecorderProxy.startRecording("./home/sougato97/recordings", "first_video")
print "Video record started."
time.sleep(5)
videoInfo = videoRecorderProxy.stopRecording()
print "Video record ended."