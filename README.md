# Chroma Blend

A workaround to DeepRemaster's low resolution limitation.

Since Satoshi Iizuka's DeepRemaster functions well only with small videos (432 x 320), a solution for coloring higher resolution videos is to extract the chroma from the small video and layer it over the larger-sized black and white video.

The program takes two inputs: The original black and white mp4, and the colored mp4 output from DeepRemaster. The output is a folder of all the video frames, with the color transferred over to the original black and white frames.

This illustrates what the program does for each frame.

<img src="https://i.imgur.com/Euuqf5K.gif" width="480" height="270">

Demonstration :
[![](http://img.youtube.com/vi/zv7PUKbj3yM/0.jpg)](http://www.youtube.com/watch?v=zv7PUKbj3yM "")

## Installation

Download the repository:

```bash
git clone https://github.com/JohannSuarez/chroma_blend.git
```

Once inside the chroma_blend directory, install the required dependencies:
```bash
pip install -r requirements.txt
```
You're good to go!

## Usage

```bash
python3 chroma_blend.py [black_and_white.mp4] [colorized.mp4]
```

Since this program as a whole relies on two smaller modules, the modules themselves can be used as standalone programs.
The modules located in the "cblend_modules" directory are:

**colorizer.py** - For colorizing the frames.

```bash
python3 colorizer.py [bw_image] [colorized_image]
```


**vid2pngs.py** - For splitting videos into pngs. A directory is created for the output pngs.

```bash
python3 vid2pngs.py [input_video]
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
