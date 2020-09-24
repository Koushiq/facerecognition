# import libraries 
import cv2
import numpy as np
import time
import multiprocessing
import email_with_files as mail
from datetime import datetime
from datetime import timedelta  

def triggerCam():

    cap =cv2.VideoCapture(0) #open camera using opencv
    #get camera width and height
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4))

    startRec=False #init and set recording flag to false
    endTime="" #init end time of video 

    out = cv2.VideoWriter('recs/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height)) # init output file

    while True: # set loop for retriving camera feed 
        ret , frame = cap.read()  # read feed from camera 
        cv2.imshow('Preview Window',frame) # preview camera feed 
        
        now = datetime.now()  # get current time 
       
        #Take two snaps from camera
        ret1, frame1 = cap.read()  # first snap
        
        ret2, frame2 = cap.read() # second snap 
        diff = cv2.subtract(frame1,frame2) # calculate difference between two snaps 

        cv2.imshow('diff',diff) # display the difference between two frames 
        if  not startRec:
            
            print("showing pixel diff while not recording")
            b,g,r = cv2.split(diff) #split blue green red pixel count from substracted frame 
            
            print(cv2.countNonZero(b))  #print the nonzero pixel count
            print(cv2.countNonZero(g))
            print(cv2.countNonZero(r))

            # compare pixel count with tolarance level , if tolarance level is exceeded then camera will assume something is right and will init recording 

            if cv2.countNonZero(b)>240000 or cv2.countNonZero(g)>240000 or cv2.countNonZero(r)>240000: 
                startRec= True # set recording flag to true 
                endTime=datetime.now() + timedelta(seconds=7) # set recording duration
        
        if startRec==True: # if recording flag is true 
            print("Current time ")    # print current time and target/ endtime time (camera will record till the target time)
            print(datetime.now())
            print("Target time ")
            print(endTime)
            if datetime.now()<=endTime: # if current time is less than endtime/target time 
                ret3,recFrame = cap.read() #capture frame and then write it to the initialized recording file 
                out.write(recFrame) # the logic works as a video is also a stream of pictures
            else:
                startRec=False # if current time is grater than endtime/target time  set recording flag to false
                out.release()  # finish the recorded video 
                print("Video Wrote!")
                p=multiprocessing.Process(target=mail.mail,args=('recs',"Possible Suspicisios Activity") ) # create separate process to send the mail , if running on single process then the camera will freeze
                p.start() # start the process
                
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #press q to exit window 
            break
    cap.release() # release current camera feed 
    cv2.destroyAllWindows() #destroy all running open cv windows