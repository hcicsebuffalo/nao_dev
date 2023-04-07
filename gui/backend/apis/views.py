from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from apis.feed import responser
import cv2

def video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        print(frame_bytes)

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame_bytes+b'\r\n')

# Create your views here.
def getfeed(request):
    # return HttpResponse("View Feed") 
    url = "http://192.168.43.226:8080/video"
    response = StreamingHttpResponse(video_feed(), content_type='multipart/x-mixed-replace; boundary=frame')
    
    resp = HttpResponse("hi")
    return response
    # return StreamingHttpResponse(responser(0, url),  )

def video_view(request):
    return render(request, 'video.html')