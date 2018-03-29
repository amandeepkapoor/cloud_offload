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

conversion_type = 'L'   # 'RGB' or 'L'
plt.ion()

#location = 'localhost'
location = '199.60.17.11'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
#serveradd = 'http://' + location + '/cgi-bin/Facedetection2.py'
serveradd = 'http://' + location + '/cgi-bin/Facedetection_Test_Network_Time.py'

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
	t1_convert_s1 = datetime.datetime.now()
	image = frame.array
	shape = image.shape
	imageList = image.flatten().tolist()
	
	
 	

	payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
	mydata = json.JSONEncoder().encode(payload)
	
	t2_convert_s1 = datetime.datetime.now()
	tdif_convert_s1 = t2_convert_s1 - t1_convert_s1
	print('Stage1 conversion time =' + str(tdif_convert_s1.seconds + tdif_convert_s1.microseconds/1e6) + ' seconds')



	t1_network = datetime.datetime.now()
	r = requests.post(serveradd, data=mydata)
	t2_network = datetime.datetime.now()
	tdif_network = t2_network - t1_network
	print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')
		
	# writing to file for testing
	#file = open('test.txt', 'w')
	#file.write(r.text)
	#file.close()
	# ----------
	
	t1_convert_s2 = datetime.datetime.now()	
	backData = json.loads(r.text.split('[ INFO:0]')[0])
	backImage = backData['image']


	arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
	
	#plt.imshow(arrback)

	#plt.show()
	#plt.pause(.01)
	
	t2_convert_s2 = datetime.datetime.now()	
	tdif_convert_s2 = t2_convert_s2 - t1_convert_s2
	print('Stage2 conversion time =' + str(tdif_convert_s2.seconds + tdif_convert_s2.microseconds/1e6) + ' seconds')
	
	
	rawCapture.truncate(0)
	tdif_loop = t2_convert_s2 - t1_convert_s1
	print('LOOP TIME =' + str(tdif_loop.seconds + tdif_loop.microseconds/1e6) + ' seconds')
	print('--------------')
	
