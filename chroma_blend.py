#!/usr/bin/env python3
'''
The main module of the chroma_blend package.
(Improved, and adheres to OOP principles)
'''

from __future__ import annotations
from cblend_modules.colorizer import BColors as fontc
from cblend_modules.colorizer import Colorizer
from cblend_modules.vid2pngs import Vid2PNGs
from typing import Union, List

import os
import argparse
import shutil
import cv2


class CBlend:

    def __init__(self) -> None:  # Initialize (Think: A constructor)
        pass

    def folders_manager(self) -> None:  # No input
        '''
        Manages the folders required
        for the operations. If they're there, folders are cleaned.
        If not, the folders are created.
        '''

        folders = ['bw_frames', 'source_frames', 'output_frames']

        for folder in folders:
            if not os.path.isdir(folder):
                print(
                    fontc.YELLOW +
                    f"Creating folder: {folder}." +
                    fontc.ENDC)
                os.mkdir(folder)
            else:
                print(f"{folder} directory found. Clearing contents..")
                shutil.rmtree(folder)
                os.mkdir(folder)


    def png2mp4(self, vidin: str) -> None:
        '''
        Function that converts the sequence of pngs to mp4's.
        '''
        # Get FPS of input bw video.
        cap = cv2.VideoCapture(vidin)
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Preparing all variables required to write a video using the f_out
        # frames.
        images = [img for img in os.listdir(
            'output_frames') if img.endswith(".png")]

        frame = cv2.imread(os.path.join('output_frames', images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(
            'final_output.avi', cv2.VideoWriter_fourcc(
                *'XVID'), fps, (width, height))

        # The list is initially unsorted, this is to fix that.
        images = sorted(images, key=lambda x: int(x[0:-6]))

        print("Writing video. Please wait..")

        for image in images:
            video.write(cv2.imread(os.path.join('output_frames', image)))

        cv2.destroyAllWindows()
        video.release()


def main():
    '''
    Main function of chroma_blend.py
    Manages provded arguments, runs folder checks, calls other modules.
    '''
    # First objective of main is to collected provided arguments.
    # It'll hold them, initalize a chroma_blend object, and then give it the
    # held arguments.

    source_frames_count: int = 0
    bw_frames_count: int = 0
    loop_len_count: int = 0

    print(fontc.OKBLUE + "Cblend activated." + fontc.ENDC)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bw_vid_input",
        help="The black and white .mp4 input to blend colors on.")
    parser.add_argument(
        "colored_vid_input",
        help="The .mp4 with the chroma that you want to blend the b&w mp4's luma on.")
    user_input = parser.parse_args()

    cblend_instance = CBlend()

    # Check if all directories are in place.
    cblend_instance.folders_manager()

    v2p_instance = Vid2PNGs()
    source_frames_count: int = v2p_instance.frame_extract(
        user_input.colored_vid_input, "source_frames") or 0
    bw_frames_count: int = v2p_instance.frame_extract(
        user_input.bw_vid_input, "bw_frames") or 0

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

    # The loop length count will run up to the last frame of either the bw vid or the colored vid.
    # This is because we have no guarantee that both vids will have identical
    # number of frames.
    loop_len_count = source_frames_count if (
        source_frames_count < bw_frames_count) else bw_frames_count

    frame_names: List[tuple] = []

    for counter in range(loop_len_count + 1):

        num = str(counter)
        frame_name_3tuple = (f'bw_frames/' + num + ".png",
            f'source_frames/' + num + "_c.png",
            f'output_frames/' + num + "_f.png")

        frame_names.append(frame_name_3tuple)


    Colorizer.size_check(frame_names=frame_names)

    for frame in frame_names:
        print(f'{frame[0]} + {frame[1]}')
        final_output = Colorizer.color_blend(black_white=frame[0],
                                             colored= frame[1])
        final_output.save(frame[2])


    print("Creating video..")

    cblend_instance.png2mp4(user_input.bw_vid_input)

    print("Cleaning up extracted frames...")
    #shutil.rmtree('source_frames/')
    shutil.rmtree('bw_frames/')

    print("All done!")


if __name__ == "__main__":
    main()
