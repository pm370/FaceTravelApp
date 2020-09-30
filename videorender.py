import cv2 #For image manipulation
import numpy
import glob #This module is used to find files matching a certain pattern


def render(imageDir): #Path is an argument given from the function call in app.py. This is the path of folder which contains the detected images.
    image_array=[]

    for file in glob.glob(imageDir+'/'+'*.jpg'):
        image=cv2.imread(file)
        # image.shape returns the dimesions of the image i.e, its height width as well as how many channels(r,g,b,and more) are in the image
        height, width , channels = image.shape #returns values of h,w,channels from tuple image.shape
        size=(450,450) #This size will be given later as an argument to the VideoWriter class
        resizeimage=cv2.resize(image,size,interpolation=cv2.INTER_AREA)
        
        image_array.append(resizeimage) #Saving the image in an array 


    out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'),0.5,size)
    print("Rendering "+str(len(image_array))+" images")

    for i in range(len(image_array)):
        out.write(image_array[i])

    out.release()
    print("Video rendered successfully")
            
