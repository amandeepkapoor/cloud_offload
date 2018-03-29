import io
import socket
import struct
import datetime
import time
import picamera
from PIL import Image

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('199.60.17.11', 23000))

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
        for foo in camera.capture_continuous(stream, 'rgb'):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            t1_network = datetime.datetime.now()
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())

	
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            stream.write(connection.read(image_len))
            stream.seek(0)
            #image = Image.open(stream)
            image = Image.frombytes('RGB', (640, 480), bytearray(stream))
            print('Image is %dx%d' % image.size)
            t2_network = datetime.datetime.now()
            tdif_network = t2_network - t1_network
            print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')

	    
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 30:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
