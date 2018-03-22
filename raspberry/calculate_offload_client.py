
import datetime
import json
import requests
import numpy as np
from PIL import Image

img = Image.open("image/picture.jpg").convert('L')
arr = np.array(img)
img.show()
shape = arr.shape
imageList = arr.flatten().tolist()




#location = 'localhost'
location = '192.168.1.82'
port = 80
serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'



payload = {'key1': [[1, 2, 3], [2, 3, 4]], 'key2': 200, 'image': imageList, 'shape': shape}
mydata = json.JSONEncoder().encode(payload)


for i in range(10):
    t1 = datetime.datetime.now()
    r = requests.post(serveradd, data=mydata)
    backData = json.loads(r.text)
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
