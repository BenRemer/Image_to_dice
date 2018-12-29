import numpy as np
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from PIL import Image
import math
import glob
import os
import warnings
import click
from tqdm import trange



def get_dice_images():
    path_to_dice_pictures = './dice_pictures/'
    full_path = os.path.realpath(path_to_dice_pictures)
    # print("Path: ", full_path)
    dice_paths = {} # list of die locations, get as dice_paths[dice_#][0]
    for filename in glob.glob(full_path + '/*.png'): 
        # im=Image.open(filename)
        # dice_paths.append(im)
        filename = os.path.splitext(os.path.basename(filename))[0]
        # print(filename)
        dice_paths[filename] = glob.glob(full_path + '/' + filename + '*.png')
    return dice_paths

def get_selected_image():
    selected_picture_path = "none.txt"
    while not selected_picture_path.lower().endswith(('.png', '.jpg', '.jpeg')): # while correct image is not chosen
        print("Please choose the file:")
        time.sleep(1)
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        selected_picture_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print("Selected path: ", selected_picture_path)
        if selected_picture_path == "":
            print("Cancelled")
            return 'none'
        if not selected_picture_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("Incorrect filetype, please choose a different picture:")
            time.sleep(1)
    return selected_picture_path

def write_to_file(array, new_width):
    f = open("dice_list.txt", "w")
    count = 0
    for die in array:
        if count == new_width:
            f.write('\n')
            count = 0
        f.write(die)
        count += 1


@click.command()
@click.option('--block_size', '--b', default=7, help='Size of the blocksize, default of 7')
@click.option('--input_file', '--i', help='File to select, if none selected will prompt for file')
@click.option('--output_file', '--o', default="finished.png", help='Name of output file, defaults to finished.png')
@click.option('--show_info', '--s', is_flag=True, default=False, help='Flag to see if info will be shown, default to flase')

def convert_image(block_size, input_file, output_file, show_info):
    if input_file:
        selected_picture_path = input_file
    else:
        selected_picture_path = get_selected_image()
    if not selected_picture_path:
        return

    dice_paths = get_dice_images()
    if show_info:
        print("Block size: " + str(block_size))

    image_normal = cv2.imread(selected_picture_path) # read image
    image_gray = cv2.cvtColor(image_normal, cv2.COLOR_BGR2GRAY) #convert to grayscale
    WIDTH, HEIGHT = image_gray.shape
    # turn array to np array
    image_gray = np.array(image_gray)
    # grab height and width of reduced image
    new_height, new_width =int(math.ceil(HEIGHT / block_size)), int(math.ceil(WIDTH / block_size))
    # fill new array with zeros
    np_arr = np.zeros((new_height, new_width))
    for j in range(new_height):
        for i in range(new_width):
            y_low = j * block_size 
            y_high = (j + 1) * block_size
            x_low = i * block_size 
            x_high = (i + 1) * block_size
            # gets rid of pesky warning for nan mean
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                np_arr[j][i] = np.mean(image_gray[y_low:y_high, x_low:x_high])  
    # print("Array", np_arr)
    if show_info:
        print("Length:", len(np_arr), " Width:", new_width, " Height:", new_height)
    # show pixelated image
    # plt.imshow(np_arr, cmap='gray')
    # plt.show()
    dice_images = {}
    for i in range(6):
        image = cv2.imread(dice_paths['die_' + str(i + 1)][0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
        # cv2.imshow('image',image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # np_die = np.array(image)
        # print(np_die)
        dice_images['die_' + str(i + 1)] = image
    # print(dice_images['die_6'])
    dice_image_height, dice_image_width = dice_images['die_1'].shape
    # print("Die height:", dice_image_height, " Die width:", dice_image_width)
    # plt.imshow(dice_images['die_1'], cmap='gray')
    # plt.show()
    die_fit_6 = (0, 42.5)
    die_fit_5 = (42.5, 85)
    die_fit_4 = (85, 127.5)
    die_fit_3 = (127.5, 170)
    die_fit_2 = (170, 212.5)
    die_fit_1 = (212.5, 255)
    new_die_height, new_die_width = int(math.ceil(new_height * dice_image_height)), int(math.ceil(new_width * dice_image_width))
    # print("new width, new height", new_die_height, new_die_width)
    die_arr = np.zeros((new_die_height, new_die_width))
    dice_count = 0
    build_list = []

    with trange(new_height) as t:
        for j in t:
            for i in range(new_width):
                average = np_arr[j][i]
                dice_count += 1
                if average < die_fit_6[1]:
                    die_to_place = dice_images['die_6']
                    build_list.append("6")
                elif average < die_fit_5[1]:
                    die_to_place = dice_images['die_5']
                    build_list.append("5")
                elif average < die_fit_4[1]:
                    die_to_place = dice_images['die_4']
                    build_list.append("4")
                elif average < die_fit_3[1]:
                    die_to_place = dice_images['die_3']
                    build_list.append("3")
                elif average < die_fit_2[1]:
                    die_to_place = dice_images['die_2']
                    build_list.append("2")
                else:
                    die_to_place = dice_images['die_1']
                    build_list.append("1")
                die_count_x = 0
                die_count_y = 0
                for k in range(j * dice_image_height, (j+1)*dice_image_height):
                    # print("j * new_height, (j+1)*new_height", j * new_height, (j+1)*new_height)
                    die_count_y = 0
                    for l in range(i * dice_image_width, (i + 1)*dice_image_width):
                        # print("l", l)
                        die_arr[k][l] = die_to_place[die_count_x][die_count_y]
                        die_count_y += 1
                        # print(die_arr[k][l])
                    die_count_x += 1
    cv2.imwrite(output_file, die_arr)
    if show_info:
        print("Takes " + str(len(build_list)) + " dice to build")
        print("File saved as " + output_file + ' to ' + os.getcwd())
        write_to_file(build_list, new_width)
    return build_list


# def main():
#     # block_size = int(input("What is the block size: "))

#     # Show all the dice
#     # for i in range(6):
#     #     cv2.imshow('die' + str(i + 1), cv2.imread(dice_paths['die_' + str(i + 1)][0]))
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()

#     # selected_picture_path = get_selected_image()

#     # if not selected_picture_path:
#     #     return

#     build_list = convert_image()
#     print("File saved to " + os.getcwd() + " as finished.png\n")






if __name__ == "__main__":
    convert_image()
