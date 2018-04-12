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


res = (320, 240)
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
imageFrame = tk.Frame(window, width=res[0], height=res[1]) #640, 480
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Video Frame
lmain = tk.Label(imageFrame)
lmain.grid(row = 0, column=0)

# Make a file-like object out of the connection
connection = client_socket.makefile('rwb')

list_loop = [0]*30
list_network = [0]*30
list_conv_1 = [0]*30
list_conv_2 = [0]*30

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (res[0], res[1])
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
	        counter = 0
	        for foo in camera.capture_continuous(stream, 'jpeg'): #rgb
	            #window.update_idletasks()
	            t1_loop = datetime.datetime.now()
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
	            #print("Image",image_len)
	            stream.write(connection.read(image_len))
	            t2_network = datetime.datetime.now()
	            #print("stream.tell():",stream.tell())

	            stream.seek(0)
	            
	            image = Image.open(stream)
	            imgtk = ImageTk.PhotoImage(image=image)
	            lmain.imgtk = imgtk
	            lmain.config(image=imgtk)
	            lmain.img = imgtk
	            
	            #image_np = np.array(image)
	            #cv.rectangle(image_np,(239,185),(390,336),(255,0,0),2)
	            #print("stream size: ",sys.getsizeof(stream))
	            #plt.imshow(image_np)
	            #plt.show()
	            #plt.pause(.0001)
	            #image = Image.frombytes('RGB', (640,480,3), (bytearray(stream)*(640*480*3)))
	            #print('Image is %dx%d' % image.size)
	            #t2_network = datetime.datetime.now()
	            #tdif_network = t2_network - t1_network
	            #print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')
	            
	            #image.show()
	            
	            if (counter == 30):
	                window.destroy()
	                break
	            # If we've been capturing for more than 30 seconds, quit
	            #if time.time() - start > 30:
	                #window.destroy()
	                #break
	            # Reset the stream for the next capture
	            stream.seek(0)
	            stream.truncate()
	            t2_loop = datetime.datetime.now()
	            tdif_loop = t2_loop - t1_loop
	            tdif_network = t2_network - t1_network
	            t_conv_1 = t1_network - t1_loop
	            t_conv_2 = t2_loop - t2_network
	            list_loop[counter] = (tdif_loop.seconds + tdif_loop.microseconds/1e6)
	            list_network[counter] = (tdif_network.seconds + tdif_network.microseconds/1e6)
	            list_conv_1[counter] = (t_conv_1.seconds + t_conv_1.microseconds/1e6)
	            list_conv_2[counter] = (t_conv_2.seconds + t_conv_2.microseconds/1e6)
	            counter += 1
	            #print('------')	            
	            #print('conv1 time =' + str(t_conv_1.seconds + t_conv_1.microseconds/1e6) + ' seconds')
	            #print('Network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')
	            #print('conv2 time =' + str(t_conv_2.seconds + t_conv_2.microseconds/1e6) + ' seconds')
	            #print('loop time =' + str(tdif_loop.seconds + tdif_loop.microseconds/1e6) + ' seconds')
        #counter = 0
        print("Hello")
        show_frame()
	
        print('max time (conv1, conv2, network, loop) =', max(list_conv_1[3:]),max(list_conv_2[3:]),max(list_network[3:]),max(list_loop[3:]))
        print('min time (conv1, conv2, network, loop) =', min(list_conv_1),min(list_conv_2),min(list_network),min(list_loop))
        print('avg time (conv1, conv2, network, loop) =', sum(list_conv_1[3:])/len(list_conv_1[3:]),sum(list_conv_2[3:])/len(list_conv_2[3:]),sum(list_network[3:])/len(list_network[3:]),sum(list_loop[3:])/len(list_loop[3:]))
        #print('loop time =' + str(tdif_loop.seconds + tdif_loop.microseconds/1e6) + ' seconds')
        window.mainloop()        
    # Write a length of zero to the stream to signal we're done

    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()


