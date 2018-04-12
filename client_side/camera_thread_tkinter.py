import io
import socket
import struct
import datetime
import time
import picamera
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys
import tkinter as tk
import threading 

#Set up GUI
#window = tk.Tk()
#window.wm_title("Test")
#window.config(background="#FFFFFF")

#Graphics Window
#imageFrame = tk.Frame(window, width=640, height=480)
#imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Video Frame
#lmain = tk.Label(imageFrame)
#lmain.grid(row = 0, column=0)

# =============== CONNECTION ==============
client_socket = socket.socket()
client_socket.connect(('199.60.17.11', 23000))
connection = client_socket.makefile('rwb')


def camera_capture(connection):
    print('=== in send ===')
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        time.sleep(2)

        stream = io.BytesIO()

        for foo in camera.capture_continuous(stream, 'jpeg'): #rgb
            

            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            connection.flush()


            stream.seek(0)
            stream.truncate()
            #time.sleep(2)


def recv_from_server(connection):
    #Set up GUI
    window = tk.Tk()
    window.wm_title("Test")
    window.config(background="#FFFFFF")

#Graphics Window
    imageFrame = tk.Frame(window, width=640, height=480)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Video Frame
    lmain = tk.Label(imageFrame)
    lmain.grid(row = 0, column=0)
    #global window
    #global imgtk
    #global lmain
    print('=== in recv ===')
    while True:
        window.update()
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print(image_len)
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
	
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        img = Image.open(image_stream)
        #img.show()
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.config(image=imgtk)
        lmain.img = imgtk

        image_stream.seek(0)
        image_stream.truncate()


try:
    #window.mainloop()
    t = threading.Thread(target=camera_capture, args=(connection, ))
    u = threading.Thread(target=recv_from_server, args=(connection, ))
    t.start()
    u.start()
    t.join()
    u.join()
     
           
    # Write a length of zero to the stream to signal we're done
    #connection.write(struct.pack('<L', 0))
except:
    print('=== EXCEPT ===')
    pass


