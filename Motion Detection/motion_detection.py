"""
Created on Sat May  2 15:08:06 2020

@author: shashiben
"""

#Importing required directories
import cv2

capture=0
#Capture the live Video
cap=cv2.VideoCapture(0)

#Get first frame
ret,frame1=cap.read()

#Get second frame
ret,frame2=cap.read()

#Fourcc for video writer
fourcc=cv2.VideoWriter_fourcc(*'XVID')

#To save video when s is clicked
output=cv2.VideoWriter("cap.avi",fourcc,20,(640,480)) 

#Run window until camera closes
while(cap.isOpened()):
    
    #Check difference between frame
    diff=cv2.absdiff(frame1,frame2)
    
    #Convert it into gray
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    
    #Smoothing image using gaussian blur
    blur=cv2.GaussianBlur(gray, (5,5), 0)
    
    #convert to threshold
    _,thresh=cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    #Display threshold
    cv2.imshow("Thres", thresh)
    
    #Dilate the image to reduce noise
    dilated=cv2.dilate(thresh, None,iterations=3)
    
    #Find contours
    contours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        
        #Show rectangle
        (x,y,w,h)=cv2.boundingRect(c)
        
        #Dont show rectangle for smaller motion having area less than 700
        if cv2.contourArea(c)<700:
            continue
        
        #draw rectangle
        cv2.rectangle(frame1, (x,y),(x+w,y+h), (0,255,0),2)
    #cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    cv2.imshow("Frame",frame1)
    
    #Cange frame
    frame1=frame2
    ret,frame2=cap.read()
    
    #Check keyboard handling
    key=cv2.waitKey(1) &0xFF
    if key==27:
        break
    elif key==ord("s"):
        #To save video
        capture=1
    if (capture==1):
        #write frames in video
        output.write(frame1)
#Destroy all windows
cv2.destroyAllWindows()

#Release output
output.release()

#Release captures
cap.release()




