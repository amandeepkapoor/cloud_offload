import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camera.start_recording('/home/pi/Desktop/test.h264')
camera.wait_recording(20)
camera.stop_recording()