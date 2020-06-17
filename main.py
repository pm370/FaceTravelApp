from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox as mbox
from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import shutil
import cv2
import PhotoGallery
import colorfulness
import date_sort
import resize
import crop
import emotion_sort
import videorender


class Application:
	def __init__(self):
		self.pathImages='./images'
		self.pathCroppedImages='./detected_faces'
		self.pathSortedImages='./sorted_images'

		self.root = Tk()
		self.root.title("Face Travel App")
		self.root.geometry('750x500')
		self.root.resizable(False, False)

		self.f1 = Frame(self.root, width=750, height=500)
		self.f2 = Frame(self.root, width=750, height=500)
		self.f3 = Frame(self.root, width=750, height=500)
		self.f4 = Frame(self.root, width=750, height=500)

		for frame in (self.f1, self.f2, self.f3, self.f4):
			frame.grid(row=0, column=0, sticky='news')

		self.panel = Label(self.f4)
		#panel.pack(padx=10, pady=15)
		#self.current_image = None
		#self.vs = cv2.VideoCapture('video.avi') 
		self.panel.place(x=130,y=30)
		self.root.config(cursor="arrow")

		#Menubar
		self.menubar = Menu(self.root)

		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Browse", command=self.donothing)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Export", command=lambda:self.exportVideo())
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.root.quit)

		self.actionmenu = Menu(self.menubar, tearoff=0)

		self.sortmenu = Menu(self.actionmenu, tearoff=0)
		self.sortmenu.add_command(label="By Color", command=lambda:self.sortByColorMenu())
		self.sortmenu.add_command(label="By Date", command=lambda:self.sortByDateMenu())
		self.sortmenu.add_command(label="By Emotion", command=lambda:self.sortByEmotionMenu())

		self.actionmenu.add_cascade(label="Sort",menu=self.sortmenu)

		self.menubar.add_cascade(label="File", menu=self.filemenu)
		self.menubar.add_cascade(label="Action", menu=self.actionmenu)

		self.root.config(menu=self.menubar)

		#Frame 1
		self.fontBrowseBtn = tkFont.Font(family='Helvetica', size=10, weight='bold')
		self.lblText1 = Label(self.f1, text = 'Select a folder by clicking on the button below', font=self.fontBrowseBtn).place(x=200, y=100)
		self.btnBrowse = Button(self.f1, text ='Browse', width=10, height=3, font=self.fontBrowseBtn, command = lambda:self.openFolder()).place(bordermode=OUTSIDE, x=300, y=150) 

		###Frame 2
		self.varPath=StringVar()
		Button(self.f2, text='Back', font=self.fontBrowseBtn, command=lambda:self.raise_frame(self.f1)).place(x=1, y=1)
		Label(self.f2, textvariable=self.varPath, font=self.fontBrowseBtn).place(x=100, y=2)
		self.canvas1=Canvas(self.f2,bg='#FFFFFF',width=700,height=500)
		self.vbar1=Scrollbar(self.f2,orient=VERTICAL)
		self.vbar1.pack(side=RIGHT,fill=Y)
		self.canvas1.pack(side=LEFT,expand=True, fill=X)

		###Frame 3

		Button(self.f3, text='Back', font=self.fontBrowseBtn, command=lambda:self.raise_frame(self.f2)).place(x=1, y=1)
		Label(self.f3, text="Sorted Images Gallery", font=self.fontBrowseBtn).place(x=100, y=2)
		self.canvas2=Canvas(self.f3,bg='#FFFFFF',width=700,height=500)
		self.vbar2=Scrollbar(self.f3,orient=VERTICAL)
		self.vbar2.pack(side=RIGHT,fill=Y)
		self.canvas2.pack(side=LEFT,expand=True, fill=X)
		Button(self.f3,text='Preview Video', font=self.fontBrowseBtn, command=lambda:self.previewVideo()).place(x=320,y=460)

		###Frame 4

		Button(self.f4, text='Back', font=self.fontBrowseBtn, command=lambda:self.raise_frame(self.f3)).place(x=1, y=1)
		Label(self.f4, text="Preview of the Video", font=self.fontBrowseBtn).place(x=100, y=2)

	def raise_frame(self,frame):
		frame.tkraise()

	def openFolder(self):
	    path = filedialog.askdirectory()
	    self.varPath.set(path)
	    resize.copy(path, self.pathImages)
	    PhotoGallery.gallery(self.pathImages, 320, 240)
	    self.updateGallery1()
	    self.raise_frame(self.f2)

	def updateGallery1(self):
		self.img1 = PhotoImage(file="resized_album.png")
		self.canvas1.create_image(0,0, anchor=NW, image=self.img1)
		self.vbar1.config(command=self.canvas1.yview)
		self.canvas1.config(width=300,height=400,yscrollcommand=self.vbar1.set)
		self.canvas1.configure(scrollregion = self.canvas1.bbox("all"))

	def updateGallery2(self):
		self.img2 = PhotoImage(file="resized_album.png")
		self.canvas2.create_image(0,0, anchor=NW, image=self.img2)
		self.vbar2.config(command=self.canvas2.yview)
		self.canvas2.config(width=300,height=400,yscrollcommand=self.vbar2.set)
		self.canvas2.configure(scrollregion = self.canvas2.bbox("all"))	

	def sortByColorMenu(self):
	    crop.crop_image(self.pathImages)
	    colorfulness.sort_c(self.pathCroppedImages)
	    PhotoGallery.gallery(self.pathSortedImages, 250, 200)
	    self.updateGallery2()
	    self.raise_frame(self.f3)
	    videorender.render(self.pathSortedImages)

	def sortByDateMenu(self):
	    crop.crop_image(self.pathImages)
	    date_sort.sort_d(self.pathCroppedImages)
	    PhotoGallery.gallery(self.pathSortedImages, 250, 200)
	    self.updateGallery2()
	    self.raise_frame(self.f3)
	    videorender.render(self.pathSortedImages)

	def sortByEmotionMenu(self):
	    crop.crop_image(self.pathImages)
	    emotion_sort.sort_e(self.pathCroppedImages)
	    PhotoGallery.gallery(self.pathSortedImages, 250, 200)
	    self.updateGallery2()
	    self.raise_frame(self.f3)
	    videorender.render(self.pathSortedImages)

	def video_loop(self):
			ok, frame = self.vs.read()
			if ok:
				key = cv2.waitKey(1000)
				cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
				self.current_image = Image.fromarray(cv2image)  # convert image for PIL
				imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter 
				self.panel.imgtk = imgtk  
				self.panel.config(image=imgtk)
			self.f4.after(100, self.video_loop)

	def updateVideo(self):
		self.current_image = None
		self.vs = cv2.VideoCapture('video.avi') 
		self.video_loop()


	def previewVideo(self):
	    self.raise_frame(self.f4)
	    self.updateVideo()
	    #self.vs.release()

	def exportVideo(self):
		exportPath = filedialog.askdirectory()
		shutil.copyfile('video.avi', exportPath+'/video.avi')
		print("Video File Saved Successfully")
		mbox.showinfo("Information", "Video File Exported Successfully")
	
	def donothing(self):
   		print("Do nothing")

if __name__=="__main__":
	obj=Application()
	obj.raise_frame(obj.f1)
	obj.root.mainloop()


