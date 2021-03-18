'''
The main module of the chroma_blend package.
(Improved, and adheres to OOP principles)
'''

import os
import argparse
import shutil
import cv2
from cblend_modules.colorizer import BColors as fontc
from cblend_modules.colorizer import color_blend
from cblend_modules.vid2pngs import frame_extract


class CBlend:

    def __init__(self): # Initialize (Think: A constructor)
        # Currently, there are no variables
        # that are shared between methods. 
        # No need for class-wide variables yet.
        pass





    def folders_manager(self): # No input
        '''
        Manages the folders required
        for the operations. If they're there, folders are cleaned.
        If not, the folders are created.
        '''
        if not os.path.isdir("bw_frames"):
            print(
                fontc.YELLOW +
                "Creating folder: bw_frames. This will contain the black and white frames." +
                fontc.ENDC)
            os.mkdir("bw_frames")
        else:
            print("bw_frames directory found. Clearing contents..")
            shutil.rmtree('bw_frames/')
            os.mkdir("bw_frames")

        if not os.path.isdir("source_frames"):
            print(
                fontc.YELLOW +
                "Creating folder: bw_folder. This will contain the colored source frames." +
                fontc.ENDC)
            os.mkdir("source_frames")
        else:
            print("source_frames directory found. Clearing contents..")
            shutil.rmtree('source_frames/')
            os.mkdir("source_frames")

        if not os.path.isdir("output_frames"):
            print(
                fontc.YELLOW +
                """Creating folder: output_frames.
                This will contain the final higher-res colored frames.
                """
                + fontc.ENDC)
            os.mkdir("output_frames")
        else:
            print("output_frames directory found. Clearing contents..")
            shutil.rmtree('output_frames/')
            os.mkdir("output_frames")


    def png2mp4(self, vidin: str): 
        '''
        Function that converts the sequence of pngs to mp4's.
        '''

        #Get FPS of inputted bw video.
        cap=cv2.VideoCapture(vidin)
        fps=cap.get(cv2.CAP_PROP_FPS)



        #Preparing all variables required to write a video using the f_out frames.
        images = [img for img in os.listdir('output_frames') if img.endswith(".png")]
        frame = cv2.imread(os.path.join('output_frames', images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter('final_output.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))


        #The list is initially unsorted, this is to fix that.
        images = sorted(images, key=lambda x: int(x[0:-6]))

        print("Writing video. Please wait..")

        for image in images:

            video.write(cv2.imread(os.path.join('output_frames', image)))

        

        cv2.destroyAllWindows()
        video.release()


lise = CBlend()
lise.png2mp4('output_frames/0_f.png')