import numpy as np
import imutils
import math
import time
import sys
import cv2
import os

from flask import Flask, render_template, Response
# from camera import VideoCamera

app = Flask(__name__)


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 1920)  # float `width`
        self.video.set(4, 1080)  # float `height`
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('Class_Det.mp4')
        # self.video = cv2.VideoCapture(args["input"])

    def __del__(self):
        # self.writer.release()
        # cap.release()
        # cv2.destroyAllWindows()
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        print(image.shape)
        # start = time.time()
        # ret,image=cap.read()
        image=cv2.resize(image,(640,360))
        # (H, W) = image.shape[:2]
        
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    c = 1
    start = time.time()
    while True:
        start_1 = time.time()
        if c % 20 == 0:
            end = time.time()
            FPS = 20/(end-start)
            print("FPS_avg : {:.6f} ".format(FPS))
            start = time.time()
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        end_1 = time.time()
        FPS = 1/(end_1-start_1)
        print("FPS : {:.6f} ".format(FPS))
        c +=1
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)