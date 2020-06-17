import cv2
import sys
import os
#import videorender
import numpy as np
#import add_audio
from keras.preprocessing import image
import cv2
import numpy as np

def crop_image(imageDir):
	prototxt="deploy.prototxt.txt"
	model="res10_300x300_ssd_iter_140000.caffemodel"
	confidencedefault=0.5
	
	#imageDir="./images/"
	#imageDir="F:\\Python\\Study\\ProjectDemo\\images\\"

	# load our serialized model from disk
	print("[INFO] loading model...")

	net = cv2.dnn.readNetFromCaffe(prototxt,model)
	n=100
	pathExtractedFaces="./detected_faces/"


	for file in os.listdir(imageDir):
		n=n+1
		# load the input image and construct an input blob for the image
		# by resizing to a fixed 300x300 pixels and then normalizing it
		image = cv2.imread(imageDir+"/"+file)
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (500, 500)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the detections and
		# predictions
		print("[INFO] computing object detections...")
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > confidencedefault:
				# compute the (x, y)-coordinates of the bounding box for the
				# object
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				#Choosing the region of interest
				roi_color = image[startY:endY+100,startX-50:endX+50]
				#print(pathExtractedFaces+str(n)+"cropped.jpg")
				cv2.imwrite(pathExtractedFaces+str(n)+"cropped.jpg", roi_color)

	print("[INFO] image saved successfully...")
			

	
	#cv2.imwrite(str(n)+"detectedface.jpg",image)

#print("Rendering the video")

#videorender.render(pathSadFaces,pathHappyFaces,pathAngryFaces,pathNeutralFaces,pathSurpriseFaces)

#print("Adding audio to the video file")
#add_audio.audio()
	


