
import datetime
import json
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

conversion_type = 'RGB'   # 'RGB' or 'L'


# here we read it from raspberry
img = Image.open("picture.jpeg").convert(conversion_type)
arr = np.array(img)
#img.show()
shape = arr.shape
imageList = arr.flatten().tolist()


location = 'localhost'
#location = '199.60.17.30'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
serveradd = 'http://' + location + '/cgi-bin/calculate_offload_RGB.py'


payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
mydata = json.JSONEncoder().encode(payload)

t1 = datetime.datetime.now()
for i in range(1):
	r = requests.post(serveradd, data=mydata)
	backData = json.loads(r.text)
	#print(r.text)
	backImage = backData['image']
	coord = backData['coord']
t2 = datetime.datetime.now()
tdif = t2 - t1
print(str(tdif.microseconds/1e6) + ' seconds')


arrback = np.array(backImage, dtype=np.uint8).reshape(shape)

# show in matplotlib
fig,ax = plt.subplots(1)
ax.imshow(arrback)
rect = patches.Rectangle((coord[0],coord[1]),coord[2],coord[3],linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
plt.show()



#imgback = Image.fromarray(arrback, 'RGB')
#imgback.show()

#print("\n headers :\n" + str(r.headers))
#print("\n server status:" + str(r.status_code))
