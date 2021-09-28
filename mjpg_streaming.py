from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
from PIL import Image as im
import imutils
import time
import cv2
import sys

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self.send_response(20)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:

                    if(frame is not None):
                        pass
                    r, buf = cv2.imencode(".jpg", frame)
                    self.wfile.write("--jpgboundary\r\n".encode())
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                except KeyboardInterrupt:
                    break
            return

        if self.path.endswith('.html') or self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://localhost:9090/stream.mjpg" height="240px" width="320px"/>')
            self.wfile.write('</body></html>')
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 1920)
        self.stream.set(4, 1080)
        # self.stream.set(15,-100)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def realmain():
    global frame

    # ip = 'localhost'
    ip = '192.168.10.81'

    try:
        cap = WebcamVideoStream().start()
        server = ThreadedHTTPServer((ip, 9090), CamHandler)
        print("starting server")
        target = Thread(target=server.serve_forever,args=())

        i = 0
        while True:
            start = time.time()
            img = cap.read()
            img1 = imutils.resize(img, width=640,height=480)
            frame = img
            print("frame",i)
            cv2.imshow("image",img)
            cv2.waitKey(1)
            if(i == 0):
                target.start()
            i +=1
            # time.sleep(1)
            end = time.time()
            FPS = 1/(end-start)
            print("FPS : {:.6f} ".format(FPS))

    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    realmain()