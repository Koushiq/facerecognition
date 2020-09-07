import cv2
import numpy as np
import time
import multiprocessing 
from datetime import datetime
from datetime import timedelta  


cap =cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

def triggerCam():
    global cap
    global frame_width
    global frame_height
    startRec=False
    f1Snapped,f2Snapped=False,False
    endTime=""
    out = cv2.VideoWriter('recs/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    while True:
        ret , frame = cap.read()
        cv2.imshow('Preview Window',frame)
        
        now = datetime.now()
        current_time = now.strftime("%S")
        if int(current_time)%10 ==5 and not startRec:
            cv2.imwrite('FrameOne.jpg',frame)
            f1Snapped=True
            
        if int(current_time)%10 ==4 and not startRec:
            cv2.imwrite('FrameTwo.jpg',frame)
            f2Snapped=True
        
        
        if f1Snapped and f2Snapped and not startRec:
            print("Comparing Frames!")
            frame1= cv2.imread('FrameOne.jpg')
            frame2= cv2.imread('FrameTwo.jpg')
            
            diff = cv2.subtract(frame1,frame2)
            #line added for debugging purpose 
            cv2.imshow('diff',diff)
            
            b,g,r = cv2.split(diff)
            
            print(cv2.countNonZero(b))
            print(cv2.countNonZero(g))
            print(cv2.countNonZero(r))
            
            #set Rec Flag to True
            
            endTime=datetime.now() + timedelta(seconds=4)
            f1Snapped,f2Snapped=False,False
            #startRec=True
        
        if startRec==True:
        # rec for 10 seconds
            print("Current time ")
            print(datetime.now())
            print("Target time ")
            print(endTime)
            if datetime.now()<=endTime:
                ret3,recFrame = cap.read()
                out.write(recFrame)
            else:
                startRec=False
                out.release()
                print("Video Wrote!")
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

p1 = multiprocessing.Process(target=triggerCam)
p1.start()





