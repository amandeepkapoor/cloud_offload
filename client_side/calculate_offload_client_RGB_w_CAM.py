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


payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
mydata = json.JSONEncoder().encode(payload)

t1 = datetime.datetime.now()
for i in range(1):
	r = requests.post(serveradd, data=mydata)
	file = open('test', 'w')
	file.write(r.text.split('[ INFO:0]')[0])
	file.close()
	backData = json.loads(r.text.split('[ INFO:0]')[0])
	#print(r.text)
	backImage = backData['image']
	#coord = backData['coord']
t2 = datetime.datetime.now()
tdif = t2 - t1
print(str(tdif.microseconds/1e6) + ' seconds')


arrback = np.array(backImage, dtype=np.uint8).reshape(shape)

# show in matplotlib
#fig,ax = plt.subplots(1)
plt.imshow(arrback)
#rect = patches.Rectangle((coord[0],coord[1]),coord[2],coord[3],linewidth=1,edgecolor='r',facecolor='none')
#ax.add_patch(rect)
plt.show()


