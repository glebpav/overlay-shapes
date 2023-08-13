import os
import random

from PIL import Image
from random import shuffle

# --------  SETTINGS  --------

output_dir = "output"
origin_dir = "assets"
background_name = "background.png"
count_of_objects = 9

max_rotation_angel = 90
min_rotation_angel = 0

padding = 50

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

offsets = []
rotations = []
names = []

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)
for img_name in objects_names_array:
    img = Image.open(f"{origin_dir}/{img_name}").convert("RGBA")
    img_width, img_height = img.size

    # Rotate image
    rotation_angel = random.randint(min_rotation_angel, max_rotation_angel)
    img = img.rotate(rotation_angel, expand=True)

    # Finding coordinates
    new_x = random.randint(padding, bg_width - padding - img_width)
    new_y = random.randint(padding, bg_height - padding - img_height)

    background_img.paste(img, (new_x, new_y), mask=img)

    offsets.append((new_x, new_y))
    rotations.append(rotation_angel)
    names.append(img_name)

# Displaying the image
background_img.show()

# Writing data
background_img.save(f"{output_dir}/output.png")
with open(f"{output_dir}/map.txt", 'w') as out:
    for img_idx in range(len(objects_names_array)):
        out.write(f"{offsets[img_idx]};{rotations[img_idx]};{names[img_idx]}\n")