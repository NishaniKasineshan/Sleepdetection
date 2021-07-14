import numpy as np
import cv2
import pygame
pygame.init()
pygame.mixer.init()

cap=cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

count=0
alarm=pygame.mixer.Sound('alarm.mp3')
while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,5,1,1)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    if (len(faces)>0):
        for (x,y,w,h) in faces:
            frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            roi_gray=gray[y:y+h,x:x+w]
            roi_color=frame[y:y+h,x:x+w]
            eyes=eye_cascade.detectMultiScale(roi_gray,1.3,5)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),5)
            if(len(eyes)>=2):
                cv2.putText(frame, "Eyes open!", (100,70), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),2)
                alarm.stop()
            else:
                print("Blink detected--------------")
                count=count+1
                if(count==10):
                    cv2.putText(frame, "Wake up you idiot!", (100,70), cv2.FONT_HERSHEY_PLAIN, 2,(0,0,255),2)
                    alarm.play()
                cv2.waitKey(1000)
                
    else:
        cv2.putText(frame,"No face detected",(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255),2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
