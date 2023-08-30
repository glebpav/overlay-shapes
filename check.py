import os
import random

from PIL import Image
from random import shuffle


def get_center_c(x, y, img, bg_img):
    x = x - int(img.width / 2)
    y = bg_img.height - y - int(img.height / 2)
    return (x, y)

# --------  SETTINGS  --------

output_dir = "output"
origin_dir = "assets"
background_name = "background.png"
count_of_objects = 8

max_rotation_angel = 90
min_rotation_angel = 0

padding = 50
padding_vertical = 150
padding_horizontal = 200
pixel_error_horizontal = 30
pixel_error_vertical = 30

# --------  EXECUTION  --------

# Getting all images names
objects_names_array = os.listdir(origin_dir)
objects_names_array.remove(background_name)
shuffle(objects_names_array)
# Saving from shuffled array only count of object
objects_names_array = objects_names_array[:count_of_objects]

# Opening the primary image (used in background)
background_img = Image.open(f"{origin_dir}/{background_name}")
bg_width, bg_height = background_img.size

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)

img = Image.open(f"{origin_dir}/a.png").convert("RGBA")
img_r = img.rotate(30, expand=True)
y = 0
x = 0

background_img.paste(img, get_center_c(x, y, img, background_img), mask=img)
background_img.paste(img_r, get_center_c(x, y, img_r, background_img), mask=img_r)

# Displaying the image
background_img.show()
