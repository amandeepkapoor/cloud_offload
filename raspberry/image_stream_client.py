import io
import datetime
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('199.60.17.11', 23000))

# Make a file-like object out of the connection
connection = client_socket.makefile('rwb')
try:
    camera = picamera.PiCamera()
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
    image_stream = io.BytesIO()
    count = 0
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        #connection.flush()
	
	# Read image back from server-socket
        
        data = connection.recv(1024)
        print('Received', str(data,'utf-8'))
	
	
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 120:
            break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        print(count)
        count = count + 1
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()