from PIL import Image
import sys, os

path = os.path.abspath("") + "/"
processed = False
	

def processImage(path, name):
	img = Image.open(os.path.join(path, name))
	size = img.size[0] / 4 # splits the width of the image by 3, expecting the 3x2 layout blender produces.
	splitAndSave(img, 2*size, size, size, addToFilename(name, "_Right-X"))
	splitAndSave(img, 3*size, size, size, addToFilename(name, "_Back-Z"))
	splitAndSave(img, 0, size, size, addToFilename(name, "_Left+X"))
	splitAndSave(img, size, 2*size, size, addToFilename(name, "_Down-Y"))
	splitAndSave(img, size, 0, size, addToFilename(name, "_Up+Y"))
	splitAndSave(img, size , size, size, addToFilename(name, "_Front+Z"))

def addToFilename(name, add):
	name = name.split('.')
	return name[0] + add + "." + name[1]

def splitAndSave(img, startX, startY, size, name):
	area = (startX, startY, startX + size, startY + size)
	saveImage(img.crop(area), path, name)

def saveImage(img, path, name):
	try:
		img.save(os.path.join(path, name))
	except:
		print ("   ERROR: Could not convert image.")
		pass


processImage(path, "sky.png")
processed = True

if not processed:
	print ("  ERROR: No Image")
	print ("   usage: 'python script.py image-name.png'")