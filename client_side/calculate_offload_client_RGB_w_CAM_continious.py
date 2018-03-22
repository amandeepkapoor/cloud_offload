import picamera
import datetime
import json
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import picamera

conversion_type = 'RGB'   # 'RGB' or 'L'


# taking picture
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 3
    output = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    shape = output.shape
    imageList = output.flatten().tolist()


#location = 'localhost'
location = '199.60.17.30'
#port = 80
#serveradd = 'http://' + location + ':' + '/cgi-bin/calculate_offload_RGB.py'
serveradd = 'http://' + location + '/cgi-bin/Facedetection2.py'





with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    output = np.empty((240, 320, 3), dtype=np.uint8)
    while True:
    	camera.capture(output, 'rgb')
    	print(output.shape)
    	imageList = output.flatten().tolist()
    	payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
    	mydata = json.JSONEncoder().encode(payload)
    	t1 = datetime.datetime.now()
    	r = requests.post(serveradd, data=mydata)
    	backData = json.loads(r.text.split('[ INFO:0]')[0])
    	backImage = backData['image']
    	t2 = datetime.datetime.now()
    	tdif = t2 - t1
    	print(str(tdif.microseconds/1e6) + ' seconds')
    	arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
    	plt.imshow(arrback)
    	plt.show()


