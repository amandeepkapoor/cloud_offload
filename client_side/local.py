# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import picamera
import datetime
import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import picamera

face_cascade = cv.CascadeClassifier('harclass/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('harclass/haarcascade_eye.xml')

plt.ion()

#conversion_type = 'RGB'   # 'RGB' or 'L'


#location = 'localhost'
#location = '199.60.17.30'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
#serveradd = 'http://' + location + '/cgi-bin/Facedetection2.py'


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1920, 1080))
 
# allow the camera to warmup
time.sleep(0.1)
 
#t2_loop = datetime.datetime.now()
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
	print('--------')
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	t1_loop = datetime.datetime.now()	# loop timing
	#tdif_loop_roll = t1_loop - t2_loop
	#print('loop time roll =' + str(tdif_loop_roll.microseconds/1e6) + ' seconds')
	arrback = frame.array
	#shape = image.shape
	#imageList = image.flatten().tolist()
	
 	

	#payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
	#mydata = json.JSONEncoder().encode(payload)



	t1 = datetime.datetime.now()
	gray = cv.cvtColor(arrback, cv.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
    		cv.rectangle(arrback,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = arrback[y:y+h, x:x+w]
    		eyes = eye_cascade.detectMultiScale(roi_gray)
    		for (ex,ey,ew,eh) in eyes:
        		cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	t2 = datetime.datetime.now()
	tdif = t2 - t1
	print('conversion time =' + str(tdif.seconds + tdif.microseconds/1e6) + ' seconds')
	
	plt.imshow(arrback)

	plt.show()
	plt.pause(.0001)


 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	t2_loop = datetime.datetime.now()	# loop timing
	tdif_loop = t2_loop - t1_loop
	print('loop time =' + str(tdif_loop.microseconds/1e6) + ' seconds')

 
	
