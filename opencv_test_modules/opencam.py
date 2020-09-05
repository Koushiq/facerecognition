import numpy as np
import cv2

def triggerCam():
    cap = cv2.VideoCapture(0)
    ret2, frame2 = cap.read()
    cv2.imshow('frame2',frame2)
    while(True):
        
        ret, frame = cap.read()
        
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


triggerCam()