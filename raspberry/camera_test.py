import datetime
import json
import requests
import numpy as np
from PIL import Image
import time
import picamera
import matplotlib.pyplot as plt


#while True:
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 3
    #time.sleep(2)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    #camera.capture_continuous(output, 'rgb')
    camera.capture(output, 'rgb')
    plt.imshow(output)
    plt.show()
    #ImageCaptured = Image.fromarray(output,'RGB')
    #ImageCaptured.show()
    #camera.capture(output, 'rgb')
    #print(output.shape)
    #print(output)
    
    
