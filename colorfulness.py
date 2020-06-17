# import the necessary packages
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os
def image_colorfulness(image):
	# split the image into its respective RGB components
	(B, G, R) = cv2.split(image.astype("float"))

	# compute rg = R - G
	rg = np.absolute(R - G)

	# compute yb = 0.5 * (R + G) - B
	yb = np.absolute(0.5 * (R + G) - B)

	# compute the mean and standard deviation of both `rg` and `yb`
	(rgMean, rgStd) = (np.mean(rg), np.std(rg))
	(ybMean, ybStd) = (np.mean(yb), np.std(yb))

	# combine the mean and standard deviations
	stdRoot = np.sqrt((rgStd ** 2) + (ybStd ** 2))
	meanRoot = np.sqrt((rgMean ** 2) + (ybMean ** 2))

	# derive the "colorfulness" metric and return it
	return stdRoot + (0.3 * meanRoot)

#Change imageDir path to the folder with cropped images
#imageDir="F:\\Downloads\\image-colorfulness\\ukbench_sample\\"

def sort_c(imageDir):
	# initialize the results list
	print("[INFO] computing colorfulness metric for dataset...")
	results = []

	# loop over the image paths
	for file in os.listdir(imageDir+'/'):
		# load the image, resize it (to speed up computation), and
		# compute the colorfulness metric for the image
		image = cv2.imread(imageDir+'/'+file)
		image = imutils.resize(image, width=250)
		C = image_colorfulness(image)

		# add the image and colorfulness metric to the results list
		results.append((image, C))

	# sort the results with more colorful images at the front of the
	# list, then build the lists of the *most colorful* and *least
	# colorful* images
	print("[INFO] displaying results...")

	results = sorted(results, key=lambda x: x[1])

	n=0

	#Change writePath where you want to save the sorted images
	writePath="./sorted_images/"


	filelist = [ f for f in os.listdir(writePath) if f.endswith(".jpg") ]
	for file in filelist:
		os.remove(writePath+file)
	print("deleted existing data")		
	
	for image in results:
		n=n+1
		cv2.imwrite(writePath+str(n)+"pic.jpg", image[0])

#sort_c(imageDir)