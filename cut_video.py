from math import sqrt
import cv2

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

def cut_video(frame, number_of_squares, desired_square):
    sqrt_of_number_of_squares = sqrt(number_of_squares)
    
    h = len(frame)
    w = len(frame[1])

    h_index, w_index = desired_square
    
    new_frame = frame[round(h_index * (h/sqrt_of_number_of_squares)) :round((h_index + 1) * (h/sqrt_of_number_of_squares)), round(w_index * (w/sqrt_of_number_of_squares)) :round((w_index + 1) * (w/sqrt_of_number_of_squares))] 
    
    return new_frame

#cut_whole_video will take number_of_squares and generate a list, frame_list, of equal sized and distributed frames in a grid.
def cut_whole_video(frame, number_of_squares):
    sqrt_of_number_of_squares = sqrt(number_of_squares)

    h = len(frame)
    w = len(frame[1])

    frame_list = []
    
    for h_index in range(round(sqrt_of_number_of_squares)):
        for w_index in range(round(sqrt_of_number_of_squares)):
            new_frame = frame[round(h_index * (h/sqrt_of_number_of_squares)) :round((h_index + 1) * (h/sqrt_of_number_of_squares)), round(w_index * (w/sqrt_of_number_of_squares)) :round((w_index + 1) * (w/sqrt_of_number_of_squares))]
            frame_list.append(new_frame)

    return frame_list

#cut_custom_video will take a list of four element tuples, custom_size_list, and generate a list, frame_list, of custom sized frames. 
def cut_custom_video(frame, custom_size_list):
    frame_list = []
    
    for custom_size in custom_size_list:
        start_width, start_height, width, height = custom_size
        new_frame = frame[start_height:height, start_width:width]
        frame_list.append(new_frame)
        
    return frame_list
    
