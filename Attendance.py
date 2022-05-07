import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import matplotlib.pyplot as plt

path = 'C:/Users/ANUSKA RAY/Downloads/ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images) : 
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
  
encodeListKnown = findEncodings(images)
#print(len(encodeListKnown))
print("Encoding complete")

with open('C:/Users/ANUSKA RAY/Downloads/Attendance.csv', 'w+') as f:
    pass
  
def markAttendance(name) : 
    with open('C:/Users/ANUSKA RAY/Downloads/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name}, {dtString}')
            
cap = cv2.VideoCapture(0)

#c = 0 ;
while True:
    #c = c + 1
    success, img = cap.read()
    imgs = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #state the location of face detect
    facesCurFrame = face_recognition.face_locations(imgs)
    #encoding the webcam images
    encodesCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)
    
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]: 
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            #y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 20)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        
    cv2.imshow('Webcam', img)
    #cv2.waitKey(1)
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
    
cap.release()
cv2.destroyAllWindows() 
