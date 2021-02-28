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
        # Variables for png2mp4
        self.cap = None
        self.fps = 0
        self.image_folder = 'output_frames'
        self.video_name = 'final_output.avi'

        self.images = 0
        self.frame = None
        self.height = 0
        self.width  = 0
        self.layers = None
        self.video = None

        # Variables for video_blend
        self.source_frames_count = 0
        self.bw_frames_count = 0
        self.loop_len_count = 0



    def folders_manager(self):
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


    def png2mp4(self, vidin):
        '''
        Function that converts the sequence of pngs to mp4's.
        '''

        #Get FPS of inputted bw video.
        self.cap=cv2.VideoCapture(vidin)
        self.fps=self.cap.get(cv2.CAP_PROP_FPS)



        #Preparing all variables required to write a video using the f_out frames.
        self.images = [img for img in os.listdir(self.image_folder) if img.endswith(".png")]
        self.frame = cv2.imread(os.path.join(self.image_folder, self.images[0]))
        self.height, self.width, self.layers = self.frame.shape
        self.video = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.width,self.height))


        #The list is initially unsorted, this is to fix that.
        self.images = sorted(self.images, key=lambda x: int(x[0:-6]))

        print("Writing video. Please wait..")

        for self.image in self.images:

            self.video.write(cv2.imread(os.path.join(self.image_folder, self.image)))

        

        cv2.destroyAllWindows()
        self.video.release()


    """
    def video_blend(self, ):
        '''
        video_blend manages arguments, runs folder checks, calls other methods.
        '''



        print(fontc.OKBLUE + "Cblend activated." + fontc.ENDC)


        self.folders_manager()


        #The two input videos are extracted one at a time,
        #beginning with the colored frames. Second is black and white frames.


        source_frames_count = frame_extract(
            user_input.colored_vid_input, "source_frames")
        bw_frames_count = frame_extract(user_input.bw_vid_input, "bw_frames")

        print(
            fontc.CYAN +
            "Colored frames counted: " +
            fontc.ENDC +
            str(source_frames_count))
        print(
            fontc.WHITE +
            "Black and white frames counted: " +
            fontc.ENDC +
            str(bw_frames_count))

        if source_frames_count != bw_frames_count:
            print(
                fontc.YELLOW +
                "Warning: Inconsistent number of frames. Some frames will not be generated." +
                fontc.ENDC)
        else:
            loop_len_count = source_frames_count

        if source_frames_count < bw_frames_count:
            loop_len_count = source_frames_count
        elif bw_frames_count < source_frames_count:
            loop_len_count = bw_frames_count


        for counter in range(loop_len_count + 1):

            bw_name = "bw_frames/" + str(counter) + ".png"
            cl_name = "source_frames/" + str(counter) + "_c.png"
            final_name = "output_frames/" + str(counter) + "_f.png"
            #print("File names are: " + bw_name + " and " +  cl_name)
            final_output = color_blend(bw_name, cl_name)
            final_output.save(final_name)


        print("Creating video..")

        png2mp4(user_input.bw_vid_input)


        print("Cleaning up extracted frames...")
        shutil.rmtree('source_frames/')
        shutil.rmtree('bw_frames/')

        print("All done!")
    """


gabby = CBlend()
gabby.folders_manager()
#gabby.png2mp4("demo_files/bw.mp4")