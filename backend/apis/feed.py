import cv2
from PIL import Image
from importlib import reload


class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def release(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        _ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame_video(self):
        ret, frame = self.video.read()
        while True:
            if ret:
                jpeg = cv2.imencode('.jpg', frame)
                return frame, jpeg.tobytes()


def responser(boolean, slug):
    i=0
    j=0
    urlist=[slug]
    while True:
        camera = (Video(urlist[j]))
        if i % 1 == 0:
            frame, jpeg_bytes = camera.get_frame_video()
            print(frame)


