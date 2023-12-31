import os
import random

from PIL import Image
from random import shuffle

# --------  SETTINGS  --------

output_dir = "output"
origin_dir = "assets"
background_name = "background.png"
count_of_objects = 8

max_rotation_angel = 90
min_rotation_angel = 0

padding = 50
padding_vertical = 200
padding_horizontal = 200
pixel_error_horizontal = 30
pixel_error_vertical = 30

# --------  EXECUTION  --------


def get_center_c(x, y, img, bg_img):
    x = x - int(img.width / 2)
    y = bg_img.height - y - int(img.height / 2)
    return (x, y)

# Getting all images names
objects_names_array = os.listdir(origin_dir)
objects_names_array.remove(background_name)
shuffle(objects_names_array)
# Saving from shuffled array only count of object
objects_names_array = objects_names_array[:count_of_objects]

# Opening the primary image (used in background)
background_img = Image.open(f"{origin_dir}/{background_name}")
bg_width, bg_height = background_img.size

offsets = []
rotations = []
names = []

print(bg_width)

size_of_zone_horizontal = (bg_width - 2 * padding_horizontal) / count_of_objects
size_of_zone_vertical = (bg_height - 2 * padding_vertical) / count_of_objects

base_x = [padding_horizontal + size_of_zone_horizontal * (idx + 0.5) for idx in range(count_of_objects)]
base_y = [padding_vertical + size_of_zone_vertical * (idx + 0.5) for idx in range(count_of_objects)]

print(base_x)

shuffle(base_x)
shuffle(base_y)

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)
for img_idx, img_name in enumerate(objects_names_array):
    img = Image.open(f"{origin_dir}/{img_name}").convert("RGBA")

    # Rotate image
    rotation_angel = random.randint(min_rotation_angel, max_rotation_angel)
    img = img.rotate(rotation_angel, expand=True)
    img_width, img_height = img.size

    # Finding coordinates
    new_x = int(base_x[img_idx] + random.randint(-pixel_error_horizontal, pixel_error_horizontal))
    new_y = int(base_y[img_idx] + random.randint(-pixel_error_vertical, pixel_error_vertical))

    background_img.paste(img, get_center_c(new_x, new_y, img, background_img), mask=img)

    offsets.append(get_center_c(new_x, new_y, img, background_img))
    rotations.append(rotation_angel)
    names.append(img_name)

# Displaying the image
background_img.show()

# Writing data
background_img.save(f"{output_dir}/outputPicture.png")
with open(f"{output_dir}/description.txt", 'w') as out:
    for img_idx in range(len(objects_names_array)):
        out.write(f"{offsets[img_idx]};{rotations[img_idx]};{names[img_idx]}\n")
