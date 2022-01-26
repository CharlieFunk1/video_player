from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler #Python’s built-in library
import time
import cv2
from cut_video import cut_video, cut_whole_video
from queue import Queue
from threading import Thread

hostName = "127.0.0.1"
serverPort = 8080 #You can choose any available port; by default, it is 8000
current_frame = None

def gen_frames():
    while True:
        success, frame = cap.read()  # read the camera frame
        #print(frame)
        if not success:
            raise Exception("Failed to read frame")
        else:
            time.sleep(.033)
            global current_frame
            current_frame = frame

#def gen_frames(desired_square, capture):  
#     while True:
#         success, frame = capture.read()  # read the camera frame
#         #print(frame)
#         if not success:
#             continue
#         else:
#             new_frame = cut_video(frame, 4, desired_square)
#             ret, buffer = cv2.imencode('.jpg', new_frame)
#             frame = buffer.tobytes()
#             yield (frame)  # concat frame one by one and show result


class MyServer(BaseHTTPRequestHandler):  
    def do_GET(self): #the do_GET method is inherited from BaseHTTPRequestHandler
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=new_frame")
            self.end_headers()
            #genny = gen_frames((0,0))
            while True:
                frame2 = cut_video(current_frame, 4, (0,0))
                ret, buffer = cv2.imencode('.jpg', frame2)
                new_frame = buffer.tobytes()
                time.sleep(.033)
                self.wfile.write(bytes("--new_frame\n", "utf8"))
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-length', len(new_frame))
                self.end_headers()
                self.wfile.write(new_frame)
                
        elif self.path == "/1":
            self.send_response(200)
            self.send_header("content-type", "multipart/x-mixed-replace; boundary=new_frame")
            self.end_headers()
            #genny = gen_frames((0,1))
            while True:
                frame2 = cut_video(current_frame, 4, (1,0))
                ret, buffer = cv2.imencode('.jpg', frame2)
                new_frame = buffer.tobytes()
                time.sleep(.033)
                self.wfile.write(bytes("--new_frame\n", "utf8"))
                self.send_header('content-type', 'image/jpeg')
                self.send_header('content-length', len(new_frame))
                self.end_headers()
                self.wfile.write(new_frame)

        elif self.path == "/2":
            self.send_response(200)
            self.send_header("content-type", "multipart/x-mixed-replace; boundary=new_frame")
            self.end_headers()
            #genny = gen_frames((0,1))
            while True:
                frame2 = cut_video(current_frame, 4, (0,1))
                ret, buffer = cv2.imencode('.jpg', frame2)
                new_frame = buffer.tobytes()
                time.sleep(.033)
                self.wfile.write(bytes("--new_frame\n", "utf8"))
                self.send_header('content-type', 'image/jpeg')
                self.send_header('content-length', len(new_frame))
                self.end_headers()
                self.wfile.write(new_frame)
                
        elif self.path == "/3":
            self.send_response(200)
            self.send_header("content-type", "multipart/x-mixed-replace; boundary=new_frame")
            self.end_headers()
            #genny = gen_frames((0,1))
            while True:
                frame2 = cut_video(current_frame, 4, (1,1))
                ret, buffer = cv2.imencode('.jpg', frame2)
                new_frame = buffer.tobytes()
                time.sleep(.033)
                self.wfile.write(bytes("--new_frame\n", "utf8"))
                self.send_header('content-type', 'image/jpeg')
                self.send_header('content-length', len(new_frame))
                self.end_headers()
                self.wfile.write(new_frame)
#Assign video to cap
cap = cv2.VideoCapture('video/flow720p.mp4')

#Number of square slices you want.  Square root must be integer.
number_of_squares = 9

#cut_video will display a portion of the video broken up in squares.  The square root of number_of_squares must be an integer such that the squares
#form a larger square as shown in the illistration.  Desired square is a tuple with the coordinates of the square we want to return.
#The following example demonstrates number_of_squares equal to 9 and shows the corrdinates of desired_square for all elements.
#|---|---|---|
#|0,0|0,1|0,2|
#|---|---|---|
#|1,0|1,1|1,2|
#|---|---|---|
#|2,0|2,1|2,2|
#|---|---|---|
desired_square = (1,1)

#Check for error in opening file
if (cap.isOpened()== False): 
    print("Error opening video  file")



if __name__ == "__main__":
    t1 = Thread(target = gen_frames, args = ())
    t1.start()
    time.sleep(1)
    print(current_frame)
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
    print("Server stopped.")

