## Nao functions version 2.0
## change log:
## 1.02: Added class "Region"
## 1.02: Resolution stuff.
## 1.03: Detect() now returns an object of the class "Region()"
## 1.04: Added Aldebarans face detection NaoFaceLocation().
## 1.05: Added the gesture() function and EyeLED() function.
## 1.06: Now able to look for the correct haarcascade file within the pythonpath
## 1.07: Changed Track() function to better support different frame rates
## 1.08: Added ALTrack function
## 1.09: Added second gesture in Gesture()
## 1.10: Added InitPose
## 1.11: Added Move
## 1.12: Added Crouch
## 1.13: Removed Gesture(), instead use the gesture lib. Changed comments for Move()
## 1.14: Added Play() function for playing sound files
## 1.15: Added Record() function
## 1.16: Added WalkTo function
## 1.17: Added PlaySine function
## 1.18: Added function FindFace()
## 1.19: Added RunMovement() (19-09-2011 - Turin)
## 1.20: Added Stiffen() for stiffening the joints
## 1.21: Added RunLed() for running led scripts
## 1.22: GetAvailableLEDPatterns() and GetAvailableGestures() added.
## 1.23: speechProxy added
## 1.24: File existence check added in RunMovement, RunLed, RunSpeech
## 1.25: Fixed remove = remove.reverse() returning None error
## 1.26: Added InitSpeech() and DetectSpeech()
## 1.27: GetAvailableDialogs() added.
## 1.28: Added LoadDialog()
## 1.29: Changed searchpaths of RunLED, RunMovement and RunSpeech to include /led, /gestures and /tts subfolders, respectively.
## 1.30: Added possibility of sending port number to InitProxy
## 1.31: Added better error handling in several functions and made posting of text optional.
## 1.32: RunLED changed to read files with ; as delimiter and to deal with multi-line led-files
## 1.33: LoadDialog() reads files with ; as delimiter
## 1.34: Added functions MoveHead() to move nao's head and GetYaw() to request the yaw of nao's head 
## 1.35: Added functions SetTTSVolume() and GetTTSVolume() for checking and controlling the volume of the Text to Speech
## 1.36: Added functions SetMusicVolume() and GetMusicVolume() for checking and controlling the volume of the Music
## 1.37: Updated FindFace to include arbitrary offset and gain. Default changed to up -0.2.
## 1.38: Speed of GetImage() improved. Removed dependency on Python Image Library
## 1.39: Removed "from naoqi import xxx" statements.
## 1.40: Added ALRobotPosture proxy, GoToPosture and proper InitPose() and Crouch(); InitProxy rewritten 
## 1.41: Added Landmark detection, Sound localization  and Sound detection
## 1.42: Added GetGyro, GetAccel, GetTorsoAngle, and GetFootSensors

### nao_nocv.py
## 1.0 removed dependencies on OpenCV and Image libraries. InitVideo and GetImage modified, but broken.
## 1.1 incorporated updates from nao.py version 1.38
    ## 1.37: Updated FindFace to include arbitrary offset and gain. Default changed to up -0.2.
    ## 1.38: Speed of GetImage() improved. Removed dependency on Python Image Library
    ## 1.39: Removed "from naoqi import xxx" statements.
## 1.2 updated to match nao.py version 1.40
        ## 1.40: Added ALRobotPosture proxy, GoToPosture and proper InitPose() and Crouch(); InitProxy rewritten;
## 1.3 updated to match nao.py version 1.41
        # 1.41: Added Landmark detection, Sound localization  and Sound detection 
## 2.0 updated to naoqi version 2.x
        # 1.42: Added GetGyro, GetAccel, GetTorsoAngle, and GetFootSensors
        
#import cv
from time import time
from time import sleep
#import Image
import random
import math
import sys
import os
import csv
import numpy as np
import naoqi

from collections import deque


__naoqi_version__='2.1'
__nao_module_name__ ="Nao Library"

gftt_list = list() # initialize good features to track for opencv
fast = 0 # initiliaze face detection state for opencv
time_q = deque([1,1,1,1,1,1,1,1,1,1])
old_time = time()
time_old_track = time()
#font = cv.InitFont(cv.CV_FONT_HERSHEY_TRIPLEX, 0.5, 0.5, 0.0, 1)

## Find the *.xml file for face detection.
list_path = sys.path
for i in range (0,len(list_path)):
    if os.path.exists(list_path[i]+"/haarcascade_frontalface_alt2.xml"):
        break
   
#cascade_front = cv.Load(list_path[i]+"/haarcascade_frontalface_alt2.xml")

interpol_time=0.3
start_mov_t = time()
weights = list()
existence = list()
id_pose = None
alface_subscribed = False
xtargetold = 0
ytargetold = 0

class ResolutionCamera:
    def __init__(self):
        self.low = 0
        self.medium = 1
        self.high = 2
        self.very_high=3
        self.res_160x120 = 0  #kQQVGA
        self.res_320x240 = 1  #kQVGA
        self.res_640x480 = 2  #kVGA
        self.res_1280x960 = 3 #k4VGA
        self.resolutionar = [160,120],[320,240],[640,480],[1280,960]
        self.framerate=30


camera_resolution = ResolutionCamera()

class Region:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

def Say(text, POST=True):
    global tts
    #print text
    try:
        #volume=GetTTSVolume()        
        SetTTSVolume(0.99)
        if POST:
            tts.post.say(text)
        else:
            tts.say(text)
        #SetTTSVolume(volume)
    except NameError:
        print ('ALTextToSpeech proxy undefined. Are you running a simulated naoqi?')
        
def HeadTouch():
    head_touch = memoryProxy.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value", 0)
    return head_touch

#################################################################################
## Use this function, InitProxy, to initialise the proxy. As an argument give up
## the Ip of Nao
#################################################################################
def ConnectProxy(proxy_name, IP, PORT):
    
    theProxy=None
    try:
        theProxy = naoqi.ALProxy(proxy_name, IP, PORT)
        sleep(0.01)
    except RuntimeError as e:
        print ("Error when creating ", proxy_name ," proxy:")
        print (str(e))    
    return theProxy
    
def InitProxy(IP="marvin.local", proxy=[0], PORT = 9559):
    """proxy: (list) 1->TTS, 2->audio, 3->motion, 4->memory, 5->face, 6->video, 7->LED's, 8->Track, 9->Speech, 10->Audioplayer, 11->VisionToolbox"""
    global audioProxy
    global motionProxy
    global memoryProxy
    global cameraProxy
    global faceProxy
    global ledProxy
    global tts
    global trackfaceProxy
    global playProxy
    global videoProxy
    global asr
    global speechProxy # same as asr for backward compatibility
    global sonarProxy
    global postureProxy
    global landmarkProxy
    global trackerProxy
    global soundProxy
    global soundLocalizationProxy
    
    global ALModuleList
    global proxyDict
    
    ALModuleList=["ALTextToSpeech","ALAudioDevice","ALMotion","ALMemory","ALFaceDetection","ALVideoDevice","ALLeds","ALFaceTracker","ALSpeechRecognition","ALAudioPlayer","ALVideoRecorder","ALSonar","ALRobotPosture","ALLandMarkDetection","ALTracker","ALSoundDetection","ALAudioSourceLocalization"]
    proxyDict={}
    proxyDict=proxyDict.fromkeys(ALModuleList,None)
    #proxyList=[None]*(len(ALModuleList))
    
    # check if list is empty
    if len(proxy)==0:
        proxy=range(1, len(ALModuleList)+1)
    else:
    #if not check whether it contains a 0
        if 0 in proxy:
            proxy=range(1, len(ALModuleList)+1)
    
    for i in proxy:
        proxyDict[ALModuleList[i-1]]=ConnectProxy(ALModuleList[i-1],IP, PORT)
    
    #define globals
    tts=proxyDict["ALTextToSpeech"]
    audioProxy=proxyDict["ALAudioDevice"]
    motionProxy=proxyDict["ALMotion"]
    memoryProxy=proxyDict["ALMemory"]
    faceProxy=proxyDict["ALFaceDetection"]
    cameraProxy=proxyDict["ALVideoDevice"]
    ledProxy=proxyDict["ALLeds"]
    trackfaceProxy=proxyDict["ALFaceTracker"]
    asr=proxyDict["ALSpeechRecognition"]
    speechProxy=asr # for backward compatibility
    playProxy=proxyDict["ALAudioPlayer"]
    videoProxy=proxyDict["ALVideoRecorder"]
    sonarProxy=proxyDict["ALSonar"]
    postureProxy=proxyDict["ALRobotPosture"]
    landmarkProxy=proxyDict["ALLandMarkDetection"]
    soundProxy=proxyDict["ALSoundDetection"]
    soundLocalizationProxy=proxyDict["ALAudioSourceLocalization"]
    trackerProxy=proxyDict["ALTracker"]

def InitSonar(flag=True):
    
    #period = 100
    #precision = 0.1
    if flag:
        #sonarProxy.subscribe("test4", period , precision )
        sonarProxy.subscribe("test4" )
    else:
        try:
            sonarProxy.unsubscribe("test4" ) 
            flag=False
        except:
            print ("Sonar already unsubscribed")
            flag=False
    return flag
   
#################################################################################
## Use this function, CloseProxy, to close the proxy. As an argument give up
## the Ip of Nao
#################################################################################
def CloseProxy(proxy=[0]):
    """proxy: (list) 1->TTS, 2->audio, 3->motion, 4->memory, 5->face, 6->video, 7->LED's, 8->Track, 9->Speech, 10->Audioplayer, 11->VisionToolbox"""

    global ALModuleList
    global proxyDict
    
    # check if list is empty
    if len(proxy)==0:
        proxy=range(1, len(ALModuleList)+1)
    else:
    #if not check whether it contains a 0
        if 0 in proxy:
            proxy=range(1, len(ALModuleList)+1)

    for i in proxy:
        try:
            proxyDict[ALModuleList[i-1]].exit()
            sleep(0.1)
            #print "Proxy ALTextToSpeech established"
        except RuntimeError as e:
            print ("Error when deleting ", ALModuleList[i-1], " TextToSpeech proxy:")
            print (str(e))

    #redefine globals (one or more are set to None)
    tts=proxyDict["ALTextToSpeech"]
    audioProxy=proxyDict["ALAudioDevice"]
    motionProxy=proxyDict["ALMotion"]
    memoryProxy=proxyDict["ALMemory"]
    faceProxy=proxyDict["ALFaceDetection"]
    cameraProxy=proxyDict["ALVideoDevice"]
    ledProxy=proxyDict["ALLeds"]
    trackfaceProxy=proxyDict["ALFaceTracker"]
    asr=proxyDict["ALSpeechRecognition"]
    speechProxy=asr # for backward compatibility
    playProxy=proxyDict["ALAudioPlayer"]
    videoProxy=proxyDict["ALVideoRecorder"]
    sonarProxy=proxyDict["ALSonar"]
    postureProxy=proxyDict["ALRobotPosture"]
    landmarkProxy=proxyDict["ALLandMarkDetection"] 
     
################################################################################
## nao.ALFacePosition() subscribes to faceProxy and returns location of face.
## It uses the embedded functions of Aldebaran face detection. If you want to
## change the period, you will have to first unsubscribe using switch = False.
## It returns [face_location,detected]. detected = whether a face has been seen.
################################################################################
def ALFacePosition(switch = True, period = 100):    
    global alface_subscribed

    if alface_subscribed == False:
        faceProxy.subscribe("Test_Face", period, 0.0)
        alface_subscribed = True

    location_face = memoryProxy.getData("FaceDetected")
    if switch == False:
        faceProxy.unsubscribe("Test_Face")
        alface_subscribed == False
    #print " location face: " , location_face
    if location_face==None:
        location_face=[]
    if len(location_face) >= 2: # Changed with respect to old naoqi versions
        return [-location_face[1][0][0][1],location_face[1][0][0][2]], True
        
    else:
        return [], False
        
