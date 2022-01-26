import cv2
from cut_video import cut_video, cut_whole_video

#Assign video to cap
cap = cv2.VideoCapture('video/newlong4.mov')

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

# Read until video is completed
while(cap.isOpened()):
      
  # Capture frame-by-frame
    ret, frame = cap.read()

    #Call one of the cut video functions to cut the video.  cut_video = one slice, cut_whole_video = list of all slices
    
    #new_frame = cut_video(frame, number_of_squares, desired_square)
    frame_list = cut_whole_video(frame, number_of_squares)

    
    if ret == True:

        #Display the new frame
        
        #cv2.imshow('frame', new_frame)

        #Display all frames!
        
        i = 0
        for frame in frame_list:
            cv2.imshow(str(i), frame)
            i += 1

        #Wait for q key to be pressed to break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
     
    # Break the loop
    else: 
        break
    
#Release cap
cap.release()
   
# Closes all the frames
cv2.destroyAllWindows()
