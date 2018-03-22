#!/usr/bin/python3
import json
import cgitb
import sys
from datetime import datetime
import time
import numpy as np
from PIL import Image
cgitb.enable()
import cv2 as cv

face_cascade = cv.CascadeClassifier('/usr/local/lib/python3.5/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('/usr/local/lib/python3.5/dist-packages/cv2/data/haarcascade_eye.xml')

print("Content-type: application/json; charset=utf-8")
print("\n")
myjson = json.load(sys.stdin)
shape = myjson['shape']
conversion_type = myjson['type']
# process image
myImage = myjson['image']
arrback = np.array(myImage, dtype=np.uint8).reshape(shape)
img = cv.imread(arrback)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#imgback = Image.fromarray(arrback, conversion_type).rotate(180)
arr = np.array(img)
imageList = arr.flatten().tolist()
myjson['image'] = imageList
#myjson['coord'] = [50, 60, 200, 200]

print(json.dumps(myjson))




