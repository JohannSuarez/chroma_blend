'''
In charge of splitting video to frames (Input is a video)
Is only fed mp4s.
Outputs frames(PNG)
'''

import os
import sys
import argparse
import shutil
import cv2


def video_length(vid_input):
    '''
    Determines video length.
    Primarily to ensure file isn't empty.
    '''
    cap = cv2.VideoCapture(vid_input)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def custom_directory_name(name_input):
    '''
    Creates a string for directory name.
    String is based off original filename.
    '''

    # Starts at two, because the string could start with double periods
    # if the file is outside the directory.

    dot_index = name_input.find(".", 2)

    return name_input[:dot_index]


def frame_namer(cap, ret, dir_name, frame_count, suffix):
    '''
    A helper function for frame_extract, made to avoid writing the same code twice.
    In charge of creating, and naming the frames.
    '''

    while ret:

        try:
            ret, frame = cap.read()
            file_name = dir_name + "/" + \
                str(frame_count) + suffix + ".png"
            frame_count = frame_count + 1
            cv2.imwrite(file_name, frame)
            print("Extracted " + file_name + "...")
        except: # pylint: disable=W0702
            print("No frame " + file_name + " . Ending extraction.")
            return frame_count - 2



def frame_extract(vid_input, which_directory):
    '''
    The main component. Extracts frames from given .mp4
	Input is .mp4, and an optional directory name.
    '''
    # Checks that the vid duration isn't 0.0
    duration = video_length(vid_input)
    if duration == 0:
        print("Length is 0. Error.")
        sys.exit()

    cap = cv2.VideoCapture(vid_input)  # Open video.
    frame_count = 0  # Keep track of frames.

    # Testing the first frame, ret is a boolean, frame is the actual frame.
    ret, frame = cap.read()

    if __name__ == "__main__":

        # If this py is ran as main, the output will be in a custom directory
        dir_name = custom_directory_name(vid_input)

        if os.path.isdir(dir_name):
            print("Directory " + dir_name + " exists. Cleaning...")
            # Clean
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
        else:
            # Make custom directory
            print("Hello" + dir_name)
            os.mkdir(dir_name)

        file_name = dir_name + "/" + str(frame_count) + ".png"
        cv2.imwrite(file_name, frame)
        print("Extracted " + file_name + "...")
        suffix = ""

        # First parameter is its name, second is the image.
        frame_count = frame_count + 1

        frame_namer(cap, ret, dir_name, frame_count, suffix)



    else:
        # Only difference is directory output.
        # If which directory contains something,
        # it's ran as module.

        if which_directory not in ("bw_frames", "source_frames"):
        #if (which_directory != "bw_frames") and (which_directory != "source_frames"):
            print(""" Error: vid2png's called as module,
            but output directory isn't bw_frames or source_frames.
            """)

            print("Received directory is: " + which_directory)
        else:
            print("Directory input recognized")

            if which_directory == "source_frames":
                suffix = "_c"
            else:
                suffix = ""

            dir_name = which_directory

            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name)  # Clean
                os.mkdir(dir_name)
            else:
                os.mkdir(dir_name)  # Make custom directory

            file_name = dir_name + "/" + str(frame_count) + suffix + ".png"
            cv2.imwrite(file_name, frame)
            print("Extracted " + file_name + "...")
            # First param is its name, second is the image.
            frame_count = frame_count + 1

            #Variables used: ret, frame, file_name, frame_count, suffix
            return frame_namer(cap, ret, dir_name, frame_count, suffix)


def main():
    '''
    Procedures if this module were
    called on its own (as a main)
    '''
    # Create argparse to be able to dictate input.

    print("Vid2PNGs activated as main.")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "vid_input",
        help="The .mp4 input to convert to png frames.")
    user_input = parser.parse_args()

    frame_extract(user_input.vid_input, "NULL")


if __name__ == "__main__":
    main()
