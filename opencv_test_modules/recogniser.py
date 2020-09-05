import face_recognition
import cv2
import numpy as np
import get_files as files
import time

def triggerFaceDetection():
    video_capture = cv2.VideoCapture(0)
    knownFaceEncodings=[]
    knownFaceNames=[]

    cameraFaceLocations=[]
    cameraFaceEncodings=[]
    faceNames=[]

    processFrame = True

    images = files.get_dir_files('imgs')

    print (images)

    knownFaceNames=files.get_file_name_all('imgs')
    print (knownFaceNames)


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
            
            
        cv2.imshow('Video',frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
triggerFaceDetection()


    

    
