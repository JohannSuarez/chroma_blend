from PIL import Image
import numpy as np
import cv2
import logging
import os, sys, argparse, shutil


#in charge of splitting video to frames (Input is a video)
#Is only fed mp4s.
#Spits out frames(PNG)


def video_length(vid_input):
	cap = cv2.VideoCapture(vid_input)
	length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	return length





def custom_directory_name(name_input):
	dot_index =  name_input.find(".")
	return name_input[:dot_index]





def frame_extract(vid_input, which_directory):
	
	len = video_length(vid_input)			#Checks that the vid duration isn't 0.0
	if(len == 0):
		print("Length is 0. Error.")
		sys.exit()

	cap = cv2.VideoCapture(vid_input)		#Open video.
	frame_count = 0					#Keep track of frames.

	ret, frame = cap.read()				#Testing the first frame, ret is a boolean, frame is the actual frame.

	if __name__ == "__main__":

		dir_name = custom_directory_name(vid_input)				#If this py is ran as main, the output will be in a custom directory

		if(os.path.isdir(dir_name) == True):
			print("Directory " + dir_name + " exists. Cleaning...")
			shutil.rmtree(dir_name)						#Clean
			os.mkdir(dir_name)
		else:
			os.mkdir(dir_name)						#Make custom directory

		file_name = dir_name + "/" + str(frame_count) + ".png"
		cv2.imwrite(file_name, frame)
		print("Extracted " + file_name + "...")
		frame_count = frame_count + 1						#First param is its name, second is the image.
											
		while ret:
			
			try:				
				ret, frame = cap.read()	
				file_name = dir_name + "/" + str(frame_count) + ".png"
				frame_count = frame_count + 1
				cv2.imwrite(file_name, frame)
				print("Extracted " + file_name + "...")
			except:
				print("No frame " + file_name + " . Ending extraction." )	



			
	else:										#Only difference is directory output.
	
		if (which_directory != "bw_frames") and (which_directory != "source_frames"):
			print("Error: vid2png's called as module, but provided output directory isn't bw_frames or source_frames.")
			print("Received directory is: " + which_directory)
		else:
			print("Directory input recognized")
			
			if(which_directory == "source_frames"):
				suffix = "_c"
			else:
				suffix = ""

			dir_name = which_directory
			
			if(os.path.isdir(dir_name) == True):
				shutil.rmtree(dir_name)						#Clean
				os.mkdir(dir_name)
			else:
				os.mkdir(dir_name)						#Make custom directory

			file_name = dir_name + "/" + str(frame_count) + suffix + ".png"
			cv2.imwrite(file_name, frame)
			print("Extracted " + file_name + "...")
			frame_count = frame_count + 1						#First param is its name, second is the image.
												
			while ret:
				
				try:				
					ret, frame = cap.read()	
					file_name = dir_name + "/" + str(frame_count) + suffix + ".png"
					frame_count = frame_count + 1
					cv2.imwrite(file_name, frame)
					print("Extracted " + file_name + "...")
				except:
					print("No frame " + file_name + " . Ending extraction." )
					return frame_count - 2	
			
	
			
	
	
	
def main():
	
	#Create argparse to be able to dictate input.

	print("Vid2PNGs activated as main.")
	
	parser = argparse.ArgumentParser()
	parser.add_argument("vid_input", help="The .mp4 input to convert to png frames.")
	user_input = parser.parse_args()


	frame = frame_extract(user_input.vid_input, "NULL")
	




if __name__ == "__main__":								
	main()
