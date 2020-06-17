import os, time
from stat import *
import cv2

#path where images are stored
#imageDir="F:\\Internships\\FaceTravelApp\\Face-Travel-App-master\\image folder copy\\"
def sort_d(imageDir):
	res=[]
	

	for file in os.listdir(imageDir+'/'):
	    image = cv2.imread(imageDir+'/'+file)
	    st = os.stat(imageDir+'/'+file)
	    dt=time.asctime(time.localtime(st[ST_MTIME]))
	    res.append((image,dt))

	results = sorted(res, key=lambda x: x[1])
	print('[INFO] Images are sorted by date succesfully')

	n=0

	#path where you want to saved the sorted images by date
	writePath="./sorted_images/"
	filelist = [ f for f in os.listdir(writePath) if f.endswith(".jpg") ]
	for file in filelist:
		os.remove(writePath+file)

	for image in results:
	    n=n+1
	    cv2.imwrite(writePath+"pic"+str(n)+".jpg", image[0])

	print('[INFO] Images are stored in the folder')

#sort_d('./detected_faces')
