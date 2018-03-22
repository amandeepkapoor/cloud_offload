#!/usr/bin/python3
import json
import cgitb
import sys
from datetime import datetime
import time
import numpy as np
from PIL import Image
cgitb.enable()
print("Content-type: application/json; charset=utf-8")
print("\n")


myjson = json.load(sys.stdin)
x = myjson['key1']
myjson['key1'] = str(datetime.now())
myjson['key2'] = myjson['key2']*(-30)
myjson['key3'] = 'NEW'
myjson['key4'] = x + 2*x
shape = myjson['shape']
# process image
myImage = myjson['image']
arrback = np.array(myImage, dtype=np.uint8).reshape(shape)
imgback = Image.fromarray(arrback, 'L').rotate(45)
arr = np.array(imgback)
imageList = arr.flatten().tolist()
myjson['image'] = imageList

print(json.dumps(myjson))