def DetectFace(switch = True, period = 100):
    facePosition, detected = ALFacePosition(switch, period)
    timestamp=time()
    
    return detected, timestamp, facePosition # for consistency with DetectSound DetectLandmark etc

###############################################################################
## EyesLED() can change the color of the leds. The color parameter sets
## the color in RGB values.
## The standard color is off, [0,0,0]. The interpolation time defines the time
## in seconds it will take to fully switch to the new color.
###############################################################################
def EyeLED(color=[0,0,0],interpol_time = 0, POST=True):
    sGroup = "FaceLeds"
    try:
        if POST:
            ledProxy.post.fadeRGB(sGroup, 256*256*color[0] + 256*color[1] + color[2],interpol_time)
        else:
            ledProxy.fadeRGB(sGroup, 256*256*color[0] + 256*color[1] + color[2],interpol_time)            
                
    except NameError:
        print ('ALLeds proxy undefined.')

###############################################################################
## This function returns the available gestures located in the gesture dir.
###############################################################################
def GetAvailableGestures():
    """Returns available gestures in a list"""
    list_path = sys.path
    found = 0
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/gestures"):
            found = 1
            break

    if found == 0:
        print ("Could not find /gestures directory!")
        raise IOError
        return None

    remove = []
    
    list_gestures = os.listdir(list_path[i]+"/gestures")
    for i in range(len(list_gestures)):
        list_gestures[i] = "/gestures/"+list_gestures[i]
        if not list_gestures[i].endswith(".py") and not list_gestures[i].endswith(".ges"):
            remove.append(i)

    ## remove non py files
    remove.reverse()
        
    for i in range(len(remove)):
        list_gestures.pop(remove[i])
        
    return list_gestures

###############################################################################
## This function returns the available gestures located in the gesture dir.
###############################################################################
def GetAvailableLEDPatterns():
    """Returns available gestures in a list"""
    list_path = sys.path
    found = 0
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/led"):
            found = 1
            break

    if found == 0:
        print ("Could not find /led directory!")
        raise IOError
        return None

    list_led = os.listdir(list_path[i]+"/led")
    remove = []
    for i in range(len(list_led)):
        list_led[i] = "/led/"+list_led[i]
        if not list_led[i].endswith(".csv") and not list_led[i].endswith(".led"):
            remove.append(i)
    ## remove non csv files


    remove.reverse()
    for i in remove:
        list_led.pop(i)
            

    return list_led

###############################################################################
## This function returns the available dialogs located in the dialogs dir.
###############################################################################
def GetAvailableDialogs():
    """Returns available dialogs in a list"""
    list_path = sys.path
    found = 0
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/dialogs"):
            found = 1
            break

    if found == 0:
        print ("Could not find /dialogs directory!")
        raise IOError
        return None

    list_dlg = os.listdir(list_path[i]+"/dialogs")
    remove = []
    for i in range(len(list_dlg)):
        list_dlg[i] = "/dialogs/"+list_dlg[i]
        if not list_dlg[i].endswith(".csv") and not list_dlg[i].endswith(".dlg"):
            remove.append(i)
    ## remove non csv files


    remove.reverse()
    for i in remove:

        list_dlg.pop(i)
            

    return list_dlg

#########################################################################
## Loads a dialog csv file and converts its logic and questions/messages
## to dictionaires for use in a smach state machine
#########################################################################
def LoadDialog(file_name):
    """ Give the filename of the dialog in the /dialogs folder. Extension should be .csv or .dlg."""
    list_path = sys.path
    filefound=False
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/dialogs/"+file_name):
            filefound=True
            break

    if not filefound:
        print ("Dialog file "+str(file_name)+" not found in PYTHONPATH")
        return

    file_load = open(list_path[i]+"/dialogs/"+file_name)

    #read all rows of CSV file (assumes delimiter is ';')
    csv_reader = csv.reader(file_load, delimiter=';')

    return csv_reader

################################################################################
## nao.InitVideo() initialises the cv image and sets the variables on Nao.
## It allows you to give up the resolution. But first execute nao.InitProxy()
################################################################################
def InitVideo(resolution_id):
    global key
    global nameId
    global cameraProxy
    global nao_img

    res = camera_resolution.resolutionar[resolution_id]
    framerate=camera_resolution.framerate
    kALColorSpace=0 #BGR: 11, RGB: 13
    
    try:
        nameId = cameraProxy.subscribe("python_GVM2"+str(random.random()*10), resolution_id, kALColorSpace, framerate) #0, 0, 10
    except NameError:
        print ('ALVideoDevice proxy undefined. Are you running a simulated naoqi?')
        return None
    nao_img = np.zeros((res[0], res[1],3),dtype=np.uint8)

    return nao_img
        
#################################################################################
## nao.GetImage() gets the image from Nao. You will fist need to execute
## nao.Initvideo()
#################################################################################
def GetImage():
    global nao_img

    gotimage = False
    count = 0
    
    while not gotimage and count < 10:
        try:
            img =cameraProxy.getImageRemote(nameId)
            nao_img=img[6]




#            pi=Image.frombuffer("L",(img[0],img[1]),img[6])


            gotimage =True
        except NameError:
            print ('ALVideoDevice proxy undefined. Are you running a simulated naoqi?')
            break
        except:
            count = count + 1
            print("problems with video buffer!! Did you initialize nao.InitVideo() the video first?")

#    cv.SetData(cv_im, pi.tostring())
#    cv.Flip(cv_im,cv_im,0)

#    key = cv.WaitKey(10)
    return nao_img

################################################################################
## Initializes the track function it stiffens the joints, gathers the IDPose
################################################################################
def InitTrack():
    global xtargetold
    global ytargetold
    xtargetold = 0
    ytargetold = 0
    # Stiffening the head joints
    motionProxy.stiffnessInterpolation('HeadYaw', 1.0, 1.0)
    motionProxy.stiffnessInterpolation('HeadPitch', 1.0, 1.0)
    interpol_time = 0.5
    names  = ["HeadYaw","HeadPitch"]
################################################################################
## Releasing stiffness of the head joints
################################################################################
def EndTrack():
    motionProxy.stiffnessInterpolation('HeadYaw', 0.0, 1.0)
    motionProxy.stiffnessInterpolation('HeadPitch', 0.0, 1.0)

################################################################################
## If the tracking function is initialised you can let nao follow a point in
## the camera stream the boolean "detected" specifies whether the target
## was detected. "frametime" is the time between frames.
################################################################################   
def Track(target_loc, detected, speed = 5, min_move = 0.04):
    """
    target_loc =  the location Nao's head should move to in radians
    detected = is the head detected, If False target_loc is not used and speed of movement gradually decreases
    (optional) speed = the speed of the movement
    (optional) min_move = the minimal angle of difference between the target_loc and current location for movements to occur.

    """
    global xtargetold
    global ytargetold
    global time_old_track
    global id_pose
    global interpol_time
    global start_mov_t

    interpol_time = 1.0/speed

    xtarget = target_loc[0]
    ytarget = target_loc[1]

    try:
        frametime = time() - time_old_track
        time_old_track = time()
    except:
        print ("Not able to determine frame rate. Guessing...")
        frametime = 0.15

    if detected == False:
        xtarget = xtargetold-xtargetold*(frametime)
        ytarget = ytargetold-ytargetold*(frametime)

    xtargetold = xtarget
    ytargetold = ytarget

    if ((xtarget > min_move or xtarget < -min_move) or (ytarget > min_move or ytarget < -min_move)):
        names  = ["HeadYaw","HeadPitch"]

        try:
            id_pose
        except NameError:
            id_pose = None

        if id_pose != None:
            #motionProxy.stop(id_pose)
            pass

        try:
            id_pose = motionProxy.post.angleInterpolation(names, [-xtarget/2.5,ytarget/2.5] , interpol_time, False)
        except RuntimeError:
            print ("Kan hoofd niet draaien")
        start_mov_t = time()
################################################################################



## Is used to see if Nao's head is moving.
################################################################################
def MovingHead():
    time_mov = time()-start_mov_t
    if time_mov > 2*interpol_time:
        return False
    else:
        return True
    return
###############################################################################
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
################################################################################
# Track Face
################################################################################
def ALTrack(switch=1):
    """Turn head tracking on or off. Or get status = 2"""
##    if switch == 1:
##        InitTrack()
##        trackfaceProxy.startTracker()
##    elif switch == 0:
##        trackfaceProxy.stopTracker()
##        #EndTrack()
##    else:
##        return trackfaceProxy.isActive()
    Tracker(switch)

def Tracker(switch=1,targetName="Landmark", targetParam=0.1):
    """Turn tracker on or off. Or get status = 2"""

    
##Target    Parameters Comment
##RedBall   diameter of ball (meter)    Used to compute the distance between robot and ball. 
##Face      width of face (meter)       Used to compute the distance between robot and face. 
##LandMark  [size, [LandMarkId, ...]]   size is used to compute the distance between robot and LandMark. LandMarkId to specify the LandMark to track. 
##LandMarks [[size, [LandMarkId, ...]], [size, [LandMarkId, ...]]] Same parameters as LandMark. One array by LandMark. 
##People    [peopleId, ...]             Used to track a specific people. 
##Sound     [distance, confidence]      distance is used to estimate sound position and confidence to filter sound location. 

    if switch == 1:
        InitTrack()
        # Add target to track.
        trackerProxy.registerTarget(size, LandMarkId)
        # Then, start tracker.
        trackerProxy.track(size)
    elif switch == 0:
        trackerProxy.stopTracker()
        trackerProxy.unregisterAllTargets()
        #EndTrack()
    else:
        return trackfaceProxy.isActive()

##############################################################################
## Go to one of the predefined postures
#############################################################################
def GoToPosture(thePosture, speed=0.5):

#    "StandInit"
#    "SitRelax"
#    "StandZero"
#    "LyingBelly"
#    "Sit"
#    "LyingBack"
#    "Stand"
#    "Crouch"

    postureProxy.goToPosture(thePosture, speed)

def version(string):
    n=string.find('.') # find first period
    a=string[:n+1] # cut out the main version number plus period
    b=string[n+1:].replace('.','') #remove any trailing periods

    return float(a+b) # convert to float    

##############################################################################
## Put's Noa into its Initpose. Only use when standing or in crouch position.
#############################################################################
def InitPose(time_pos=0.5, speed=0.8):
    """Nao will move to initpose."""

    Move(0.0,0.0,0.0) # stop moving
    sleep(0.1)
    # set stiffness
    motionProxy.stiffnessInterpolation('Body',1.0, time_pos)
    GoToPosture("Stand", speed)
    #sleep(0.5)
    #IP.initPose(motionProxy)
    # numJoints = len(motionProxy.getJointNames('Body'))

    # allAngles = [0.0,0.0,                   # head
        # 1.39, 0.34, -1.39, -1.04, 0.0, 0.0,             # left arm
        # 0.0, 0.0, -0.43, 0.69, -0.34, 0.0,                  # left leg
        # 0.0, 0.0, -0.43, 0.69, -0.34, 0.0,                  # right leg
        # 1.39, -0.34, 1.39, 1.04, 0.0, 0.0]              # right arm
    # #printnumJoints
    # if (numJoints == 26):
        # angles = allAngles
    # elif (numJoints == 22):  # no hands (e.g. simulator)
        # angles = allAngles[0:6] + allAngles[8:24]
    # else:
        # print "error in Init Pose"
        
    # try:
        # motionProxy.post.angleInterpolation('Body', angles, 1.5, True);
    
    # except RuntimeError,e:
        # print "An error has been caught"
        # print e
        
