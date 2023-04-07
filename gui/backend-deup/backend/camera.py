import cv2
from PIL import Image
from importlib import reload 
import json
import time



# celery = Celery('tasks', broker='amqp://guest@localhost//') #!

# TODO:
# Add dynamic video source selection 
class Video(object):
	def __init__(self,urls=None):
		self.urls=urls
		self.video = cv2.VideoCapture(0)
	def __del__(self):
		self.video.release()
		# Release the video camera 

	def get_frame(self):
		_, frame = self.video.read()
		################################################################
		_ret, jpeg = cv2.imencode('.jpg', frame)
		
		return jpeg.tobytes()

	def get_frame_video(self,attandance=None):
		ret, frame = self.video.read()
		while True:
			if ret:
			################################################################
				_ret, jpeg = cv2.imencode('.jpg', frame)
				# print( type(frame), type(jpeg))
				
				return frame, jpeg.tobytes()

def unique(list1): 
	# intilize a null list 
	unique_list = [] 
	  
	# traverse for all elements 
	for x in list1: 
		# check if exists in unique_list or not 
		if x not in unique_list: 
			unique_list.append(x) 
	return unique_list

def gen(camera):
	while True:
		frame = camera.get_frame()
		
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @shared_task
def responser(boolean, slug):
	# reload(face_detection)
	urlist=[slug]
	#try:
	attandance=[]
	i = 0
	j = 0 
	while True:
		camera = (Video(urls=urlist[j]))
		print(urlist[j])
		if i % 1==0:
			frame, jpeg_bytes = camera.get_frame_video(attandance=attandance)
			print(frame)
			print(jpeg_bytes)
			# detected_frame, detected_user = face_detection.det_recog_engine(frame, recog = True)
			# # print(detected_user)
			# print(type(detected_frame))
			# print(detected_user)
			# r, jpeg = cv2.imencode('.jpg', detected_frame)
			# detected_jpeg =jpeg.tobytes()
			# # print(detected_jpeg)
			# if boolean == 0:
			# 	yield (b'--frame\r\n'
			# 		b'Content-Type: image/jpeg\r\n\r\n' + detected_jpeg + b'\r\n\r\n')
			# elif boolean == 1:
			# 	# print(type(detected_user))
			# 	# detected_user = {"user": detected_user}
			# 	# print(json.dumps(detected_user))
			# 	# yield(detected_user)		
			# 	# yield "<html><body style='background-color: #ecfffb'>\n"

			# 	# yield "<div style='background-color: #b4f1f1'>%s</div>\n" %detected_user
			# 	# yield " " * 1024  # Encourage browser to render incrementally
			# 	# time.sleep(5)

			# 		# yield "<img src='http://127.0.0.1:8000/responser/feed' style= 'align-right'>"
			# 	yield "</body style='background-color: blue></html>\n"
			# 	yield "<div style='box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2) width: 20%;background-color: blue';>"
			# 	yield  "<div style= 'padding: 2px 16px; width:20%'>"
			# 	yield   "<h4><b>%s</b></h4>" %detected_user
			# 	yield 	"</div>"
			# 	yield	"</div>" 
			# 	yield " " * 1024  # Encourage browser to render incrementally
			# 	time.sleep(2)
			# 	yield "</body></html>\n"			
			# else:
			# 	detected_user = {"user": detected_user}
			# 	print(json.dumps(detected_user))
			# 	return json.dumps(detected_user)
		j+=1	
		if j == len(urlist):
			j = 0 	
		i+=1