# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import picamera
import datetime
import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import picamera
import tkinter as tk
from PIL import Image, ImageTk
import io

face_cascade = cv.CascadeClassifier('harclass/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('harclass/haarcascade_eye.xml')


#conversion_type = 'RGB'   # 'RGB' or 'L'


resol = (1920, 1080)


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = resol
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=resol)


#Set up GUI
window = tk.Tk()
window.wm_title("Test")
window.config(background="#FFFFFF")

#Graphics Window
imageFrame = tk.Frame(window, width=resol[0], height=resol[1])
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Video Frame
lmain = tk.Label(imageFrame)
lmain.grid(row = 0, column=0)

stream = io.BytesIO()
 
# allow the camera to warmup
time.sleep(0.1)

list_loop = [0]*30
list_network = [0]*30
list_conv_1 = [0]*30
list_conv_2 = [0]*30
counter = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
	
	t1_loop = datetime.datetime.now()	# loop timing (overal)

	window.update()
	#print('--------')

	t1 = datetime.datetime.now()
	
	arrback = frame.array
	gray = cv.cvtColor(arrback, cv.COLOR_BGR2GRAY)
	#print(gray)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
    		cv.rectangle(arrback,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = arrback[y:y+h, x:x+w]
    		eyes = eye_cascade.detectMultiScale(roi_gray)
    		for (ex,ey,ew,eh) in eyes:
        		cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	t2 = datetime.datetime.now()
	tdif_network = t2 - t1
	
	
	arrback = cv.cvtColor(arrback,cv.COLOR_BGR2RGB)
	ret,result = cv.imencode(".jpg",arrback)
	#result.show()
	stream.write(result.tobytes())
	stream.seek(0)
	image = Image.open(stream)
	#print(type(image))

	imgtk = ImageTk.PhotoImage(image=image)
	lmain.imgtk = imgtk
	lmain.config(image=imgtk)
	lmain.img = imgtk

	stream.seek(0)
	stream.truncate()
	
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	
	if (counter == 30):
	  window.destroy()
	  break

	t2_loop = datetime.datetime.now()	# loop timing
	t_conv_1 = t1 - t1_loop
	t_conv_2 = t2_loop - t2
	tdif_loop = t2_loop - t1_loop
	list_loop[counter] = (tdif_loop.seconds + tdif_loop.microseconds/1e6)
	list_network[counter] = (tdif_network.seconds + tdif_network.microseconds/1e6)
	list_conv_1[counter] = (t_conv_1.seconds + t_conv_1.microseconds/1e6)
	list_conv_2[counter] = (t_conv_2.seconds + t_conv_2.microseconds/1e6)
	counter += 1
	#print('conv1 time =' + str(t_conv_1.seconds + t_conv_1.microseconds/1e6) + ' seconds')
	#print('Detection time =' + str(tdif.seconds + tdif.microseconds/1e6) + ' seconds')
	#print('conv2 time =' + str(t_conv_2.seconds + t_conv_2.microseconds/1e6) + ' seconds')
	#print('loop time =' + str(tdif_loop.seconds + tdif_loop.microseconds/1e6) + ' seconds')
	

print('max time (conv1, conv2, detection, loop) =', max(list_conv_1[3:]),max(list_conv_2[3:]),max(list_network[3:]),max(list_loop[3:]))
print('min time (conv1, conv2, detection, loop) =', min(list_conv_1),min(list_conv_2),min(list_network),min(list_loop))
print('avg time (conv1, conv2, detection, loop) =', sum(list_conv_1[3:])/len(list_conv_1[3:]),sum(list_conv_2[3:])/len(list_conv_2[3:]),sum(list_network[3:])/len(list_network[3:]),sum(list_loop[3:])/len(list_loop[3:]))
window.mainloop()

 
	