def Stiffen(stiffness = True, int_time=1):
    """Make Nao stiffen its joints (Can be True or False)"""
    motionProxy.stiffnessInterpolation('Body',int(stiffness), int_time)

def StiffenUpperBody(stiffness = True, int_time=0.1):
    """Make Nao stiffen its joints (Can be True or False)"""
    motionProxy.setStiffnesses('HeadPitch',int(stiffness), int_time)
    motionProxy.setStiffnesses('HeadYaw',int(stiffness), int_time)
    motionProxy.setStiffnesses('LElbowRoll',int(stiffness), int_time)
    motionProxy.setStiffnesses('LElbowYaw',int(stiffness), int_time)
    motionProxy.setStiffnesses('LHand',int(stiffness), int_time)
    motionProxy.setStiffnesses('LShoulderPitch',int(stiffness), int_time)
    motionProxy.setStiffnesses('LShoulderRoll',int(stiffness), int_time)
    motionProxy.setStiffnesses('LWristYaw',int(stiffness), int_time)
    motionProxy.setStiffnesses('RElbowRoll',int(stiffness), int_time)
    motionProxy.setStiffnesses('RElbowYaw',int(stiffness), int_time)
    motionProxy.setStiffnesses('RHand',int(stiffness), int_time)
    motionProxy.setStiffnesses('RShoulderPitch',int(stiffness), int_time)
    motionProxy.setStiffnesses('RShoulderRoll',int(stiffness), int_time)
    motionProxy.setStiffnesses('RWristYaw',int(stiffness), int_time)

################################################################################
## Nao crouches and loosens it's joints.
###############################################################################
def Crouch(speed=0.8):
    Move(0.0,0.0,0.0) # stop moving
    sleep(0.1)
    GoToPosture("Crouch", speed)
    motionProxy.stiffnessInterpolation('Body',0, 0.5)

##def Crouch():
##    """Make Nao to crouch pose."""
##    
##  # get the robot config
##    robotConfig = motionProxy.getRobotConfig()
##    
##  #for i in range(len(robotConfig[0])):
##    #    print robotConfig[0][i], ": ", robotConfig[1][i]
##
##    # "Model Type"   : "naoH25", "naoH21", "naoT14" or "naoT2".
##    # "Head Version" : "VERSION_32" or "VERSION_33" or "VERSION_40".
##    # "Body Version" : "VERSION_32" or "VERSION_33" or "VERSION_40".
##    # "Laser"        : True or False.
##    # "Legs"         : True or False.
##    # "Arms"         : True or False.
##    # "Extended Arms": True or False.
##    # "Hands"        : True or False.
##    # "Arm Version"  : "VERSION_32" or "VERSION_33" or "VERSION_40".
##    # Number of Legs : 0 or 2
##    # Number of Arms : 0 or 2
##    # Number of Hands: 0 or 2
##    if robotConfig[1][0]=="naoH25" or robotConfig[1][0]=="naoH21":
##        pass
##    else:
##        print "Wrong robot type: cannot crouch without arms and legs"
##        return
##    if robotConfig[1][8]=="VERSION_32":
##      allAngles = [0.0,0.0,                   # head
##              1.545, 0.33, -1.57, -0.486, 0.0, 0.0,       # left arm
##              -0.3, 0.057, -0.744, 2.192, -1.122, -0.035,     # left leg
##              -0.3, 0.057, -0.744, 2.192, -1.122, -0.035,         # right leg
##              1.545, -0.33, 1.57, 0.486, 0.0, 0.0]        # right arm
##    elif robotConfig[1][8]=="VERSION_33":
##    #Modified for robot version V33
##      allAngles = [0.0,0.0,                   # head
##              1.545, 0.2, -1.56, -0.5, 0.0, 0.0,       # left arm
##              -0.319, 0.037, -0.695, 2.11, -1.189, -0.026,     # left leg
##              -0.319, 0.037, -0.695, 2.11, -1.189, -0.026,         # right leg
##              1.545, -0.2, 1.56, 0.5, 0.0, 0.0]        # right arm
##    else:
##    #Modified for robot version V4.0
##      allAngles = [0.0,0.0,                   # head
##              1.53, 0.15, -1.56, -0.5, 0.0, 0.0,       # left arm
##              -0.30, 0.05, -0.75, 2.11, -1.19, -0.04,     # left leg
##              -0.30, 0.05, -0.75, 2.11, -1.19, -0.04,         # right leg
##              1.53, -0.15, 1.56, 0.5, 0.0, 0.0]        # right arm
##
##    numJoints = len(motionProxy.getJointNames('Body'))
##    if (numJoints == 26):
##        angles = allAngles
##    elif (numJoints == 22):  # no hands (e.g. simulator)
##        angles = allAngles[0:6] + allAngles[8:24]
##    else:
##        print "error in numJoints"
##            
##    try:
##        motionProxy.angleInterpolation('Body', angles, 1.5, True);
##
##    except RuntimeError,e:
##        print "An error has been caught"
##        print e
##
##    motionProxy.stiffnessInterpolation('Body',0, 0.5)
    
##################################################################################
## Allows Nao to move in a certain direction with a certain speed.
################################################################################
def Move(dx=0, dy=0, dtheta=0, freq=1):
    """"
    dx = forward speed, dtheta = rotational speed,
    dy = sidewards speed, freq = step frequency.
    Allows Nao to move in a certain direction
    with a certain speed.
    """
    
    if version(__naoqi_version__)<2:
        motionProxy.setWalkTargetVelocity(dx, dy, dtheta, freq)
    else:
        motionProxy.moveToward(dx,dy,dtheta)
    
def ReadSonar():    
    """Read the left and right Sonar Values"""
    SonarLeft = "Device/SubDeviceList/US/Left/Sensor/Value"
    SonarRight = "Device/SubDeviceList/US/Right/Sensor/Value"
    SL=memoryProxy.getData(SonarLeft,0) # read sonar left value from memory
    SR=memoryProxy.getData(SonarRight ,0) # read sonar right value from memory
    return SL, SR

def GetGyro():
    """Get the Gyrometers Values"""
    GyrX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
    GyrY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
    return GyrX, GyrY

def GetAccel():
    """Get the Accelerometers Values"""
    AccX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
    AccY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
    AccZ = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")
    return AccX, AccY, AccZ

def GetTorsoAngle():
    """Get the Computed Torso Angle in radians"""
    TorsoAngleX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
    TorsoAngleY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value")
    return TorsoAngleX, TorsoAngleY

def GetFootSensors():
    """Get the foot sensor values"""
    # Get The Left Foot Force Sensor Values
    LFsrFL = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
    LFsrFR = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
    LFsrBL = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
    LFsrBR = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")
    LF=[LFsrFL, LFsrFR, LFsrBL, LFsrBR]

    # Get The Right Foot Force Sensor Values
    RFsrFL = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value")
    RFsrFR = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value")
    RFsrBL = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value")
    RFsrBR = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value")
    RF=[RFsrFL, RFsrFR, RFsrBL, RFsrBR]

    return LF, RF

##################################################################################
## Allows Nao to move dx meters forward, dy meters sidways with final orientation of dtheta
################################################################################
def Walk(dx=0,dy=0,dtheta=0,post=False):
    
    
    """"
    dx = forward meters, dtheta = final angle,

    dy = sidewards meters
    Allows Nao to move in a certain direction.
    
    """
    if version(__naoqi_version__)<2:
        if post==False:
            motionProxy.walkTo(dx, dy, dtheta)
        else:
            motionProxy.post.walkTo(dx, dy, dtheta)
    else:
        if post==False:
            motionProxy.moveTo(dx, dy, dtheta)
        else:
            motionProxy.post.moveTo(dx, dy, dtheta)


##################################################################################
## Moves nao head yaw and pitch of the provided values yaw_val and pitch_val
################################################################################
def MoveHead(yaw_val=0, pitch_val=0, isAbsolute=True, post=True, timeLists= [[1],[1]]):

    names      = ["HeadYaw", "HeadPitch"]
    angleLists = [[yaw_val], [pitch_val]]

    if post==False:
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    else:
        motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)

def GetYaw():
    names  = "HeadYaw"
    useSensors  = True
    HeadYaw = motionProxy.getAngles(names, useSensors)
    return HeadYaw

def GetPitch():
    names  = "HeadPitch"
    useSensors  = True
    HeadPitch = motionProxy.getAngles(names, useSensors)
    return HeadPitch

def GetYawPitch():
    names  = ["HeadYaw", "HeadPitch"]
    useSensors  = True
    HeadYawPitch = motionProxy.getAngles(names, useSensors)
    return HeadYawPitch

##################################################################################
## Allows Nao to play a sinusoidal wave of frequency in Hertz p1, Volume gain 0-100  p2, Stereo Pan set to either {-1,0,+1} p3 , duration in seconds
################################################################################

def PlaySine(p1,p2,p3,duration):
    global audioProxy
    
    try:
        audioProxy.playSine(p1,p2,p3,duration)
    except NameError:
        print ('ALAudioDevice proxy undefined. Are you running a simulated naoqi?')

###################
#stop music
###########################
def StopPlay():
    
    playProxy.stopAll()



######################################################
# Use this class and it's Play() function to play a wav or mp3 file on Nao.
# The files should be uploaded via ftp. Go to ftp://username:password@nao's_ip
# And upload them it's initial directory, which is /home/nao/ .
# id_music
######################################################



def Play(file_name):
    """Plays a audio file on Nao, it runs the file from the /home/nao/ directory"""

    file_name = "/home/nao/"+file_name
    id_music=playProxy.post.playFile(file_name)
    return id_music


###########
# Pause
########################
def Pause(id_music):

    playProxy.post.pause(id_music)


########################
#playFileFromPosition
##############################
def playFileFromPosition(file_name, position):
    file_name = "/home/nao/"+file_name
    id_music=playProxy.post.playFileFromPosition(file_name, position)
    return id_music


##########################
#Set Volume TTS
##################################
def SetTTSVolume(volume):
    tts.setVolume(volume)

##########################
#Get Volume TTS
##################################
def GetTTSVolume():
    vol=tts.getVolume()
    return vol

##########################
#Set Volume Music
##################################
def SetMusicVolume(id_music,volume):
    playProxy.setVolume(id_music,volume)

##########################
#Get Volume Music
##################################
def GetMusicVolume():
    vol=playProxy.getMasterVolume()
    return vol



###############################################################################
## This will record a file located in the /home/nao/naoqi/share/naoqi/vision
## Directory on Nao
###############################################################################
def Record(file_name, fps = 3.0, resolution = 0):
    """
    file_name without extension. fps, should be higher than 3.0.
    resolution shoud be between 0 and 2.
    Saved in /home/nao/naoqi/share/naoqi/vision
    """
    vidp.startVideoRecord_adv(file_name,fps,"MJPG",resolution,-1)

    

