import cv2
import numpy as np

cap = cv2.VideoCapture('/dev/video0')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:    
    # Display the resulting frame
        print(frame)
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# from flask import Flask, Response
# import cv2
# app = Flask(__name__)
# video = cv2.VideoCapture(0)
# @app.route('/')
# def index():
#     return "Default Message"
# def gen(video):
#     while True:
#         success, image = video.read()
#         ret, jpeg = cv2.imencode('.jpg', image)
#         frame = jpeg.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# @app.route('/video_feed')
# def video_feed():
#     global video
#     return Response(gen(video),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=2204, threaded=True)