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

  
    def size_check(self, frame_names: List[tuple] ) -> None:
        '''
        Check an image sample from both bw_frames and source_frames. 
        We can do this by grabbing the first element of frame_names.

        If the two image samples are the same size, use size_corrector 
        on the entirety of either the bw_frames or the color_frames 
        depending on which of them needs to be upsized.
        '''
        
        print(frame_names[0][0][0])
        print(frame_names[0][0][1])

        bw_image = Image.open(frame_names[0][0][0]) # Black and white 
        remastered_image = Image.open(frame_names[0][0][1]) # Colored

        # Variables to perform size consistency check
        bw_w, bw_h = bw_image.size
        cl_w, cl_h = remastered_image.size

        if(bw_w - cl_w != 0) or (bw_h - cl_h != 0):
            print("Video pair are different sizes. Correcting frames..")

            # It's here that you have to asynchronously resize either the 
            # entirety of the bw frames or the colored frames.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # What do you need to pass into size_corrector?
                # Well, what does the size_corrector do?
                # Resize chroma, to make it as big as the luma.
                # So what does size_corrector need?
                # A list of all the chroma frames, and the proper height/width for them.

                # Let chroma_obj be a dictionary that contains a list
                # of all the chroma frames in string form, and two other 
                # key-pair values for the height and width dimensions.
                # This way you don't have to fumble with passing multiple 
                # arguments with the map function.
                chroma_obj =
                executor.map(self.size_corrector, chroma_obj)


    def size_corrector(self, width: int, height: int, image):
        ''' 
        A size corrector. The chroma image is expected to be smaller than the luma image.
        If so, the dimensions must be matched to the luma image prior to any other operation.
        ''' 
        new_image = image.resize((width, height))
        return new_image

    def append_id(self, filename: str) -> str:
        '''
        Formatting the name of the output file.
        '''

        dot_index = filename.find(".")
        return filename[:dot_index] + '_f' + filename[dot_index:]


    def color_blend(self, black_white, colored):
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

        # Variables to perform size consistency check
        '''
        bw_w, bw_h = bw_image.size
        cl_w, cl_h = remastered_image.size

        if(bw_w - cl_w != 0) or (bw_h - cl_h != 0):
            print("Image pair are different sizes, correcting...")
            remastered_image = remastered_image.resize((bw_w, bw_h))
        '''

        # Construct RGB version of both b&w image and the chroma image. Needed to
        # Seamlessly convert to hsv.
        bw_image_rgb = bw_image.convert('RGB')
        remastered_image_rgb = remastered_image.convert('RGB')

        # numpy array
        bw_image_rgb = np.array(bw_image_rgb)
        remastered_image_rgb = np.array(remastered_image_rgb)

        # Convert both the input image and color mask to Hue Saturation Value
        # (HSV) colorspace
        img_hsv = color.rgb2hsv(bw_image_rgb)

        # Color mask is THE colored(remastered) version.
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
            self.append_id(black_white)[10:] +
            BColors.ENDC)
        return final


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
    result.save(colorizer_instance.append_id(user_input.bw_input))

# If this .py were used as a module, main wouldn't execute.
if __name__ == "__main__":
    main()