###############################################################################
## This function will look for a face. If it doesn't find it False is returned.
###############################################################################
def FindFace(gain=1.0, offset=[0.0, -0.2]):
    """ It looks for a face and if it finds it returns boolean True """
    location, detected = ALFacePosition()
    if detected:
        return True
    
##     - -
##     0 0 0 0 0
##     4 2 0 2 4
##    ###########
##-0.4#+-+-+-+#e#
##    #|#####|#|#
##-0.2#+#+-+#+#+#
##    #|#|#|#|#|#
##   0#+#+#s#+#+#
##    #|#|###|#|#
## 0.2#+#+-+-+#+#
##    #|#######|#
## 0.4#+-+-+-+-+#
##    ###########
    
#    offset=0.0
#    offset=0.0
#    gain=1.0
    max_yaw=2 # range [-119, 119] degrees
    min_yaw=-2
    max_pitch=0.26 # conservative but safe, real range is [-38.5, 29.5] /180*Pi
    min_pitch=-0.6
    yaw =   [0.0, 0.0,-0.2,-0.2,0.0,0.2, 0.2, 0.2, 0.0,-0.2,-0.4,-0.4,-0.4,-0.2,0.0,0.2,0.4, 0.4, 0.4, 0.2, 0.0]
    pitch = [0.0,-0.2,-0.2, 0.0,0.0,0.0,-0.2,-0.4,-0.4,-0.4,-0.4,-0.2, 0.0, 0.0,0.0,0.0,0.0,-0.2,-0.4,-0.4,-0.4]

#    pitch = [0,-0.2,-0.2,0.0,0.2,0.2,0.2,0.0,-0.2,-0.4,-0.4,-0.4,-0.4,-0.2,
#             0.0,0.2,0.4,0.4,0.4,0.4,0.4,0.2,0.0,-0.2,-0.4,0.0]

