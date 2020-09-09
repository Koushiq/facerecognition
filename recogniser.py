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
    video_capture = cv2.VideoCapture(0)
    knownFaceEncodings=[]
    knownFaceNames=[]

    cameraFaceLocations=[]
    cameraFaceEncodings=[]
    faceNames=[]

    processFrame = True
    sendMail = True
    
    endTimeKnownface=0
    endTimeUnknownface=0
    images = files.get_dir_files('imgs')

    print (images)

    knownFaceNames=files.get_file_name_all('imgs')
    print (knownFaceNames)

    snapTaken=False
    for path in images:
        knownImage = face_recognition.load_image_file("imgs/"+path)
        knownFaceEncodings.append(face_recognition.face_encodings(knownImage)[0])


    while True:
        ret, frame = video_capture.read()

        smallFrame =cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgbSmallFrame= smallFrame[:, :, ::-1]

        if processFrame:
            cameraFaceLocations = face_recognition.face_locations(rgbSmallFrame)
            cameraFaceEncodings = face_recognition.face_encodings(rgbSmallFrame,cameraFaceLocations)
            faceNames=[]

            for cameraFaceEncoding in cameraFaceEncodings:
                #make this multiprocess
                matches = face_recognition.compare_faces(knownFaceEncodings,cameraFaceEncoding)            
                name="Unrecognized"
                
                faceDistances = face_recognition.face_distance(knownFaceEncodings,cameraFaceEncoding)
                bestMatchIndex= np.argmin(faceDistances)

                if matches[bestMatchIndex]:
                    name=knownFaceNames[bestMatchIndex]

                faceNames.append(name)

        processFrame=not processFrame


        for(top,right,bottom,left), name in zip(cameraFaceLocations,faceNames):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)


            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            print("name is :" + name)
            snapTaken=True
            
            print("current time")
            print(datetime.now())
            
            print("target time")
            print(endTimeKnownface)
            # send next mail 30 seconds after sending the first mail
            if endTimeKnownface != 0 and datetime.now()>endTimeKnownface:
                sendMail=True
                endTimeKnownface=0
            
            #checing both flags to save snap and send mail
            print("snaptaken")
            print(snapTaken)
            print("sendMail")
            print(sendMail)
            if snapTaken==True and sendMail==True:
                cv2.imwrite('snaps/snap.jpg',frame)
                if name is not "Unrecognized":
                    p = multiprocessing.Process(target=mail.mail, args=('snaps',name+"is at your door !"))
                    p.start()
                    #mail.mail('snaps',name+"is at your door!")
                    endTimeKnownface=datetime.now() + timedelta(seconds=30)
                    #print(endTimeKnownface)
                else:
                    p = multiprocessing.Process(target=mail.mail, args=('snaps',"An Possible Unknown Person is at your door "))
                    p.start()
                    #mail.mail('snaps',name+"is at your door!")
                    endTimeKnownface=datetime.now() + timedelta(seconds=15)
                    #print(endTimeKnownface)
                sendMail=False
                snapTaken=False    
                    
        cv2.imshow('Video',frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
triggerFaceDetection()


    

    
