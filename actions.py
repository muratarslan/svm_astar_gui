import sys
import os
import time
import cv2
import config as c
import glob
from gi.repository import Gtk
from svm import *

directory = c.DATASET_DIRECTORY
negative = c.NEGATIVE
positive = c.POSITIVE

class SvmController:
        
        """Represents Nao Controller GUI

        params: glade_file_path - path:string
        """
	def __init__(self, glade_file_path=c.GLADE_FILE_PATH):
            self.glade_file_path = glade_file_path
            
            # Gtk Builder Init
            self.builder = Gtk.Builder()
            self.builder.add_from_file(self.glade_file_path)
            self.builder.connect_signals(self)

            # Add UI Components
            self.window = self.builder.get_object("svmWindow")

            # Show UI
            self.window.show_all()

        ### Destroy GUI
        def destroy(self, widget):
            print "destroyed"
            Gtk.main_quit()

   	### Choose Area Image
	def chooseFile(self, widget):
	    self.input = widget.get_filename()
	    print "Choosen Image: ", self.input
	    return self.input

	### Create Dataset
	def crop(self, widget):
	    global directroy
	    file = self.input
	    img = cv2.imread(file)
	    i = 0
	    if os.path.isdir(directory) == False:
		os.mkdir(directory)  # Create a folder
		os.chdir(directory)  # Change directory
	    else:
		os.chdir(directory)  # Change directory
	    
	    os.mkdir("negative")
	    os.mkdir("positive")

	    for v in range(0, 640, 20):
		for c in range (0, 480, 20):
		    crop_img = img[c:20+c, v:20+v] # Crop from x, y, w, h 
		    #cv2.imshow("cropped", crop_img)
		    cv2.imwrite(str(i) + '.png', crop_img)
		    i += 1
	    print "Image Cropped and dataset created..."

	### Change positive negative images names
	def rename(self, widget):
	    global positive
	    global negative
	    os.chdir(negative)
	    for i, f in enumerate(glob.glob('*.png')):
	      print "%s -> %s.png" % (f, i)
	      os.rename(f, "%s.png" % i)

	    os.chdir(positive)
	    for i, f in enumerate(glob.glob('*.png')):
	      print "%s -> %s.png" % (f, i)
	      os.rename(f, "%s.png" % i)

	def solve(self,widget):
	    path()
