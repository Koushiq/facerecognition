import cv2
import numpy as np
import time
import multiprocessing
import email_with_files as mail
from datetime import datetime
from datetime import timedelta  

def triggerCam():
    cap =cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    startRec=False
    f1Snapped,f2Snapped=False,False
    endTime=""
    out = cv2.VideoWriter('recs/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    while True:
        ret , frame = cap.read()
        cv2.imshow('Preview Window',frame)
        
        now = datetime.now()
       
        
        ret1, frame1 = cap.read()
        
        ret2, frame2 = cap.read()
        diff = cv2.subtract(frame1,frame2)
        #line added for debugging purpose 
        cv2.imshow('diff',diff)
        if  not startRec:
            
            
            
            print("showing pixel diff while not recording")
            b,g,r = cv2.split(diff)
            
            print(cv2.countNonZero(b))
            print(cv2.countNonZero(g))
            print(cv2.countNonZero(r))
            
            if cv2.countNonZero(b)>240000 or cv2.countNonZero(g)>240000 or cv2.countNonZero(r)>240000:
                startRec= True
                endTime=datetime.now() + timedelta(seconds=7)
            #set Rec Flag to True
            
            
            #f1Snapped,f2Snapped=False,False
            #startRec=True
        
        if startRec==True:
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
                p=multiprocessing.Process(target=mail.mail,args=('recs',"Possible Suspicisios Activity") )
                p.start()
                
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()





