# Image to Dice
This script will take an image(.png, .jpg, or .jpeg) as an input and recreate it using different sides of a die. Will also spit out the instructions for recreating it with physical dice if uisng flag --s.

## Install Guide
### Prereqs
- Install OpenCV either by binary at: ```https://opencv.org/``` or by using pip: ```python3 pip install opencv-python```
- Install Pillow either by binary at: ```https://pillow.readthedocs.io/en/stable/installation.html``` or by using pip: ```python3 pip install Pillow```
- Install Click by using pip: ```python3 pip install click```
- Install TQDM either at: ```https://github.com/tqdm/tqdm``` or by using pip: ```python3 pip install tqdm```

### Installation
Clone this repository with: ```https://github.com/BenRemer/Image_to_dice.git```

## Usage

### Running the bot
- Using terminal move to where it was downloaded and run: ```./Dice.py```
	- If on windows run: ```python3 Dice.py```
- Type ```python3 Dice.py --help``` to see all the flags

### Flags
- ```--b``` with an integer to set how many pixels is in each block to turn into a die. Default to 7
- ```--i``` with a string of the file location, if none provided a prompt will display
- ```--o``` with a string to name the output file, defaults to finished.png
- ```--s``` will show block size, length, width, and height of finished picture and makes a file for buiilding yourself, defaults to false
- ```--help``` will show the flags and exit
