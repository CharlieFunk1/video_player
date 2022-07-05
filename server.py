from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler #Python’s built-in library
import time
import cv2
from math import sqrt
from cut_video import cut_custom_video, cut_whole_video
from queue import Queue
from threading import Thread
from parse import *

#Hostname for access to video.  0.0.0.0 will allow access from other devices on network.
hostName = "0.0.0.0"

#You can choose any available port; by default, it is 8000.
serverPort = 8080 

#Global variable used to communicate from gen_frames thread to main thread.  Do not change.
current_frame = None

# If equal_size is True, will automatically generate equal sized slices in a grid.  custom_size_list can be ignored.
# If equal_size is False, will use custom_size_list to determine size and number of slices.  number_of_squares can be ignored.
#Are slices equal size?  If so, square root of number_of_squares must be an integer.
equal_size = False
#For custom sizes, define start and end positions in pixels.
#(start_x, start_y, width, height)
#start x,y --------------> Width x
#         ||-------------|
#         ||             |
#         ||             |
#         ||             |
#         V|-------------|
#       Height y
#equal_size = True use:
number_of_squares = 4
#equal_size = False use:
custom_size_list = [
(0, 0, 1280, 720),
(0, 100, 500, 300),
(500, 300, 600, 350),
]

#Video to be split
#video = 'video/bob.mp4'
video = 'video/flow720p.mp4'
#gen_frames is threadded and reads frames from the video and sends them to global variable current_frame.
#This is so only one element reads from cap at any time.
def gen_frames():
    while True:
        cap = cv2.VideoCapture(video)           
        #Check for error in opening file
        if (cap.isOpened()== False): 
            print("Error opening video  file")
        while True:
            success, frame = cap.read()  # read the camera frame
            if not success:
                cap.release()
                cap = cv2.VideoCapture(video)
            else:
                time.sleep(.033)
                global current_frame
                current_frame = frame

#Sets up a web server, creates the neccisary number of domains, and sends the video slices to each.  Domains are numbered 0-x.
class MyServer(BaseHTTPRequestHandler):
    def create_domain(self, i):
        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=new_frame")
        self.end_headers()
        while True:
            if equal_size == True:
                frame_list = cut_whole_video(current_frame, number_of_squares)
            else:
                frame_list = cut_custom_video(current_frame, custom_size_list)
            frame = frame_list[i]
            ret, buffer = cv2.imencode('.jpg', frame)
            new_frame = buffer.tobytes()
            time.sleep(.033)
            self.wfile.write(bytes("--new_frame\n", "utf8"))
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-length', len(new_frame))
            self.end_headers()
            self.wfile.write(new_frame)
            
    def do_GET(self):
        for i in range(number_of_squares):
            if self.path == "/" + str(i):
                self.create_domain(i)


if __name__ == "__main__":
    t1 = Thread(target = gen_frames, args = ())
    t1.start()
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
    print("Server stopped.")

