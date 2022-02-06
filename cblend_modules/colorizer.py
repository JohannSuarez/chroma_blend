'''
The module that colors frames.
Color data is grabbed from low-res picture.
Then blended over the low-res black and white picture.
'''

import argparse
import concurrent.futures
import numpy as np
from PIL import Image, ImageEnhance
from skimage import color
from typing import List
from timeit import default_timer as timer


class BColors:
    '''
    Color constants. This should be moved elsewhere.
    '''
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


class Colorizer:

    def __init__(self) -> None:
        pass

    @staticmethod
    def size_check(frame_names: List[tuple] ) -> None:
        '''
        Check an image sample from both bw_frames and source_frames.
        We can do this by grabbing the first element of frame_names.

        If the two image samples are the same size, use size_corrector
        on the entirety of either the bw_frames or the color_frames
        depending on which of them needs to be upsized.
        '''
        # Each frame has three names; the bw, the colored, and the remastered.

        bw_image = Image.open(frame_names[0][0]) # Black and white name of first frame.
        remastered_image = Image.open(frame_names[0][1]) # Remastered name of first frame.

        # Variables to perform size consistency check
        bw_w, bw_h = bw_image.size
        cl_w, cl_h = remastered_image.size

        if(bw_w - cl_w != 0) or (bw_h - cl_h != 0):
            print("Video pair are different sizes. Correcting frames..")

            # Grab a list of all the source frames. 
            # Resize all source frames into the black-and-white films dimensions.
            # This can be done asynchronously.
            all_source_frames = [name[1] for name in frame_names]
            adjusted_size_corrector = lambda input: Colorizer.size_corrector(width=bw_w, height=bw_h, image=input)

            start = timer()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(adjusted_size_corrector, all_source_frames)

            end = timer()

            print(end-start)

    @staticmethod
    def size_corrector(width: int, height: int, image):
        '''
        A size corrector. The chroma image is expected to be smaller than the luma image.
        If so, the dimensions must be matched to the luma image prior to any other operation.
        Chroma image will be resized, and saved to disk.
        '''
        print(f'Size corrector invoked on {image}')
        source_image = Image.open(image)
        new_image = source_image.resize((width, height))
        new_image.save(image);

    @staticmethod
    def append_id(filename: str) -> str:
        '''
        Formatting the name of the output file.
        '''
        dot_index = filename.find(".")
        return filename[:dot_index] + '_f' + filename[dot_index:]


    @staticmethod
    def color_blend(black_white, colored):
        '''
        Parameter requirements for color_blend:
        [Assumed this is being run as a module for batch tasks]

        Black and white image has to be in number sequence. Ex: (0001.jpg, 0002.jpg)
        Colored image has to match its respective B & W image's name, but with "_c" appended.
        Ex: (0001_c.jpg, 0002_c.jpg)
        Output name should be a formatted string; the number sequence appended by "_f" for final.
        Ex: (0001_f.png, 0002_f.png)
        '''

        bw_image = Image.open(black_white)
        remastered_image = Image.open(colored)

        # Construct RGB version of both b&w image and the chroma image. Needed to
        # Seamlessly convert to hsv.
        bw_image_rgb = bw_image.convert('RGB')
        remastered_image_rgb = remastered_image.convert('RGB')

        bw_image_rgb = np.array(bw_image_rgb)
        remastered_image_rgb = np.array(remastered_image_rgb)

        # Convert both the input image and color mask to Hue Saturation Value
        # (HSV) colorspace
        img_hsv = color.rgb2hsv(bw_image_rgb)

        # Color mask is THE colored (remastered) version.
        color_mask_hsv = color.rgb2hsv(remastered_image_rgb)

        # Replacing the hue and saturation of the black and white image with
        # values from color mask
        img_hsv[..., 0] = color_mask_hsv[..., 0]
        img_hsv[..., 1] = color_mask_hsv[..., 1]
        img_masked = color.hsv2rgb(img_hsv)

        # Converting numpy image to format recognized by PIL
        final = Image.fromarray((img_masked * 255).astype(np.uint8))

        brightener = ImageEnhance.Brightness(final)
        final = brightener.enhance(1.15)

        print(
            BColors.OKGREEN +
            "Color blend success! " +
            "Generated " +
            BColors.YELLOW +
            Colorizer.append_id(black_white)[10:] +
            BColors.ENDC)
        return final


    @staticmethod
    def fu():
        print("Make me!!")

def main ():
    '''
    Main function of the module.
    '''

    print(BColors.OKBLUE + "Main activated." + BColors.ENDC)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bw_input",
        help="The black and white input to blend colors on.")
    parser.add_argument(
        "colored_input",
        help="The image with the chroma that you want to blend the b&w image's luma on.")
    user_input = parser.parse_args()

    colorizer_instance = Colorizer()

    result = colorizer_instance.color_blend(user_input.bw_input, user_input.colored_input)
    result.save(Colorizer.append_id(user_input.bw_input))

# If this .py were used as a module, main should not execute.
if __name__ == "__main__":
    main()
