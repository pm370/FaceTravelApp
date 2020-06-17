from tkinter import *
from PIL import Image
import os
import math
from tkinter.tix import ScrolledWindow
import cv2
import resize


def border(img, width=10, color="White"):
    x,y = img.size
    bordered = Image.new("RGB", (x+(2*width), y+(2*width)), color)
    bordered.paste(img, (width, width))
    return bordered

def normalize(imgs):
    "Normalize height for all images to shortest image."
    shortest = min([ x.size[1] for x in imgs ])
    resized = []
    for img in imgs:
        height_ratio = float(img.size[1]) / shortest
        new_width = img.size[0] * height_ratio
        img2 = img.resize((int(new_width), int(shortest)), Image.ANTIALIAS)
        resized.append(img2)
    return resized

def chunk(imgs):
    "Break images into chunks equal to size of smallest image."
    smallest = min([ x.size[0] for x in imgs ])
    height = imgs[0].size[1]
    chunked_imgs = []
    for img in imgs:
        parts = math.ceil((img.size[0] * 1.0) / smallest)
        for i in range(0, parts):
            box = (i*smallest, 0, (i+1)*smallest, height)
            img2 = img.crop(box)
            img2.load()
            chunked_imgs.append(img2)
    return chunked_imgs

def merge(imgs, per_row=4):
    "Format equally sized images into rows and columns."
    width = imgs[0].size[0]
    height = imgs[0].size[1]
    page_width = width * per_row
    page_height = height * math.ceil((1.0*len(imgs)) / 4)
    page = Image.new("RGB", (page_width, page_height), "White")
    column = 0
    row = 0
    for img in imgs:
        if column != 0 and column % per_row == 0:
            row = row + 1
            column = 0
        pos = (width*column, height*row)
        page.paste(img, pos)
        column = column + 1
    return page

def album(imgs):
    imgs = normalize(imgs)
    imgs = chunk(imgs)
    imgs = [ border(x) for x in imgs ]
    return merge(imgs)

#imageDir = "F:/Python/Study/ProjectDemo/images"
#tempPath="./images/"

def gallery(imageDir, x, y):
    print(imageDir)
    n=1000
    
#    filelist = [ f for f in os.listdir(tempPath) if f.endswith(".jpg") ]
#    for file in filelist:
#        os.remove(tempPath+file)

#    for file in os.listdir(imageDir+'/'):
#        img1=cv2.imread(imageDir+'/'+file)
#        cv2.imwrite(imageDir+str(n)+"pic.jpg",img1[0])

    resize.resize(imageDir, x, y)
    imgs=[]
    n_file=0
    filelist = [ f for f in os.listdir(imageDir+"/") if f.endswith(".jpg" or ".png") ]
    for file in filelist:
        n_file=n_file+1
        imgs.append(Image.open(imageDir+"/"+file))
    #img = Image.open("1pic.jpg")

    album(imgs).save("album.png")
    basewidth = 700
    img1 = Image.open("album.png")
    wpercent = (basewidth / float(img1.size[0]))
    hsize = int((float(img1.size[1]) * float(wpercent)))
    img1 = img1.resize((basewidth, hsize), Image.ANTIALIAS)
    img1.save("resized_album.png")



