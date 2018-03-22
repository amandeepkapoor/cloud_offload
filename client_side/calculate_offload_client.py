
import datetime
import json
import requests
import numpy as np
from PIL import Image

img = Image.open("picture.jpeg").convert('L')
arr = np.array(img)
img.show()
shape = arr.shape
imageList = arr.flatten().tolist()




#location = 'localhost'
location = '199.60.17.30'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
serveradd = 'http://' + location + '/cgi-bin/calculate_offload.py'


payload = {'key1': [[1, 2, 3], [2, 3, 4]], 'key2': 200, 'image': imageList, 'shape': shape}
mydata = json.JSONEncoder().encode(payload)

t1 = datetime.datetime.now()
for i in range(1):
	r = requests.post(serveradd, data=mydata)
	backData = json.loads(r.text)
	#print(r.text)
	backImage = backData['image']
	timeNow = backData['key1']
	newList = backData['key4']
	#print(r.text)
t2 = datetime.datetime.now()
tdif = t2 - t1
print(str(tdif.microseconds/1e6) + ' seconds')

print(timeNow)
print(newList)
arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
imgback = Image.fromarray(arrback, 'L')
imgback.show()

#print("\n headers :\n" + str(r.headers))
#print("\n server status:" + str(r.status_code))
