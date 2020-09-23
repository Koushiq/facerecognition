# import libraries 
import face_recognition
import cv2
import numpy as np
import get_files as files
import time
import email_with_files as mail
from datetime import datetime
from datetime import timedelta
import multiprocessing



def triggerFaceDetection():
    video_capture = cv2.VideoCapture(0) #open camera using opencv
    # init array to load known face encoding , names and camera face location and encodings
    knownFaceEncodings=[]
    knownFaceNames=[]
    cameraFaceLocations=[]
    cameraFaceEncodings=[]
    faceNames=[]

    processFrame = True # set process frame flag to true 
    sendMail = True #declare and set send mail to True
    
    endTimeKnownface=0 
    endTimeUnknownface=0
    images = files.get_dir_files('img/known') # load known faces path

    print (images) # print to check if all paths are loaded correctly 

    knownFaceNames=files.get_file_name_all('img/known') #load known faces names from file name
    print (knownFaceNames)  # print to check all okay 

    snapTaken=False  # declare and set snapTaken flag to False

    for path in images: # loop through the loaded known faces to retrive face encoding
        knownImage = face_recognition.load_image_file("img/known/"+path) #loadimage from path
        knownFaceEncodings.append(face_recognition.face_encodings(knownImage)[0]) # retrive face encoding 


    while True: # set loop to retrive feed from camera 
        ret, frame = video_capture.read() # retrive feed from camera using opencv

        smallFrame =cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # resize frame for faster processing 

        rgbSmallFrame= smallFrame[:, :, ::-1] # process frame as rgb frame

        if processFrame: # if process frame is set to true
            cameraFaceLocations = face_recognition.face_locations(rgbSmallFrame) # retrive face locations matrix from camera 
            cameraFaceEncodings = face_recognition.face_encodings(rgbSmallFrame,cameraFaceLocations) # retrive face encodings from camera 
            faceNames=[]

            for cameraFaceEncoding in cameraFaceEncodings: # loop through face encoding retrived from camera 
                
                matches = face_recognition.compare_faces(knownFaceEncodings,cameraFaceEncoding)  #compare camera face encodings with known face encodings           
                name="Unrecognized" # set inital name to unrecognised 
                
                faceDistances = face_recognition.face_distance(knownFaceEncodings,cameraFaceEncoding) # calculate and return face distance of known face encoding and camera face encoding
                bestMatchIndex= np.argmin(faceDistances) # find best match index of faceDistances using numpy's argmin 

                if matches[bestMatchIndex]: # if matches index returns a positive value
                    name=knownFaceNames[bestMatchIndex] # set name from unrecognised to found faces name

                faceNames.append(name) # append the name to an array , necessary as multiple faces may appear infront of camera at once

        processFrame=not processFrame #not operation for process frame , if everyframe is processed and operated camera might freeze


        for(top,right,bottom,left), name in zip(cameraFaceLocations,faceNames): # loop through cameraFaceLocations and faceNames as a pair

            #set locations for drawing rectangle around face 
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # init rectangle around face 
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1) 

            # init rectangle below face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX #set font 
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)  # display name as text below face 
            
            print("name is :" + name) # print name in console 
            snapTaken=True # set snapTaken to True , as camera will not take snap for some time to send email 
            
            print("current time") # display current time 
            print(datetime.now()) 
            
            print("target time") # display target time ( time until camera cannot take any other snaps )
            print(endTimeKnownface)
           
            if endTimeKnownface != 0 and datetime.now()>endTimeKnownface: # init terminating condition , endTimeKnownface will be set if face is known or unknown, by default it is zero
                sendMail=True
                endTimeKnownface=0
            
            #print both flags to save snap and send mail
            print("snaptaken")
            print(snapTaken)
            print("sendMail")
            print(sendMail)
            if snapTaken==True and sendMail==True:# check if both flags are true , if yes save the image from camera and sent a mail of the image
                cv2.imwrite('img/snaps/snap.jpg',frame)
                if name is not "Unrecognized":
                    p = multiprocessing.Process(target=mail.mail, args=('img/snaps',name+"is at your door !")) #create separate process to send the mail , if running on single process then the camera will freeze
                    p.start()# start the process 

                    #known face is detected , set snap cool down time to 30 seconds
                    endTimeKnownface=datetime.now() + timedelta(seconds=30)
                    
                else:
                    p = multiprocessing.Process(target=mail.mail, args=('img/snaps',"An Possible Unknown Person is at your door "))
                    p.start()
                    
                    #unknown face is detected , set snap cool down time to 15 seconds
                    endTimeKnownface=datetime.now() + timedelta(seconds=15)

                    #set flags to false once mail is sent 
                sendMail=False 
                snapTaken=False     
                    
        cv2.imshow('Video',frame) # display feed from camera


        if cv2.waitKey(1) & 0xFF == ord('q'): #press q to exit 
            break

    video_capture.release() # release camera feed 
    cv2.destroyAllWindows() # destroy all windows
