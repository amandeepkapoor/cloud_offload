
import datetime
import json
import requests
import numpy as np
from PIL import Image

#img = Image.open("picture.jpeg").convert('L')
#arr = np.array(img)
#img.show()
#shape = arr.shape
#imageList = arr.flatten().tolist()




#location = 'localhost'
location = '199.60.17.11'
#port = 80
#serveradd = 'http://' + location + ':' + str(port) + '/cgi-bin/calculate_offload.py'
serveradd = 'http://' + location + '/cgi-bin/Facedetection_Test_Network_Time.py'


payload = {'key1': [1]*640*480*3}
mydata = json.JSONEncoder().encode(payload)

for i in range(10):
	t1_network = datetime.datetime.now()
	r = requests.post(serveradd, data=mydata)
	t2_network = datetime.datetime.now()
	tdif_network = t2_network - t1_network
	print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')

#backData = json.loads(r.text)
#print(r.text)
#backImage = backData['image']
#timeNow = backData['key1']
#newList = backData['key4']
#print(r.text)
#t2 = datetime.datetime.now()
#tdif = t2 - t1
#print(str(tdif.microseconds/1e6) + ' seconds')

#print(timeNow)
#print(newList)
#arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
#imgback = Image.fromarray(arrback, 'L')
#imgback.show()

#print("\n headers :\n" + str(r.headers))
#print("\n server status:" + str(r.status_code))
