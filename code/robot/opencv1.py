import cv2
import numpy as np

cap = cv2.VideoCapture(0) #camera (webcam) no. 1 if 0 as parameter.if string representingpath of a file,
#loads this video as the source.

while True:
    return_bool, frame = cap.read()#return_bool = True if there's a feed from the webcam, otherwise False,
    #and frame is the frame coming from the webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converts frame to grayscale
    cv2.imshow('frame',gray)#shows the frame in a window ('frame' is the name of the frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break #quits the loop

cap.release() #"closes" the camera so that it's not considered as in use
cv2.destroyAllWindows()








##img = cv2.imread('watch.jpg',cv2.IMREAD_GRAYSCALE)
