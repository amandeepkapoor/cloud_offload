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

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('199.60.17.11', 23000))
#plt.ion()
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

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        #camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        #counter = 0
        def show_frame():
	        #counter = 0
	        for foo in camera.capture_continuous(stream, 'jpeg'): #rgb
	            #window.update_idletasks()
	            window.update()
	            # Write the length of the capture to the stream and flush to
	            # ensure it actually gets sent
	            t1_network = datetime.datetime.now()
	            connection.write(struct.pack('<L', stream.tell()))
	            connection.flush()
	            # Rewind the stream and send the image data over the wire
	            stream.seek(0)
	
	            connection.write(stream.read())
	            #stream.truncate()
	            #stream.seek(0)
	            connection.flush()
	            
	            #stream.seek(0)
	            #stream.truncate()
	            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
	            #connection.flush()
	            stream.seek(0)
	            print("Image",image_len)
	            stream.write(connection.read(image_len))
	            print("stream.tell():",stream.tell())
	            stream.seek(0)
	            image = Image.open(stream)
	            imgtk = ImageTk.PhotoImage(image=image)
	            lmain.imgtk = imgtk
	            lmain.config(image=imgtk)
	            lmain.img = imgtk
	            #image_np = np.array(image)
	            #cv.rectangle(image_np,(239,185),(390,336),(255,0,0),2)
	            print("stream size: ",sys.getsizeof(stream))
	            #plt.imshow(image_np)
	            #plt.show()
	            #plt.pause(.0001)
	            #image = Image.frombytes('RGB', (640,480,3), (bytearray(stream)*(640*480*3)))
	            print('Image is %dx%d' % image.size)
	            t2_network = datetime.datetime.now()
	            tdif_network = t2_network - t1_network
	            print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')
	            
	            #image.show()
	            #counter += 1
	            #if (counter >10):
	                #break
	            # If we've been capturing for more than 30 seconds, quit
	            if time.time() - start > 30:
	                window.destroy()
	                break
	            # Reset the stream for the next capture
	            stream.seek(0)
	            stream.truncate()
        
        #counter = 0
        print("Hello")
        show_frame()
        window.mainloop()        
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()


