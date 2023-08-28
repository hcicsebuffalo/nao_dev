from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, StreamingHttpResponse
# from apis.feed import responser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import cv2
import pika
import base64
import numpy as np
import threading
import socket
import pickle
import os
import yaml
# from . import emotion

# Emotion code

# emotion.emotion_init()


# Load config parameters
current_path = os.getcwd()
yml_path = current_path[:-7] + "config.yml"

with open(yml_path, 'r') as ymlfile:
    #param = yaml.load(ymlfile)
    try:
        param = yaml.safe_load(ymlfile)
        print(param)
    except yaml.YAMLError as e:
        print(e)

def callback(ch, method, properties, body):
    global img_recv, img_buff
    #image_bytes = base64.b64decode(body)
    
    # Process the image as needed
    # ...
    #print(len(body))
    img_buff = body
    
    buffer = np.frombuffer(body, dtype=np.uint8)
    #buffer = base64.b64decode(body)
    img_recv = np.reshape(cv2.imdecode(buffer, cv2.IMREAD_COLOR), (960, 1280, 3) )  
    #print("------callback--------")
    #print(len(image_np))



# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
rabbit_channel = connection.channel()
rabbit_channel.queue_declare(queue='image_queue')
rabbit_channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)

img_recv = None
img_buff = None

def get_img():
    global rabbit_channel
    # Consume messages from the image queue
    #rabbit_channel.basic_qos(prefetch_count=1)
    
    # Start consuming messages
    rabbit_channel.start_consuming()

    # Close the connection to PC1
    #connection.close()

img_recv_thread = threading.Thread( target = get_img )
img_recv_thread.start()

def video_feed():
    print("*****************")
    global img_recv , img_buff
    # cap = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
        
    #     ret, img_recv = cv2.imencode('.jpg', frame)
    while True: 
        frame = cv2.imencode('.jpg', img_recv)
        #frame = cv2.imencode('.jpg', out)

        #cv2.imshow(out)
        if frame != None:
            # try: 
            #     out = emotion.faceDetection(img_recv)
            # except:
            #     out = img_recv
            out = img_recv
            retval, out_buffer = cv2.imencode('.jpg', out)
            #image_str = base64.b64encode(buffer)#.decode('utf-8')
            img_buf_out = out_buffer.tobytes()
            
            
            #print(len(img_recv), len(img_recv[0]))
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'+ img_buf_out +b'\r\n')
        else:
            pass
            #print(" None img")
        # return jpeg.tobytes()
        # print(frame_bytes)

        
        # return frame_bytes

# Create your views here.
def getfeed(request):
    # return HttpResponse("View Feed") 
    url = "http://192.168.43.226:8080/video"
    response = StreamingHttpResponse(video_feed(), content_type='multipart/x-mixed-replace; boundary=frame')
    
    resp = HttpResponse("hi")
    return response
    # return StreamingHttpResponse(responser(0, url),  )
conn = None
def establish_connection():
    global conn
    PORT = param["gui_port"]
    gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gui_socket.bind(("127.0.0.1", PORT))
    gui_socket.listen()
    print(" Establishing connection with python2")
    conn, addr = gui_socket.accept()
    print('Connection Established ......')

establish_connection()

@csrf_exempt
def action(request):
    global conn
    if request.method == 'POST':
        received_string = request.body
        decoded_data = json.loads(received_string.decode('utf-8'))
        body = decoded_data['body']
        conn.sendall(pickle.dumps([body] , protocol = 2))
        print("ACTION -> ", body)
        
    response_data = {'message': body+' completed successfully.'}
    return JsonResponse(response_data)  

def getimg(request):
    pass

def getlog(request):
    pass

def getchat(request):
    pass