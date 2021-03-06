#importam lirariile necesare

from __future__ import print_function
from fpsboost.py import PiVideoStream
from fpsboost.py  import FPS 
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils 
import time
import cv2

#construim argumentul parse si  evident parsam argumentele 

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())


# initialize the camera and stream
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 480))
stream = camera.capture_continuous(rawCapture, format="bgr",
	use_video_port=True)

print("[INFO] sampling frames from `picamera` module...")
time.sleep(2.0)
fps = FPS().start() 

for (i, f) in enumerate(stream):
	
	frame = f.array
	frame = imutils.resize(frame, width=400)
	
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	
	rawCapture.truncate(0)
	fps.update()

	if i == args["num_frames"]:
		break

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()


print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows
vs.stop()