#    pitch = [0,-0.2,-0.2,0.0,0.0,0.0,0.2,0.0,-0.2,-0.4,-0.4,-0.4,-0.4,-0.2,
#             0.0,0.2,0.4,0.4,0.4,0.4,0.4,0.2,0.0,-0.2,0.0]

                                    
    for i in range(0,len(yaw)):
        names      = ["HeadYaw", "HeadPitch"]
        the_yaw=yaw[i]*gain+offset[0]
        the_pitch=pitch[i]*gain+offset[1]
        if the_yaw>max_yaw:
            the_yaw=max_yaw
        if the_yaw<min_yaw:
            the_yaw=min_yaw
        if the_pitch>max_pitch:
            the_pitch=max_pitch
        if the_pitch<min_pitch:
            the_pitch=min_pitch
        
        angleLists = [[the_yaw], [the_pitch]]
        timeLists  = [[1],[1]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        sleep(0.25)
        location, detected = ALFacePosition()

        if detected:
            return True

    return False

#######################################################################
## This functions executes movements transported from choregraph
## and saved in a *.py file. Make sure to initialize the motion proxy.
#######################################################################
def RunMovement(file_name, post = True, to_start_position = True):
    """ Give up the filename containing the movement. Needs motion proxy."""

    list_path = sys.path
    filefound = False
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/gestures/"+file_name):
            file_name=list_path[i]+"/gestures/"+file_name
            filefound=True
            break
        if os.path.exists(list_path[i]+"/"+file_name):
            file_name=list_path[i]+"/"+file_name
            filefound=True
            break

    if not filefound:
        print ("Movement or gesture "+str(file_name)+" not found in PYTHONPATH")
        return

    file_load = open(file_name)
    lines = file_load.readlines()
    for i in range(0,len(lines)):
        if lines[i].startswith("try:"):
            break

        exec (lines[i])

    if to_start_position:
        last_key = motionProxy.getAngles(names, True)

        high_time = 0.0
        for i in range(0,len(times)):
            cur_time = times[i][len(times[i])-1]
            if cur_time > high_time:
                high_time = cur_time

        for i in range(0, len(times)):
            times[i].append(high_time+0.1)
            times[i].append(high_time+2)
            keys[i].append(keys[i][len(keys[i])-1])
            keys[i].append([last_key[i],[ 3, -0.55556, 0.00000], [ 3, 0.55556, 0.00000]])

    
    if post:
        motionProxy.post.angleInterpolationBezier(names, times, keys)
    else:
        motionProxy.angleInterpolationBezier(names, times, keys)

###########################################################################
## This function runs a speech script saves as a *.csv file. Column 1
## contains the time in seconds, Column 2 contains the TTS input. This
## function requires a TTS proxy.
###########################################################################
def RunSpeech(file_name):
    """ file_name is the name containing the speech script."""
    list_path = sys.path
    file_found=False
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/tts/"+file_name):
            file_name=list_path[i]+"/tts/"+file_name
            filefound=True
            break
        if os.path.exists(list_path[i]+"/"+file_name):
            file_name=list_path[i]+"/"+file_name
            filefound=True
            break

    if not filefound:
        print ("Speech file "+str(file_name)+" not found in PYTHONPATH")
        return

    try:
        script_reader = csv.reader(open(file_name, 'rb'))
    except:
        print ("Speech script does not exist!!!")
        return
    cur_line = script_reader.next()
    start_time = time()
    while True:
        try:
            cur_line = script_reader.next()
        except:
            break
        while float(cur_line[0])> (time()-start_time):
            sleep(0.1)
        Say(cur_line[1])
        
########################################################################
## Uses a led CSV file to read out the proper eye pattern variables.
## Allows you to set LED Group, RGB, and Duration
## Frequency is currently ignored
## CSV file format:
##  Row 1 = Header (ignored)
##  Row 2-n = LED Group; Red; Green; Blue; Frequency; Duration
## Duration = Fade Time past to ALLeds.FadeListRGB
## CSV file delimiter is ';' (Used by Excel)
#########################################################################
def RunLED(file_name, post = True):
    """ Uses a led CSV file to read out the proper eye pattern variables."""
    #open CSV file
    list_path = sys.path
    filefound=False
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/led/"+file_name):
            file_name=list_path[i]+"/led/"+file_name
            filefound=True
            break
        if os.path.exists(list_path[i]+"/"+file_name):
            file_name=list_path[i]+"/"+file_name
            filefound=True
            break

    if not filefound:
        print ("LED file "+str(file_name)+" not found in PYTHONPATH")
        return
     
    file_load = open(file_name, 'rb')

    #read all rows of CSV file (assumes delimiter is ';')
    csv_reader = csv.reader(file_load, delimiter=';')

    #read header row and ignore it
    csv_reader.next()

    #initialize LEDs to off
    ledProxy.post.off('FaceLeds')
    #print 'ledProxy.post.off(', 'FaceLeds', ')'

    #read first LED command and initialize fadeListRGB parameters
    parameters = csv_reader.next()
    name = parameters[0]
    rgbList = [256*256*int(parameters[1])+256*int(parameters[2])+int(parameters[3])]
    timeList = [float(parameters[5])]

    #while CSV file not empty
    while True:
         
         try:
              parameters = csv_reader.next()
         except:
              break

         #if LED Group different than last row
         if (name != parameters[0]):
               #send current fadeListRGB parameters to Nao
               ledProxy.post.fadeListRGB(name, rgbList, timeList)
               #print 'ledProxy.post.fadeListRGB(', name, rgbList, timeList, ')'
               #intialize fadeListRGB parameters
               name = parameters[0]
               rgbList = []
               timeList = []

         #add this row to fadeListRGB parameters
         rgbList.append(256*256*int(parameters[1])+256*int(parameters[2])+int(parameters[3]))
         timeList.append(float(parameters[5]))

    #all done - send current fadeListRGB parameters to Nao
    ledProxy.post.fadeListRGB(name, rgbList, timeList) 
    #print 'ledProxy.post.fadeListRGB(', name, rgbList, timeList, ')'
          
    return file_load

def GetAvailableModules():
    dir_file = []
    list_path = sys.path
    filefound = False
    for i in range (0,len(list_path)):
        if os.path.exists(list_path[i]+"/modules"):
            filefound = True
            break

    if not filefound:
        print ("Could not find /modules directory!")
        raise IOError
        return None

    list_dir = os.listdir(list_path[i]+"/modules")

    for directory in list_dir:
        if not directory.startswith('.'):
            list_subdir = os.listdir(list_path[i]+"/modules/"+directory)
            module_files = ["/modules/",directory+"/"]
            for file_name in list_subdir:
                if not file_name.startswith("."):
                    module_files.append(file_name)
                    #module_files.append([directory,file_name])
            dir_file.append(module_files)
    return dir_file
    
def InitSpeech(wordList=["yes","no","hello NAO","goodbye NAO"],the_language="English",wordSpotting=False):
    global speechProxy
    global memoryProxy
    
    #Creating a proxy on the module
    #Before calling the ASR commands, you need to create a proxy on the ASR module:
#    asr = ALProxy("ALSpeechRecognition",myIP,9559) #IP = address of your robot
    #asr=speechProxy
    
    #Before starting the ASR engine, you must set the language of the speech recognition system. The list of the installed languages can be obtained through the getAvailableLanguages method.
    asr.setLanguage(the_language)

    #Note that this does not affect the language of speech synthesis. 
    #We will assume that it must be the same:
    tts.setLanguage(the_language)

    # To set the words that should be recognized, use the setWordListAsVocabulary method.
    asr.setVocabulary(wordList,wordSpotting)

    #Note:
    #The following feature (the usage of the "loadVocabulary()" function) is not available for Chinese and Japanese.
    #If you prefer not to use the setWordListAsVocabulary function, you can directly defined a vocabulary in a .lxd file and load it with the loadVocabulary method as described below:

    # Example: load the vocabulary defined in the file /home/nao/MyVocabulary.lxd asr.loadVocabulary(/home/nao/MyVocabulary.lxd)

    #Defining your vocabulary in a .lxd file and load it with the loadVocabulary function allows you to add alternative phonetic transcriptions that refine the automatic transcriptions of the ASR, and can improve performances. For example, if you want the speech recognition to be robust to the different pronunciations of the word "hello", you can define your vocabulary file as follows:

    #!Language=English #!FSG <words>=alt("yes" "no" "hello" "goodbye" )alt; <start>=alt(<words>)alt; #!Transcriptions hello h@l@U hello h@ll@U

    #The phonetic alphabet used to write these phonetizations is described here: http://www.phon.ucl.ac.uk/home/sampa/.

    #Collecting the recognized word in the memory
    #If a word has been recognized, the result is placed in the "WordRecognized" key of ALMemory.
    #As a result, you can read it by accessing this key in the ALMemory module.

    # Clear event WordRecognized in ALMemory module. 
    memoryProxy.insertData("WordRecognized",[])

    
def DetectSpeech():
    global memoryProxy
    
    try:
        #getData
        result=memoryProxy.getData("WordRecognized")
        if len(result)>0:
            memoryProxy.insertData("WordRecognized",[])

    except RuntimeError:
      # catch exception
      print ("error getting data")

    return result

def InitLandMark(switch=True, period = 500):
    # Subscribe to the ALLandMarkDetection extractor
    global landmarkProxy
    
    landmarkProxy.subscribe(__nao_module_name__ , period, 0.0 )
    if switch:
        try:
            landmarkProxy.subscribe(__nao_module_name__ , period, 0.0 )
        except:
            print ("Could not subscribe to ALLandMarkDetection")
    else:
        try:
            landmarkProxy.unsubscribe(__nao_module_name__ )
        except:
            print ("Could not unsubscribe from ALLandMarkDetection")
            
def DetectLandMark():
    # Get data from landmark detection (assuming face detection has been activated).
    global memoryProxy

    data = memoryProxy.getData("LandmarkDetected")

    if data==None:
        data=[] # otherwise the next statement fails ...        
    if len(data)==0:
        detected=False
        timestamp=time()
        markerInfo=[]
    else:
        detected=True
        #timestamp=data[0][0]+1E-6*data[0][1] #this works but only if a landmark is detected
        timestamp=time()
        markerInfo=[]
        for p in data[1]:
            markerInfo.append([p[1][0], #markerID
                               p[0][1], #alpha - x location in camera angle
                               p[0][2], #beta  - y location
                               p[0][3], #sizeX
                               p[0][4], #sizeY
                               p[0][5]  #orientation about vertical w.r. Nao's head
                               ])
    return detected, timestamp, markerInfo

def InitSoundDetection(switch=True):
    # Subscribe to the ALSoundDetection
    global soundProxy

    soundProxy.setParameter("Sensitivity", 0.3)    
    if switch:
        try:
            soundProxy.subscribe(__nao_module_name__ )
        except:
            print ("Could not subscribe to ALSoundDetection")
    else:
        try:
            soundProxy.unsubscribe(__nao_module_name__ )
        except:
            print ("Could not unsubscribe from ALSoundDetection")


def DetectSound():
    # Get data from landmark detection (assuming face detection has been activated).
    data = memoryProxy.getData("SoundDetected")

    ##The SoundDetected key is organized as follows:
    ##
    ##[[index_1, type_1, confidence_1, time_1],
    ## ...,
    ##[index_n, type_n, confidence_n, time_n]]
    ##
    ##n is the number of sounds detected in the last audio buffer,
    ##index is the index (in samples) of either the sound start (if type is equal to 1) or the sound end (if type is equal to 0),
    ##time is the detection time in micro seconds
    ##confidence gives an estimate of the probability [0;1] that the sound detected by the module corresponds to a real sound.
    if data==None:
        data=[] # otherwise the next statement fails ... 
    if len(data)==0:
        detected=False
        timestamp=time()
        soundInfo=[]
    else:
        detected=True
        timestamp=time()
        soundInfo=[]
        for snd in data:
            soundInfo.append([ snd[0], #index of sound start/end
                               snd[1], #type: 1=start, 0=end
                               snd[2]  #confidence: probability that there was a sound
                               ])
        memoryProxy.insertData("SoundDetected",[]) #clear memory
    return detected, timestamp, soundInfo


def InitSoundLocalization(switch=True):
    # Subscribe to the ALSoundDetection
    global soundLocalizationProxy
    
    if switch:
        try:
            soundLocalizationProxy.subscribe(__nao_module_name__ )
        except:
            print ("Could not subscribe to ALSoundDetection")
    else:
        try:
            soundLocalizationProxy.unsubscribe(__nao_module_name__ )
        except:
            print ("Could not subscribe to ALSoundDetection")


def DetectSoundLocation():
    # Get data from landmark detection (assuming face detection has been activated).
    global memoryProxy
    
    data = memoryProxy.getData("ALSoundLocalization/SoundLocated")

    ##The SoundDetected key is organized as follows:
    ##
    ##[ [time(sec), time(usec)],
    ##
    ##  [azimuth(rad), elevation(rad), confidence],
    ##
    ##  [Head Position[6D]]
    ##]

    if data==None:
        data=[] # otherwise the next statement fails ... 
    if len(data)==0:
        detected=False
        timestamp=time()
        soundInfo=[]
    else:
        detected=True
        #timestamp=data[0][0]+1E-6*data[0][1] #this works but only if a sound is located
        timestamp=time()
        soundInfo=[]
        for snd in data:
            soundInfo.append([ snd[1][0], #azimuth angle
                               snd[1][1], #elvation angle
                               snd[1][2], #confidence: probability that there was a sound
                               snd[2]])   #Headposition 6D
        memoryProxy.insertData("ALSoundLocalization/SoundLocated",[]) #clear memory
    return detected, timestamp, soundInfo


def give_pos():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.5, 1, 1.2, 1.5, 1.8, 2.1, 2.6, 3, 3.2, 3.5, 3.8, 4.1, 4.6, 5, 5.2, 5.5, 5.8, 6.1, 6.6, 7, 7.2, 7.5, 7.8, 8.1, 8.6, 10])
    keys.append([[-0.0046272, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.185656, [3, -0.166667, 0], [3, 0.0666667, 0]], [0.0291041, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0], [3, 0.1, 0]], [0.00149202, [3, -0.1, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0.044486], [3, 0.166667, -0.0741434]], [-0.354396, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.185656, [3, -0.133333, -0.0852223], [3, 0.0666667, 0.0426111]], [0.0291041, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0], [3, 0.1, 0]], [0.00149202, [3, -0.1, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0.044486], [3, 0.166667, -0.0741434]], [-0.354396, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.185656, [3, -0.133333, -0.0852223], [3, 0.0666667, 0.0426111]], [0.0291041, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0], [3, 0.1, 0]], [0.00149202, [3, -0.1, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0.044486], [3, 0.166667, -0.0741434]], [-0.354396, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.185656, [3, -0.133333, -0.0852223], [3, 0.0666667, 0.0426111]], [0.0291041, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0], [3, 0.1, 0]], [0.00149202, [3, -0.1, 0], [3, 0.1, 0]], [-0.185656, [3, -0.1, 0.044486], [3, 0.166667, -0.0741434]], [-0.354396, [3, -0.166667, 0], [3, 0.466667, 0]], [-0.00261907, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([0.5, 1, 1.2, 1.5, 1.8, 2.1, 2.6, 3, 3.2, 3.5, 3.8, 4.1, 4.6, 5, 5.2, 5.5, 5.8, 6.1, 6.6, 7, 7.2, 7.5, 7.8, 8.1, 8.6, 10])
    keys.append([[-0.00354174, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.00157595, [3, -0.166667, 0], [3, 0.0666667, 0]], [-0.00157595, [3, -0.0666667, 0], [3, 0.1, 0]], [0.00609397, [3, -0.1, 0], [3, 0.1, 0]], [-4.19617e-05, [3, -0.1, 0], [3, 0.1, 0]], [0.00609397, [3, -0.1, -0.00613594], [3, 0.166667, 0.0102266]], [0.431013, [3, -0.166667, 0], [3, 0.133333, 0]], [0.00157595, [3, -0.133333, 0], [3, 0.0666667, 0]], [0.00157595, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.00609397, [3, -0.1, 0], [3, 0.1, 0]], [4.19617e-05, [3, -0.1, 0], [3, 0.1, 0]], [-0.00609397, [3, -0.1, 0.00613594], [3, 0.166667, -0.0102266]], [-0.431013, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.00157595, [3, -0.133333, 0], [3, 0.0666667, 0]], [-0.00157595, [3, -0.0666667, 0], [3, 0.1, 0]], [0.00609397, [3, -0.1, 0], [3, 0.1, 0]], [-4.19617e-05, [3, -0.1, 0], [3, 0.1, 0]], [0.00609397, [3, -0.1, -0.00613594], [3, 0.166667, 0.0102266]], [0.431013, [3, -0.166667, 0], [3, 0.133333, 0]], [0.00157595, [3, -0.133333, 0], [3, 0.0666667, 0]], [0.00157595, [3, -0.0666667, 0], [3, 0.1, 0]], [-0.00609397, [3, -0.1, 0], [3, 0.1, 0]], [4.19617e-05, [3, -0.1, 0], [3, 0.1, 0]], [-0.00609397, [3, -0.1, 0.00613594], [3, 0.166667, -0.0102266]], [-0.431013, [3, -0.166667, 0], [3, 0.466667, 0]], [-0.0041901, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnklePitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.35, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.417291, [3, -0.166667, 0.0357647], [3, 0.233333, -0.0500706]], [-0.607505, [3, -0.233333, 0.0371355], [3, 0.3, -0.0477457]], [-0.671934, [3, -0.3, 0], [3, 0.133333, 0]], [-0.31136, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.443284, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.417291, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.607505, [3, -0.233333, 0.0371355], [3, 0.3, -0.0477457]], [-0.671934, [3, -0.3, 0], [3, 0.133333, 0]], [-0.31136, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.443284, [3, -0.533333, 0], [3, 0.466667, 0]], [-0.344847, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnkleRoll")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.00902358, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.0858622, [3, -0.166667, 0.0162115], [3, 0.233333, -0.022696]], [-0.125746, [3, -0.233333, 0], [3, 0.3, 0]], [-0.105804, [3, -0.3, 0], [3, 0.133333, 0]], [-0.124296, [3, -0.133333, 0.0139139], [3, 0.533333, -0.0556554]], [-0.314512, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.0858622, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.125746, [3, -0.233333, 0], [3, 0.3, 0]], [-0.105804, [3, -0.3, 0], [3, 0.133333, 0]], [-0.124296, [3, -0.133333, 0.0139139], [3, 0.533333, -0.0556554]], [-0.314512, [3, -0.533333, 0], [3, 0.466667, 0]], [-0.00744537, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowRoll")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[-1.00398, [3, -0.166667, 0], [3, 0.166667, 0]], [-1.24863, [3, -0.166667, 0], [3, 0.0333333, 0]], [-1.07529, [3, -0.0333333, -0.0429523], [3, 0.0333333, 0.0429523]], [-0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.4005, [3, -0.0333333, 0.0922825], [3, 0.0333333, -0.0922825]], [-1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.39897, [3, -0.0333333, -0.0493303], [3, 0.0333333, 0.0493303]], [-1.24863, [3, -0.0333333, -0.0453384], [3, 0.0666667, 0.0906768]], [-0.990921, [3, -0.0666667, 0], [3, 0.0333333, 0]], [-1.4005, [3, -0.0333333, 0.0922825], [3, 0.0333333, -0.0922825]], [-1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.39897, [3, -0.0333333, -0.0285789], [3, 0.166667, 0.142894]], [-1.0302, [3, -0.166667, 0], [3, 0.133333, 0]], [-1.33309, [3, -0.133333, 0.0552222], [3, 0.0333333, -0.0138056]], [-1.34689, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.31468, [3, -0.0333333, -0.0999658], [3, 0.0333333, 0.0999658]], [-0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.16281, [3, -0.0333333, 0.083603], [3, 0.0333333, -0.083603]], [-1.33309, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.34689, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.31468, [3, -0.0333333, -0.0999658], [3, 0.0333333, 0.0999658]], [-0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.16281, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.929527, [3, -0.166667, 0], [3, 0.133333, 0]], [-1.24863, [3, -0.133333, 0], [3, 0.0333333, 0]], [-1.07529, [3, -0.0333333, -0.0429523], [3, 0.0333333, 0.0429523]], [-0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.4005, [3, -0.0333333, 0.0922825], [3, 0.0333333, -0.0922825]], [-1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.39897, [3, -0.0333333, -0.0493303], [3, 0.0333333, 0.0493303]], [-1.24863, [3, -0.0333333, -0.0453384], [3, 0.0666667, 0.0906768]], [-0.990921, [3, -0.0666667, 0], [3, 0.0333333, 0]], [-1.4005, [3, -0.0333333, 0.0922825], [3, 0.0333333, -0.0922825]], [-1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.39897, [3, -0.0333333, -0.0285789], [3, 0.166667, 0.142894]], [-1.0302, [3, -0.166667, 0], [3, 0.133333, 0]], [-1.33309, [3, -0.133333, 0.0552222], [3, 0.0333333, -0.0138056]], [-1.34689, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.31468, [3, -0.0333333, -0.0999658], [3, 0.0333333, 0.0999658]], [-0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.16281, [3, -0.0333333, 0.083603], [3, 0.0333333, -0.083603]], [-1.33309, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.34689, [3, -0.0333333, 0.0138056], [3, 0.0333333, -0.0138056]], [-1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.31468, [3, -0.0333333, -0.0999658], [3, 0.0333333, 0.0999658]], [-0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-1.16281, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.929527, [3, -0.166667, 0], [3, 0.466667, 0]], [-1.00802, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[-1.38417, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.434165, [3, -0.166667, -0.296275], [3, 0.0333333, 0.059255]], [-0.31758, [3, -0.0333333, -0.0449974], [3, 0.0333333, 0.0449974]], [-0.16418, [3, -0.0333333, -0.0631497], [3, 0.0333333, 0.0631497]], [0.061318, [3, -0.0333333, -0.0590701], [3, 0.0333333, 0.0590701]], [0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176453, [3, -0.0333333, 0.104068], [3, 0.0333333, -0.104068]], [-0.434165, [3, -0.0333333, 0], [3, 0.0666667, 0]], [-0.165714, [3, -0.0666667, -0.110107], [3, 0.0333333, 0.0550536]], [0.061318, [3, -0.0333333, -0.0593258], [3, 0.0333333, 0.0593258]], [0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176453, [3, -0.0333333, 0.107026], [3, 0.166667, -0.535128]], [-1.73622, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.185572, [3, -0.133333, -0.165672], [3, 0.0333333, 0.041418]], [-0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.174835, [3, -0.0333333, 0.0306808], [3, 0.0333333, -0.0306808]], [-0.351244, [3, -0.0333333, 0.0452529], [3, 0.0333333, -0.0452529]], [-0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.036858, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.185572, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176367, [3, -0.0333333, 0.0322132], [3, 0.0333333, -0.0322132]], [-0.351244, [3, -0.0333333, 0.0449975], [3, 0.0333333, -0.0449975]], [-0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.036858, [3, -0.0333333, -0.0457293], [3, 0.166667, 0.228646]], [0.376775, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.434165, [3, -0.133333, 0], [3, 0.0333333, 0]], [-0.31758, [3, -0.0333333, -0.0449974], [3, 0.0333333, 0.0449974]], [-0.16418, [3, -0.0333333, -0.0631497], [3, 0.0333333, 0.0631497]], [0.061318, [3, -0.0333333, -0.0590701], [3, 0.0333333, 0.0590701]], [0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176453, [3, -0.0333333, 0.104068], [3, 0.0333333, -0.104068]], [-0.434165, [3, -0.0333333, 0], [3, 0.0666667, 0]], [-0.165714, [3, -0.0666667, -0.110107], [3, 0.0333333, 0.0550536]], [0.061318, [3, -0.0333333, -0.0593258], [3, 0.0333333, 0.0593258]], [0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176453, [3, -0.0333333, 0.107026], [3, 0.166667, -0.535128]], [-1.73622, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.185572, [3, -0.133333, -0.165672], [3, 0.0333333, 0.041418]], [-0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.174835, [3, -0.0333333, 0.0306808], [3, 0.0333333, -0.0306808]], [-0.351244, [3, -0.0333333, 0.0452529], [3, 0.0333333, -0.0452529]], [-0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.036858, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.185572, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.176367, [3, -0.0333333, 0.0322132], [3, 0.0333333, -0.0322132]], [-0.351244, [3, -0.0333333, 0.0449975], [3, 0.0333333, -0.0449975]], [-0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.036858, [3, -0.0333333, -0.0457293], [3, 0.166667, 0.228646]], [0.376775, [3, -0.166667, 0], [3, 0.466667, 0]], [-1.38515, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[0.251572, [3, -0.166667, 0], [3, 0.166667, 0]], [0, [3, -0.166667, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.188, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, -0.0554293], [3, 0.166667, 0.277147]], [0.997728, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0.000399992], [3, 0.0333333, -0.000399992]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0], [3, 0.166667, 0]], [1, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.188, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, -0.0554293], [3, 0.166667, 0.277147]], [0.997728, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0.000399992], [3, 0.0333333, -0.000399992]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0], [3, 0.166667, 0]], [1, [3, -0.166667, 0], [3, 0.466667, 0]], [0.259178, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipPitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.45, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.052114, [3, -0.166667, 0], [3, 0.233333, 0]], [-0.33437, [3, -0.233333, 0.0516766], [3, 0.3, -0.0664414]], [-0.406468, [3, -0.3, 0], [3, 0.133333, 0]], [-0.0767419, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.104354, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.052114, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.33437, [3, -0.233333, 0.0516766], [3, 0.3, -0.0664414]], [-0.406468, [3, -0.3, 0], [3, 0.133333, 0]], [-0.0767419, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.104354, [3, -0.533333, 0.027612], [3, 0.466667, -0.0241605]], [-0.443326, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipRoll")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[0.00159365, [3, -0.166667, 0], [3, 0.166667, 0]], [0.1335, [3, -0.166667, -0.0240729], [3, 0.233333, 0.0337021]], [0.174919, [3, -0.233333, -0.0208048], [3, 0.3, 0.0267491]], [0.276162, [3, -0.3, 0], [3, 0.133333, 0]], [0.128814, [3, -0.133333, 0], [3, 0.533333, 0]], [0.208583, [3, -0.533333, 0], [3, 0.133333, 0]], [0.1335, [3, -0.133333, 0], [3, 0.233333, 0]], [0.174919, [3, -0.233333, -0.0208048], [3, 0.3, 0.0267491]], [0.276162, [3, -0.3, 0], [3, 0.133333, 0]], [0.128814, [3, -0.133333, 0], [3, 0.533333, 0]], [0.208583, [3, -0.533333, 0], [3, 0.466667, 0]], [0.00755153, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipYawPitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.00420801, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.36505, [3, -0.166667, 0.00986112], [3, 0.233333, -0.0138056]], [-0.378855, [3, -0.233333, 0], [3, 0.3, 0]], [-0.371186, [3, -0.3, -0.0031859], [3, 0.133333, 0.00141596]], [-0.36505, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.371186, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.36505, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.378855, [3, -0.233333, 0], [3, 0.3, 0]], [-0.371186, [3, -0.3, -0.0031859], [3, 0.133333, 0.00141596]], [-0.36505, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.371186, [3, -0.533333, 0], [3, 0.466667, 0]], [0, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LKneePitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[0.699999, [3, -0.166667, 0], [3, 0.166667, 0]], [0.731677, [3, -0.166667, -0.0316778], [3, 0.233333, 0.0443489]], [1.13358, [3, -0.233333, -0.0829957], [3, 0.3, 0.106709]], [1.30079, [3, -0.3, 0], [3, 0.133333, 0]], [0.653526, [3, -0.133333, 0], [3, 0.533333, 0]], [0.856014, [3, -0.533333, 0], [3, 0.133333, 0]], [0.731677, [3, -0.133333, 0], [3, 0.233333, 0]], [1.13358, [3, -0.233333, -0.0829957], [3, 0.3, 0.106709]], [1.30079, [3, -0.3, 0], [3, 0.133333, 0]], [0.653526, [3, -0.133333, 0], [3, 0.533333, 0]], [0.856014, [3, -0.533333, 0], [3, 0.466667, 0]], [0.691105, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[1.40432, [3, -0.166667, 0], [3, 0.166667, 0]], [0.357381, [3, -0.166667, 0], [3, 0.0333333, 0]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, -0.0426919], [3, 0.0333333, 0.0426919]], [0.357381, [3, -0.0333333, -0.0335774], [3, 0.0666667, 0.0671548]], [0.584411, [3, -0.0666667, -0.0429527], [3, 0.0333333, 0.0214763]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.583692, [3, -0.166667, 0], [3, 0.133333, 0]], [0.624379, [3, -0.133333, -0.35406], [3, 0.0333333, 0.088515]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.624379, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.708379, [3, -0.166667, 0.0172456], [3, 0.133333, -0.0137965]], [0.357381, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, -0.0426919], [3, 0.0333333, 0.0426919]], [0.357381, [3, -0.0333333, -0.0335774], [3, 0.0666667, 0.0671548]], [0.584411, [3, -0.0666667, -0.0429527], [3, 0.0333333, 0.0214763]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.583692, [3, -0.166667, 0], [3, 0.133333, 0]], [0.624379, [3, -0.133333, -0.35406], [3, 0.0333333, 0.088515]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.624379, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.708379, [3, -0.166667, 0], [3, 0.466667, 0]], [1.40104, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[0.293252, [3, -0.166667, 0], [3, 0.166667, 0]], [0.159494, [3, -0.166667, 0.0422683], [3, 0.0333333, -0.00845366]], [0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0889301, [3, -0.0333333, 0.0404302], [3, 0.0333333, -0.0404302]], [-0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.066004, [3, -0.0333333, -0.0247531], [3, 0.0333333, 0.0247531]], [0.159494, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.151824, [3, -0.0666667, 0.00767004], [3, 0.0333333, -0.00383502]], [0.0889301, [3, -0.0333333, 0.0404302], [3, 0.0333333, -0.0404302]], [-0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.066004, [3, -0.0333333, -0.0247531], [3, 0.166667, 0.123766]], [0.536495, [3, -0.166667, 0], [3, 0.133333, 0]], [0.0337899, [3, -0.133333, 0.186824], [3, 0.0333333, -0.0467061]], [-0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0843279, [3, -0.0333333, -0.0217316], [3, 0.0333333, 0.0217316]], [-0.052114, [3, -0.0333333, -0.0196863], [3, 0.0333333, 0.0196863]], [0.0337899, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0843279, [3, -0.0333333, -0.0217316], [3, 0.0333333, 0.0217316]], [-0.052114, [3, -0.0333333, -0.0157946], [3, 0.166667, 0.0789729]], [0.199975, [3, -0.166667, 0], [3, 0.133333, 0]], [0.159494, [3, -0.133333, 0.0157036], [3, 0.0333333, -0.0039259]], [0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0889301, [3, -0.0333333, 0.0404302], [3, 0.0333333, -0.0404302]], [-0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.066004, [3, -0.0333333, -0.0247531], [3, 0.0333333, 0.0247531]], [0.159494, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.151824, [3, -0.0666667, 0.00767004], [3, 0.0333333, -0.00383502]], [0.0889301, [3, -0.0333333, 0.0404302], [3, 0.0333333, -0.0404302]], [-0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.066004, [3, -0.0333333, -0.0247531], [3, 0.166667, 0.123766]], [0.536495, [3, -0.166667, 0], [3, 0.133333, 0]], [0.0337899, [3, -0.133333, 0.186824], [3, 0.0333333, -0.0467061]], [-0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0843279, [3, -0.0333333, -0.0217316], [3, 0.0333333, 0.0217316]], [-0.052114, [3, -0.0333333, -0.0196863], [3, 0.0333333, 0.0196863]], [0.0337899, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0843279, [3, -0.0333333, -0.0217316], [3, 0.0333333, 0.0217316]], [-0.052114, [3, -0.0333333, -0.0157946], [3, 0.166667, 0.0789729]], [0.199975, [3, -0.166667, -0.030547], [3, 0.466667, 0.0855317]], [0.296122, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[-0.0064736, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.573758, [3, -0.166667, 0.169084], [3, 0.0333333, -0.0338168]], [-0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.412688, [3, -0.0333333, -0.0700526], [3, 0.0333333, 0.0700526]], [-0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.763974, [3, -0.0333333, -0.0646531], [3, 0.0333333, 0.0646531]], [-0.573758, [3, -0.0333333, -0.0390318], [3, 0.0666667, 0.0780635]], [-0.412688, [3, -0.0666667, -0.0841993], [3, 0.0333333, 0.0420997]], [-0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.763974, [3, -0.0333333, -0.122614], [3, 0.166667, 0.613071]], [1.24538, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.421808, [3, -0.133333, 0], [3, 0.0333333, 0]], [-0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.46476, [3, -0.0333333, 0.0127834], [3, 0.0333333, -0.0127834]], [-0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.472429, [3, -0.0333333, -0.0138073], [3, 0.0333333, 0.0138073]], [-0.131882, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.421808, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.46476, [3, -0.0333333, 0.0127834], [3, 0.0333333, -0.0127834]], [-0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.472429, [3, -0.0333333, -0.0138073], [3, 0.0333333, 0.0138073]], [-0.131882, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.574861, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.573758, [3, -0.133333, 0], [3, 0.0333333, 0]], [-0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.412688, [3, -0.0333333, -0.0700526], [3, 0.0333333, 0.0700526]], [-0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.763974, [3, -0.0333333, -0.0646531], [3, 0.0333333, 0.0646531]], [-0.573758, [3, -0.0333333, -0.0390318], [3, 0.0666667, 0.0780635]], [-0.412688, [3, -0.0666667, -0.0841993], [3, 0.0333333, 0.0420997]], [-0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.763974, [3, -0.0333333, -0.122614], [3, 0.166667, 0.613071]], [1.24538, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.421808, [3, -0.133333, 0], [3, 0.0333333, 0]], [-0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.46476, [3, -0.0333333, 0.0127834], [3, 0.0333333, -0.0127834]], [-0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.472429, [3, -0.0333333, -0.0138073], [3, 0.0333333, 0.0138073]], [-0.131882, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.421808, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.46476, [3, -0.0333333, 0.0127834], [3, 0.0333333, -0.0127834]], [-0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.472429, [3, -0.0333333, -0.0138073], [3, 0.0333333, 0.0138073]], [-0.131882, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.574861, [3, -0.166667, 0], [3, 0.466667, 0]], [0.00759608, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnklePitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.35, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.31136, [3, -0.166667, 0], [3, 0.233333, 0]], [-0.355846, [3, -0.233333, 0.0192389], [3, 0.3, -0.0247358]], [-0.443284, [3, -0.3, 0], [3, 0.133333, 0]], [-0.417291, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.671934, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.31136, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.355846, [3, -0.233333, 0.0192389], [3, 0.3, -0.0247358]], [-0.443284, [3, -0.3, 0], [3, 0.133333, 0]], [-0.417291, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.671934, [3, -0.533333, 0], [3, 0.466667, 0]], [-0.34488, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnkleRoll")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[0.00303459, [3, -0.166667, 0], [3, 0.166667, 0]], [0.124296, [3, -0.166667, -0.0142444], [3, 0.233333, 0.0199421]], [0.144238, [3, -0.233333, -0.0199421], [3, 0.3, 0.0256399]], [0.314512, [3, -0.3, 0], [3, 0.133333, 0]], [0.0858622, [3, -0.133333, 0], [3, 0.533333, 0]], [0.105804, [3, -0.533333, -0.010249], [3, 0.133333, 0.00256225]], [0.124296, [3, -0.133333, -0.00465867], [3, 0.233333, 0.00815268]], [0.144238, [3, -0.233333, -0.0199421], [3, 0.3, 0.0256399]], [0.314512, [3, -0.3, 0], [3, 0.133333, 0]], [0.0858622, [3, -0.133333, 0], [3, 0.533333, 0]], [0.105804, [3, -0.533333, 0], [3, 0.466667, 0]], [0.000827394, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[1.00348, [3, -0.166667, 0], [3, 0.166667, 0]], [1.33309, [3, -0.166667, -0.0690278], [3, 0.0333333, 0.0138056]], [1.34689, [3, -0.0333333, -0.0138056], [3, 0.0333333, 0.0138056]], [1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.31468, [3, -0.0333333, 0.0999658], [3, 0.0333333, -0.0999658]], [0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.16281, [3, -0.0333333, -0.083603], [3, 0.0333333, 0.083603]], [1.33309, [3, -0.0333333, -0.0298279], [3, 0.0666667, 0.0596558]], [1.43126, [3, -0.0666667, 0], [3, 0.0333333, 0]], [1.31468, [3, -0.0333333, 0.0999658], [3, 0.0333333, -0.0999658]], [0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.16281, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.9362, [3, -0.166667, 0], [3, 0.133333, 0]], [1.24863, [3, -0.133333, 0], [3, 0.0333333, 0]], [1.07529, [3, -0.0333333, 0.0429523], [3, 0.0333333, -0.0429523]], [0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.4005, [3, -0.0333333, -0.0922825], [3, 0.0333333, 0.0922825]], [1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.39897, [3, -0.0333333, 0.0493303], [3, 0.0333333, -0.0493303]], [1.24863, [3, -0.0333333, 0.0539458], [3, 0.0333333, -0.0539458]], [1.07529, [3, -0.0333333, 0.0429523], [3, 0.0333333, -0.0429523]], [0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.4005, [3, -0.0333333, -0.0922825], [3, 0.0333333, 0.0922825]], [1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.39897, [3, -0.0333333, 0.0562086], [3, 0.166667, -0.281043]], [0.532861, [3, -0.166667, 0], [3, 0.133333, 0]], [1.33309, [3, -0.133333, -0.0552222], [3, 0.0333333, 0.0138056]], [1.34689, [3, -0.0333333, -0.0138056], [3, 0.0333333, 0.0138056]], [1.43126, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.31468, [3, -0.0333333, 0.0999658], [3, 0.0333333, -0.0999658]], [0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.16281, [3, -0.0333333, -0.083603], [3, 0.0333333, 0.083603]], [1.33309, [3, -0.0333333, -0.0298279], [3, 0.0666667, 0.0596558]], [1.43126, [3, -0.0666667, 0], [3, 0.0333333, 0]], [1.31468, [3, -0.0333333, 0.0999658], [3, 0.0333333, -0.0999658]], [0.83147, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.16281, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.9362, [3, -0.166667, 0], [3, 0.133333, 0]], [1.24863, [3, -0.133333, 0], [3, 0.0333333, 0]], [1.07529, [3, -0.0333333, 0.0429523], [3, 0.0333333, -0.0429523]], [0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.4005, [3, -0.0333333, -0.0922825], [3, 0.0333333, 0.0922825]], [1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.39897, [3, -0.0333333, 0.0493303], [3, 0.0333333, -0.0493303]], [1.24863, [3, -0.0333333, 0.0539458], [3, 0.0333333, -0.0539458]], [1.07529, [3, -0.0333333, 0.0429523], [3, 0.0333333, -0.0429523]], [0.990921, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.4005, [3, -0.0333333, -0.0922825], [3, 0.0333333, 0.0922825]], [1.54462, [3, -0.0333333, 0], [3, 0.0333333, 0]], [1.39897, [3, -0.0333333, 0.0562086], [3, 0.166667, -0.281043]], [0.532861, [3, -0.166667, 0], [3, 0.466667, 0]], [1.00797, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[1.38479, [3, -0.166667, 0], [3, 0.166667, 0]], [0.185572, [3, -0.166667, 0.20709], [3, 0.0333333, -0.041418]], [0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.174835, [3, -0.0333333, -0.0306808], [3, 0.0333333, 0.0306808]], [0.351244, [3, -0.0333333, -0.0452529], [3, 0.0333333, 0.0452529]], [0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.036858, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.185572, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.176367, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.351244, [3, -0.0333333, -0.0449975], [3, 0.0333333, 0.0449975]], [0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.036858, [3, -0.0333333, 0.0459114], [3, 0.166667, -0.229557]], [-0.380052, [3, -0.166667, 0], [3, 0.133333, 0]], [0.434165, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.31758, [3, -0.0333333, 0.0449974], [3, 0.0333333, -0.0449974]], [0.16418, [3, -0.0333333, 0.0631497], [3, 0.0333333, -0.0631497]], [-0.061318, [3, -0.0333333, 0.0590701], [3, 0.0333333, -0.0590701]], [-0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.176453, [3, -0.0333333, -0.104068], [3, 0.0333333, 0.104068]], [0.434165, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.31758, [3, -0.0333333, 0.0447418], [3, 0.0333333, -0.0447418]], [0.165714, [3, -0.0333333, 0.0631497], [3, 0.0333333, -0.0631497]], [-0.061318, [3, -0.0333333, 0.0593258], [3, 0.0333333, -0.0593258]], [-0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.176453, [3, -0.0333333, -0.108634], [3, 0.166667, 0.543171]], [1.76517, [3, -0.166667, 0], [3, 0.133333, 0]], [0.185572, [3, -0.133333, 0.165672], [3, 0.0333333, -0.041418]], [0.144154, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.174835, [3, -0.0333333, -0.0306808], [3, 0.0333333, 0.0306808]], [0.351244, [3, -0.0333333, -0.0452529], [3, 0.0333333, 0.0452529]], [0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.036858, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.185572, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.176367, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.351244, [3, -0.0333333, -0.0449975], [3, 0.0333333, 0.0449975]], [0.446352, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.036858, [3, -0.0333333, 0.0459114], [3, 0.166667, -0.229557]], [-0.380052, [3, -0.166667, 0], [3, 0.133333, 0]], [0.434165, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.31758, [3, -0.0333333, 0.0449974], [3, 0.0333333, -0.0449974]], [0.16418, [3, -0.0333333, 0.0631497], [3, 0.0333333, -0.0631497]], [-0.061318, [3, -0.0333333, 0.0590701], [3, 0.0333333, -0.0590701]], [-0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.176453, [3, -0.0333333, -0.104068], [3, 0.0333333, 0.104068]], [0.434165, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.31758, [3, -0.0333333, 0.0447418], [3, 0.0333333, -0.0447418]], [0.165714, [3, -0.0333333, 0.0631497], [3, 0.0333333, -0.0631497]], [-0.061318, [3, -0.0333333, 0.0593258], [3, 0.0333333, -0.0593258]], [-0.190241, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.176453, [3, -0.0333333, -0.108634], [3, 0.166667, 0.543171]], [1.76517, [3, -0.166667, 0], [3, 0.466667, 0]], [1.38466, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[0.251513, [3, -0.166667, 0], [3, 0.166667, 0]], [0, [3, -0.166667, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0.000399992], [3, 0.0333333, -0.000399992]], [0, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.178, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.996256, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, -0.0555556], [3, 0.166667, 0.277778]], [1, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1568, [3, -0.0333333, -0.0212], [3, 0.0333333, 0.0212]], [0.178, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0.000399992], [3, 0.0333333, -0.000399992]], [0, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.178, [3, -0.0666667, 0], [3, 0.0333333, 0]], [0.1616, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1672, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1668, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.996256, [3, -0.166667, 0], [3, 0.133333, 0]], [0, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1872, [3, -0.0333333, -0.000799999], [3, 0.0333333, 0.000799999]], [0.188, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.184, [3, -0.0333333, 0.00399999], [3, 0.0333333, -0.00399999]], [0, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.1908, [3, -0.0333333, -0.0555556], [3, 0.166667, 0.277778]], [1, [3, -0.166667, 0], [3, 0.466667, 0]], [0.25, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipPitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.45, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.0767419, [3, -0.166667, 0], [3, 0.233333, 0]], [-0.44797, [3, -0.233333, 0], [3, 0.3, 0]], [-0.104354, [3, -0.3, -0.0913514], [3, 0.133333, 0.0406006]], [-0.052114, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.406468, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.0767419, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.44797, [3, -0.233333, 0], [3, 0.3, 0]], [-0.104354, [3, -0.3, -0.0913514], [3, 0.133333, 0.0406006]], [-0.052114, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.406468, [3, -0.533333, 0.0422234], [3, 0.466667, -0.0369455]], [-0.443413, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipRoll")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.00288084, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.128814, [3, -0.166667, 0], [3, 0.233333, 0]], [-0.108872, [3, -0.233333, 0], [3, 0.3, 0]], [-0.208583, [3, -0.3, 0], [3, 0.133333, 0]], [-0.1335, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.276162, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.128814, [3, -0.133333, -0.0113955], [3, 0.233333, 0.0199421]], [-0.108872, [3, -0.233333, 0], [3, 0.3, 0]], [-0.208583, [3, -0.3, 0], [3, 0.133333, 0]], [-0.1335, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.276162, [3, -0.533333, 0], [3, 0.466667, 0]], [-0.000705859, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipYawPitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[-0.00420801, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.36505, [3, -0.166667, 0.00986112], [3, 0.233333, -0.0138056]], [-0.378855, [3, -0.233333, 0], [3, 0.3, 0]], [-0.371186, [3, -0.3, -0.0031859], [3, 0.133333, 0.00141596]], [-0.36505, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.371186, [3, -0.533333, 0], [3, 0.133333, 0]], [-0.36505, [3, -0.133333, 0], [3, 0.233333, 0]], [-0.378855, [3, -0.233333, 0], [3, 0.3, 0]], [-0.371186, [3, -0.3, -0.0031859], [3, 0.133333, 0.00141596]], [-0.36505, [3, -0.133333, 0], [3, 0.533333, 0]], [-0.371186, [3, -0.533333, 0], [3, 0.466667, 0]], [0, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RKneePitch")
    times.append([0.5, 1, 1.7, 2.6, 3, 4.6, 5, 5.7, 6.6, 7, 8.6, 10])
    keys.append([[0.699999, [3, -0.166667, 0], [3, 0.166667, 0]], [0.653526, [3, -0.166667, 0], [3, 0.233333, 0]], [1.00481, [3, -0.233333, 0], [3, 0.3, 0]], [0.856014, [3, -0.3, 0.0630312], [3, 0.133333, -0.0280139]], [0.731677, [3, -0.133333, 0], [3, 0.533333, 0]], [1.30079, [3, -0.533333, 0], [3, 0.133333, 0]], [0.653526, [3, -0.133333, 0], [3, 0.233333, 0]], [1.00481, [3, -0.233333, 0], [3, 0.3, 0]], [0.856014, [3, -0.3, 0.0630312], [3, 0.133333, -0.0280139]], [0.731677, [3, -0.133333, 0], [3, 0.533333, 0]], [1.30079, [3, -0.533333, 0], [3, 0.466667, 0]], [0.691105, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[1.40843, [3, -0.166667, 0], [3, 0.166667, 0]], [0.624379, [3, -0.166667, 0], [3, 0.0333333, 0]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.624379, [3, -0.0333333, 0.0238621], [3, 0.0666667, -0.0477243]], [0.510865, [3, -0.0666667, 0.0698822], [3, 0.0333333, -0.0349411]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.705232, [3, -0.166667, 0.0203924], [3, 0.133333, -0.0163139]], [0.357381, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, -0.0426919], [3, 0.0333333, 0.0426919]], [0.357381, [3, -0.0333333, -0.0380941], [3, 0.0333333, 0.0380941]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.578744, [3, -0.166667, 0], [3, 0.133333, 0]], [0.624379, [3, -0.133333, -0.35274], [3, 0.0333333, 0.0881851]], [0.744032, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.510865, [3, -0.0333333, 0.0723538], [3, 0.0333333, -0.0723538]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.624379, [3, -0.0333333, 0.0238621], [3, 0.0666667, -0.0477243]], [0.510865, [3, -0.0666667, 0.0698822], [3, 0.0333333, -0.0349411]], [0.309909, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.61671, [3, -0.0333333, -0.0692858], [3, 0.0333333, 0.0692858]], [0.725624, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.705232, [3, -0.166667, 0.0203924], [3, 0.133333, -0.0163139]], [0.357381, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, -0.0426919], [3, 0.0333333, 0.0426919]], [0.357381, [3, -0.0333333, -0.0380941], [3, 0.0333333, 0.0380941]], [0.510779, [3, -0.0333333, -0.0378384], [3, 0.0333333, 0.0378384]], [0.584411, [3, -0.0333333, -0.0158514], [3, 0.0333333, 0.0158514]], [0.605888, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.101229, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.282215, [3, -0.0333333, 0], [3, 0.166667, 0]], [-0.578744, [3, -0.166667, 0], [3, 0.466667, 0]], [1.40094, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[-0.297629, [3, -0.166667, 0], [3, 0.166667, 0]], [-0.0337899, [3, -0.166667, -0.128257], [3, 0.0333333, 0.0256514]], [0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0843279, [3, -0.0333333, 0.0217316], [3, 0.0333333, -0.0217316]], [0.052114, [3, -0.0333333, 0.0196863], [3, 0.0333333, -0.0196863]], [-0.0337899, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.124212, [3, -0.0666667, -0.0480653], [3, 0.0333333, 0.0240326]], [0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0843279, [3, -0.0333333, 0.0217316], [3, 0.0333333, -0.0217316]], [0.052114, [3, -0.0333333, 0.015521], [3, 0.166667, -0.0776052]], [-0.195051, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.159494, [3, -0.133333, -0.0143906], [3, 0.0333333, 0.00359766]], [-0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0889301, [3, -0.0333333, -0.0404302], [3, 0.0333333, 0.0404302]], [0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.066004, [3, -0.0333333, 0.0247531], [3, 0.0333333, -0.0247531]], [-0.159494, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0889301, [3, -0.0333333, -0.0404302], [3, 0.0333333, 0.0404302]], [0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.066004, [3, -0.0333333, 0.0205304], [3, 0.166667, -0.102652]], [-0.27879, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.0337899, [3, -0.133333, -0.118103], [3, 0.0333333, 0.0295257]], [0.164096, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.124212, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0843279, [3, -0.0333333, 0.0217316], [3, 0.0333333, -0.0217316]], [0.052114, [3, -0.0333333, 0.0196863], [3, 0.0333333, -0.0196863]], [-0.0337899, [3, -0.0333333, 0], [3, 0.0666667, 0]], [0.124212, [3, -0.0666667, -0.0480653], [3, 0.0333333, 0.0240326]], [0.182504, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.0843279, [3, -0.0333333, 0.0217316], [3, 0.0333333, -0.0217316]], [0.052114, [3, -0.0333333, 0.015521], [3, 0.166667, -0.0776052]], [-0.195051, [3, -0.166667, 0], [3, 0.133333, 0]], [-0.159494, [3, -0.133333, -0.0143906], [3, 0.0333333, 0.00359766]], [-0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0889301, [3, -0.0333333, -0.0404302], [3, 0.0333333, 0.0404302]], [0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.066004, [3, -0.0333333, 0.0247531], [3, 0.0333333, -0.0247531]], [-0.159494, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.141086, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.151824, [3, -0.0333333, 0], [3, 0.0333333, 0]], [-0.0889301, [3, -0.0333333, -0.0404302], [3, 0.0333333, 0.0404302]], [0.0907571, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.066004, [3, -0.0333333, 0.0205304], [3, 0.166667, -0.102652]], [-0.27879, [3, -0.166667, 0.00570368], [3, 0.466667, -0.0159703]], [-0.29476, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2, 2.1, 2.6, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.6, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8, 5.9, 6, 6.1, 6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.6, 10])
    keys.append([[-0.00104124, [3, -0.166667, 0], [3, 0.166667, 0]], [0.421808, [3, -0.166667, 0], [3, 0.0333333, 0]], [0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.46476, [3, -0.0333333, -0.0127834], [3, 0.0333333, 0.0127834]], [0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.472429, [3, -0.0333333, 0.0138073], [3, 0.0333333, -0.0138073]], [0.131882, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.421808, [3, -0.0333333, -0.0214763], [3, 0.0666667, 0.0429525]], [0.46476, [3, -0.0666667, -0.0143175], [3, 0.0333333, 0.00715876]], [0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.472429, [3, -0.0333333, 0.0138073], [3, 0.0333333, -0.0138073]], [0.131882, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.578728, [3, -0.166667, 0], [3, 0.133333, 0]], [0.573758, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.412688, [3, -0.0333333, 0.0700526], [3, 0.0333333, -0.0700526]], [0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.763974, [3, -0.0333333, 0.0646531], [3, 0.0333333, -0.0646531]], [0.573758, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.412688, [3, -0.0333333, 0.0700526], [3, 0.0333333, -0.0700526]], [0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.763974, [3, -0.0333333, 0.088914], [3, 0.166667, -0.44457]], [-0.638775, [3, -0.166667, 0], [3, 0.133333, 0]], [0.421808, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.409536, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.46476, [3, -0.0333333, -0.0127834], [3, 0.0333333, 0.0127834]], [0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.472429, [3, -0.0333333, 0.0138073], [3, 0.0333333, -0.0138073]], [0.131882, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.421808, [3, -0.0333333, -0.0214763], [3, 0.0666667, 0.0429525]], [0.46476, [3, -0.0666667, -0.0143175], [3, 0.0333333, 0.00715876]], [0.486237, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.472429, [3, -0.0333333, 0.0138073], [3, 0.0333333, -0.0138073]], [0.131882, [3, -0.0333333, 0], [3, 0.166667, 0]], [0.578728, [3, -0.166667, 0], [3, 0.133333, 0]], [0.573758, [3, -0.133333, 0], [3, 0.0333333, 0]], [0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.412688, [3, -0.0333333, 0.0700526], [3, 0.0333333, -0.0700526]], [0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.763974, [3, -0.0333333, 0.0646531], [3, 0.0333333, -0.0646531]], [0.573758, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.615176, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.412688, [3, -0.0333333, 0.0700526], [3, 0.0333333, -0.0700526]], [0.194861, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.961676, [3, -0.0333333, 0], [3, 0.0333333, 0]], [0.763974, [3, -0.0333333, 0.088914], [3, 0.166667, -0.44457]], [-0.638775, [3, -0.166667, 0], [3, 0.466667, 0]], [0.000398923, [3, -0.466667, 0], [3, 0, 0]]])


    return names, times, keys



def dance( ):
    global tts , motionProxy
    names, times, keys = give_pos()
    
    motionProxy.angleInterpolationBezier(names, times, keys)
    #tts.say("That was fun!")

def say(text):
    tts.setVoice("naoenu")
    tts.say(text)

def play_song():#playProxy.post.playFile("song.mp3")
    
    global playProxy
    
    playProxy.playFile("/home/nao/nao_dance_or.mp3")

def led_eye():
    
    clr = [0,0,0]
    clr[0] = np.random.randint(255)
    clr[1] = np.random.randint(255)
    clr[2] = np.random.randint(255)
    EyeLED(clr)

    
    
if __name__ == "__main__":
    print("main function")
    
    

