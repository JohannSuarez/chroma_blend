#!/usr/bin/python3
'''
The main module of the chroma_blend package.
'''

import os
import argparse
import shutil
from cblend_modules.colorizer import BColors as fontc
from cblend_modules.colorizer import color_blend
from cblend_modules.vid2pngs import frame_extract


def folders_manager():
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


def main():
    '''
    Main function of chroma_blend.py
    Manages provded arguments, runs folder checks, calls other modules.
    '''

    source_frames_count = 0
    bw_frames_count = 0
    loop_len_count = 0

    print(fontc.OKBLUE + "Cblend activated." + fontc.ENDC)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bw_vid_input",
        help="The black and white .mp4 input to blend colors on.")
    parser.add_argument(
        "colored_vid_input",
        help="The .mp4 with the chroma that you want to blend the b&w mp4's luma on.")
    user_input = parser.parse_args()

    folders_manager()


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

    print("Cleaning up extracted frames...")
    shutil.rmtree('source_frames/')
    shutil.rmtree('bw_frames/')

    print("All done!")


if __name__ == "__main__":
    main()
