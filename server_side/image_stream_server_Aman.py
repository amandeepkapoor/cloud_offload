import io
import socket
import struct
from PIL import Image
import numpy as np
import cv2 as cv

face_cascade = cv.CascadeClassifier('/usr/local/lib/python3.5/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('/usr/local/lib/python3.5/dist-packages/cv2/data/haarcascade_eye.xml')
  

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 23000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rwb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
	
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        img = Image.open(image_stream)
        arrback = np.array(img)
        #image_stream.seek(0)
       # arrback = np.asarray(bytearray(image_stream.read()), dtype=np.uint8).reshape(640,480,3)

        ######OpenCV Starts Here
        print(arrback.shape)
        gray = cv.cvtColor(arrback, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(arrback,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = arrback[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        ####OpenCV Ends####
        print("End of OpenCV")
        image_stream.seek(0)	
        image_stream.write(arrback.tobytes())
       # file_bytes = arrback.tobytes()
       # f = io.BytesIO(file_bytes)
        
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
	
        connection.write(struct.pack('<L', image_stream.tell()))
        connection.flush()
        print('----')
        image_stream.seek(0)
        connection.write(image_stream.read())

finally:
    connection.close()
    server_socket.close()

