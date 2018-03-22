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
shape = myjson['shape']
conversion_type = myjson['type']
# process image
myImage = myjson['image']
arrback = np.array(myImage, dtype=np.uint8).reshape(shape)
imgback = Image.fromarray(arrback, conversion_type).rotate(180)
arr = np.array(imgback)
imageList = arr.flatten().tolist()
myjson['image'] = imageList
myjson['coord'] = [50, 60, 200, 200]

print(json.dumps(myjson))
