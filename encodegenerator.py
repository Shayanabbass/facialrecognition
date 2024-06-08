import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facialattendence-15f63-default-rtdb.firebaseio.com/",
    'storageBucket':"facialattendence-15f63.appspot.com"
})
folderPath='Images'
imgpath=os.listdir('Images')
print(imgpath)
paths=[]
StudentIds=[]
for i in imgpath:
    paths.append(cv2.imread(os.path.join('Images',i)))
    StudentIds.append(os.path.splitext(i)[0])
    imagenameupload=f'{folderPath}/{i}'
    bucket=storage.bucket()
    blob=bucket.blob(imagenameupload)
    blob.upload_from_filename(imagenameupload)

# print (len(paths))    
# print(StudentIds)
print("encoding started")
def encodingsImages(imglist):
    encode=[]
    for img in imglist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # print(img)
        encodings=face_recognition.face_encodings(img)[0]
        encode.append(encodings)
    return encode 

en=encodingsImages(paths)  
print("encoding finished successfully") 
encodingwithids=[en,StudentIds]
file=open("imageencodings.p","wb")
pickle.dump(encodingwithids,file)
file.close
print("file saved")

# print(en)