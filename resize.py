from PIL import Image
import os, sys
import shutil

#path = "F:/Python/Study/ProjectDemo/demo"

def resize(path, x, y):
    for item in os.listdir(path):
        if os.path.isfile(path+"/"+item):
            im = Image.open(path+"/"+item)
            imResize = im.resize((x, y), Image.ANTIALIAS)
            imResize.save(path+"/"+item, 'JPEG', quality=90)

def copy(source,dest):
	for item in os.listdir(dest):
		if os.path.isfile(dest+"/"+item):
			os.remove(dest+"/"+item)
	n=0
	for item in os.listdir(source):
		if os.path.isfile(source+"/"+item):
				n=n+1
				shutil.copyfile(source+"/"+item, dest+"/pic"+str(n)+".jpg")
#resize()