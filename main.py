import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facialattendence-15f63-default-rtdb.firebaseio.com/",
    'storageBucket':"facialattendence-15f63.appspot.com"
})
# print(cv2.__version__)
bucket=storage.bucket()
cap=cv2.VideoCapture(0)
cap.set(2,640)
cap.set(3,480)
imgbackground=cv2.imread('Resources/background.png')
imgpath=os.listdir('Resources/Modes')
paths=[]
for i in imgpath:
    paths.append(cv2.imread(os.path.join('Resources/Modes',i)))
#import the encodings file
print("Loading Encoded file")
file=open("imageencodings.p","rb")
encodingwithids=pickle.load(file)
file.close()
print("Encoding file loaded")
# print(encodingwithids)
en,StudentIds=encodingwithids
print(StudentIds)
# print(imgpath)
counter=0
mode=0
student = -1
imgstudent = []

while True:
    success , img=cap.read()

    imgS=cv2.resize(img,(0,0),None,0.25,0.25, interpolation=cv2.INTER_LINEAR)

    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    facecurlocation=face_recognition.face_locations(imgS)
    # print("location",facecurlocation)
    facecurencodings=face_recognition.face_encodings(imgS,facecurlocation)
    imgbackground[162:162+480,55:55+640]=img   
    imgbackground[44:44+633,808:808+414]=paths[mode] 
    if facecurlocation:
        for encodeface,faceloc in zip(facecurencodings,facecurlocation):
            matches=face_recognition.compare_faces(en,encodeface)
            faceDis=face_recognition.face_distance(en,encodeface)
            matchindex=np.argmin(faceDis)
            # print("index",matchindex)
            # print("matches",matches)
            # print("distance",faceDis)
            if(matches[matchindex]):
                student=StudentIds[matchindex]
                print("face detected of ID",student)
                y1,x2,y2,x1=faceloc 
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox=55+x1,162+y1,x2-x1,y2-y1
                imgbackground=cvzone.cornerRect(imgbackground,bbox,rt=0)
                if counter == 0:
                    cvzone.putTextRect(imgbackground, "Loading", (275, 400))
                    # cv2.imshow("Face Attendance", imgbackground)
                    # cv2.waitKey(1)
                    counter = 1
                    mode = 1
        if counter!=0:
            if counter==1:
                #get data from database
                studentinfo=db.reference(f'Students/{student}').get()
                print(studentinfo)
                #get the image from storage
                blob=bucket.get_blob(f'Images/{student}.png')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                
                #update attendence
                datetimeobject=datetime.strptime(studentinfo['last_attendence_time'],
                                                "%Y-%m-%d %H:%M:%S")
                secondselapsed=(datetime.now()-datetimeobject).total_seconds()
                print(secondselapsed)
                if secondselapsed>30:
                        
                    ref=db.reference(f'Students/{student}')
                    studentinfo['No_of_Attendence'] = int(studentinfo['No_of_Attendence']) + 1
                    ref.child('No_of_Attendence').set(studentinfo["No_of_Attendence"])
                    ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    mode=3
                    counter=0
                    imgbackground[44:44+633,808:808+414]=paths[mode] 


            # print(studentinfo)
            if mode!=3:
                if 10<counter<20:
                    mode=2
                    # print(mode)
                imgbackground[44:44+633,808:808+414]=paths[mode] 

            # print(studentinfo)    

                if counter<=10:
                    # print(studentinfo)    
                    cv2.putText(imgbackground,str(studentinfo['No_of_Attendence']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)  
                    cv2.putText(imgbackground,str(studentinfo['Major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,50),1)    
                    cv2.putText(imgbackground,str(student),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,50),1)    
                    (w,h),_=cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv2.putText(imgbackground,str(studentinfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)    
                    imgbackground[175:175+216,909:909+216]=imgstudent
                # print(counter)
                counter+=1
                # print(counter)    
                if counter>=20:
                    mode=0
                    counter=0
                    studentinfo=[]
                    imgstudent=[]
                    imgbackground[44:44+633,808:808+414]=paths[mode]     



    else:
        mode=0
        counter=0
    cv2.imshow("webcam",imgbackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
