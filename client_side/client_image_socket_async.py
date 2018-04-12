import io
import _thread
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


def send_image(camera, conn, strm):
    try:
        print('== in SEND ==')
        #conn.write(struct.pack('<L', 0))
        
        #counter = 0
        for foo in camera.capture_continuous(strm, 'jpeg'): #rgb
            #window.update_idletasks()
            #window.update()
            print('strm tell = ' + str(strm.tell()))
	            
            #t1_network = datetime.datetime.now()
            conn.write(struct.pack('<L', strm.tell()))
            conn.flush()
            # Rewind the stream and send the image data over the wire
            strm.seek(0)
            conn.write(strm.read())
            #strm.truncate()
            #strm.seek(0)
            conn.flush()
    except:
        print('prblem')
        pass
        
        
def recv_image(conn, strm, window, imageFrame, lmain):
    print('== in RECV ==')
    time.sleep(2.1)
    while(True):
        try:
        
            #strm.seek(0)
            #strm.truncate()
            image_len = struct.unpack('<L', conn.read(struct.calcsize('<L')))[0]
            #conn.flush()
            strm.seek(0)
            print("Image",image_len)
            strm.write(conn.read(image_len))
            print("strm.tell():",strm.tell())
            strm.seek(0)
            image = Image.open(strm)
            imgtk = ImageTk.PhotoImage(image=image)
            lmain.imgtk = imgtk
            lmain.config(image=imgtk)
            lmain.img = imgtk

            print("stream size: ",sys.getsizeof(strm))


            print('Image is %dx%d' % image.size)
            #t2_network = datetime.datetime.now()
            #tdif_network = t2_network - t1_network
            #print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')



            # Reset the stream for the next capture
            strm.seek(0)
            strm.truncate()
        except:
            print('in RECV - except')


    
## ==================== BEGIN =================

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('199.60.17.11', 23000))

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

# Make a file-like object out of the connection
connection = client_socket.makefile('rwb')


stream = io.BytesIO()


print("Hello")


#_thread.start_new_thread(recv_image,(connection, stream, window, imageFrame, lmain, ))

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
            
    time.sleep(2)
    #start = time.time()
    print('== cam started ==')
    for foo in camera.capture_continuous(stream, 'jpeg'): #rgb
        try:
            window.update()
            #print('strm tell = ' + str(stream.tell()))
	          
            #t1_network = datetime.datetime.now()
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            #time.sleep(.5)
            connection.write(stream.read())
            #strm.truncate()
            #strm.seek(0)
            connection.flush()
        except:
            print('- in SEND except -')
            exit()

#_thread.start_new_thread(send_image, (connection, stream, ))

#connection.write(struct.pack('<L', 0))
connection.close()
client_socket.close()


