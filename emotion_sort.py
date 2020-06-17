import cv2
import os
import sys
#import videorender
import numpy as np
#import add_audio
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

def sort_e(imageDir):
	classifier =load_model('Emotion_little_vgg.h5')

	class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

	#imageDir="./detected_faces/"

	writePath="./sorted_images/"


	n=0
	filelist = [ f for f in os.listdir(writePath) if f.endswith(".jpg") ]
	for file in filelist:
		os.remove(writePath+file)
		
	for file in os.listdir(imageDir):
		n=n+1
		roi_color= cv2.imread(imageDir+'/'+file)
		gray=cv2.cvtColor(roi_color,cv2.COLOR_BGR2GRAY)
		gray = cv2.resize(gray,(48,48),interpolation=cv2.INTER_AREA)
		if np.sum([gray])!=0:
			roi = gray.astype('float')/255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi,axis=0)
		preds = classifier.predict(roi)[0]
		label=class_labels[preds.argmax()]
		print(label)
		#Sad->Angry->Neutral->Surprise->Happy
		if label == 'Happy':
			cv2.imwrite(writePath+"e"+str(n)+"pic.jpg", roi_color)
			# cv2.imwrite(pathExtractedFaces+str(n)+"cropped.jpg", roi_color)
		elif label == 'Neutral':
			cv2.imwrite(writePath+"c"+str(n)+"pic.jpg", roi_color)
			# cv2.imwrite(pathExtractedFaces+str(n)+"cropped.jpg", roi_color)
		elif label == 'Angry':
			cv2.imwrite(writePath+"b"+str(n)+"pic.jpg", roi_color)
		elif label== 'Sad':
			cv2.imwrite(writePath+"a"+str(n)+"pic.jpg", roi_color)
		elif label == 'Surprise':
			cv2.imwrite(writePath+"d"+str(n)+"pic.jpg", roi_color)

	print("[INFO] all images saved according to emotions")