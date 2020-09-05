import cv2
import time
import multiprocessing 

def captureFirstFrame():
    time.sleep(5)
    cap = cv2.VideoCapture(0)
    ret2, frame1 = cap.read()
    cv2.imwrite('firstframe.jpg',frame1)
    cap.release()
    cv2.destroyAllWindows()
    
    
def captureSecondFrame():
    time.sleep(8)
    cap = cv2.VideoCapture(0)
    ret2, frame2 = cap.read()
    cv2.imwrite('secondframe.jpg',frame2)
    cap.release()
    cv2.destroyAllWindows()

def triggerCam():
    video_capture =cv2.VideoCapture(0)
    file = open("flag.txt","r+")
    file.truncate(0)
    file.close()
    
    while True:
        ret , frame = video_capture.read()
        cv2.imshow('Preview Window',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            file= open('flag.txt','w')
            file.write('True')
            break
        
    video_capture.release()
    cv2.destroyAllWindows()
    

p1 = multiprocessing.Process(target=triggerCam)
p1.start()


p2= multiprocessing.Process(target=captureFirstFrame)
p2.start()

p3= multiprocessing.Process(target=captureSecondFrame)
p3.start()



