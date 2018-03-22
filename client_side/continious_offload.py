# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#import cv2
import picamera
import datetime
import json
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import picamera

plt.ion()

conversion_type = 'RGB'   # 'RGB' or 'L'


#location = 'localhost'
location = '199.60.17.30'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
serveradd = 'http://' + location + '/cgi-bin/Facedetection2.py'


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	shape = image.shape
	imageList = image.flatten().tolist()
	
 	

	payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
	mydata = json.JSONEncoder().encode(payload)



	for i in range(1):
		r = requests.post(serveradd, data=mydata)
		backData = json.loads(r.text.split('[ INFO:0]')[0])
		#print(r.text)
		backImage = backData['image']


	arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
	
	plt.imshow(arrback)

	plt.show()
	plt.pause(.2)

	
	# show the frame
	#cv2.imshow("Frame", image)
	
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	
