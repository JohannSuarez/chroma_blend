from skimage import data, color, io, img_as_float
from PIL import Image, ImageEnhance

import numpy as np
import cv2
import os, sys, argparse





''' Color constants. This should be moved elsewhere.'''

class bcolors:

	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	CYAN = "\033[36m"
	WHITE = "\033[37m"
	PURPLE = "\033[1;35m"
	YELLOW = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'








'''
A size corrector. The chroma image is expected to be smaller than the luma image. 
If that is the case, the dimensions must be matched to the luma image prior to any other operation.
This function must ONLY be visited if it's confirmed they're not the same size.
'''

def size_corrector(w, h, image):
	new_image = image.resize((w, h))
	return new_image





''' Formatting the name of the output file. '''

def append_id(filename):
	
	dot_index =  filename.find(".")
	return filename[:dot_index] + '_f' + filename[dot_index:]





''' Parameter requirements for color_blend:

	[Assuming this is being run as a module for batch tasks]
	
	Black and white image has to be in number sequence. Ex: (0001.jpg, 0002.jpg)
	Colored image has to match its respective B & W image's name, but with "_c" appended. Ex: (0001_c.jpg, 0002_c.jpg)
	Output name should be a formatted string; the number sequence appended by "_f" for final. Ex: (0001_f.png, 0002_f.png) 
'''

def color_blend(black_white, colored):


	#Make is_image() check here. Can't just be the name that determines if the image is legit. Implement try-catch mechanism

	bw_image = Image.open(black_white)				
	remastered_image = Image.open(colored)
	

	#Variables to perform size consistency check
	bw_w, bw_h = bw_image.size
	cl_w, cl_h = remastered_image.size
	
	
	if(bw_w - cl_w != 0 ) or (bw_h - cl_h != 0):
		print("Image pair are different sizes, correcting...")
		remastered_image = remastered_image.resize((bw_w, bw_h))

	# Construct RGB version of both b&w image and the chroma image. Needed to seamlessly convert to hsv. 			
	bw_image_rgb = bw_image.convert('RGB')
	remastered_image_rgb = remastered_image.convert('RGB')

	#numpy array

	bw_image_rgb = np.array(bw_image_rgb)	
	remastered_image_rgb = np.array(remastered_image_rgb)

	# Convert both the input image and color mask to Hue Saturation Value (HSV) colorspace
	img_hsv = color.rgb2hsv(bw_image_rgb)
	color_mask_hsv = color.rgb2hsv(remastered_image_rgb)				# Color mask is THE colored(remastered) version.
	



	#Replacing the hue and saturation of the black and white image with values from color mask
	img_hsv[..., 0] = color_mask_hsv[..., 0]
	img_hsv[..., 1] = color_mask_hsv[..., 1]
	img_masked = color.hsv2rgb(img_hsv)

	final = Image.fromarray((img_masked * 255).astype(np.uint8))			# Converting numpy image to format recognized by PIL


	brightener = ImageEnhance.Brightness(final)
	final = brightener.enhance(1.15)

	print(bcolors.OKGREEN + "Color blend success! " + "Generated " + bcolors.YELLOW + append_id(black_white) + bcolors.ENDC)
	return final





def main():

	print(bcolors.OKBLUE + "Main activated." + bcolors.ENDC)	

	parser = argparse.ArgumentParser()
	parser.add_argument("bw_input", help="The black and white input to blend colors on.")
	parser.add_argument("colored_input", help="The image with the chroma that you want to blend the b&w image's luma on.")
	user_input = parser.parse_args()

	
	result = color_blend(user_input.bw_input, user_input.colored_input)
	result.save(append_id(user_input.bw_input))





if __name__ == "__main__":								# So if this .py were used as a module, main wouldn't execute. 
    main()
	
