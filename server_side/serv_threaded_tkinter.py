import io
from queue import Queue
import socket
import threading
import struct
from PIL import Image
import numpy as np
import cv2 as cv
import base64
from time import sleep

imageQ = Queue()
processedQ = Queue()


def recv_from_client(connection):
    print('=== in recv ===')
    count = 0
    global imageQ

    while True:
        count = count + 1
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print(image_len)
        if not image_len:
            break

    
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)


        img = Image.open(image_stream)
        imageQ.put(img)
        if count == 10:
            break


def face_detection():
    print('=== in detection ===')
    global imageQ
    global processedQ
    while True:
        while not imageQ.empty():
            print('imageQ qsize = ', imageQ.qsize())
            img = imageQ.get()
            arrback = np.array(img)
            ######OpenCV Starts Here
            gray = cv.cvtColor(arrback, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                print(x,y,x+w,y+h)
                cv.rectangle(arrback,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = arrback[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            ####OpenCV Ends####
            arrback = cv.cvtColor(arrback, cv.COLOR_BGR2RGB)
            ret, result = cv.imencode(".jpg",arrback)
            processedQ.put(result)





def send_to_client(connection):
    print('=== in send ===')
    image_stream = io.BytesIO()
    global processedQ
    while True:
        while not processedQ.empty():
            print('processedQ qsize = ', processedQ.qsize())
            result = processedQ.get()
            #result.show()
            image_stream.seek(0)
            image_stream.truncate()
            image_stream.write(result.tobytes())
            connection.write(struct.pack('<L', image_stream.tell()))
            connection.flush()
            image_stream.seek(0)
            connection.write(image_stream.read())
            #image_stream.truncate()



face_cascade = cv.CascadeClassifier('harclass/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('harclass/haarcascade_eye.xml')
  

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 23000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rwb')


t = threading.Thread(target=recv_from_client, args=(connection, ))
v = threading.Thread(target=face_detection, args=())
u = threading.Thread(target=send_to_client, args=(connection, ))
t.start()
v.start()
u.start()
t.join()
v.join()
u.join()

print('==========HERE==========')
#while not imageQ.empty():
#    print(imageQ.qsize())

#    img = imageQ.get()
#    sleep(3)
#    img.show()


    
