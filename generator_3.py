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


def get_center_c(x, y, img_origin, img_background):
    x = x - int(img_origin.width / 2)
    y = img_background.height - y - int(img_origin.height / 2)
    return (x, y)


# Getting all images names
print(f"{origin_dir}/{background_name}")
objects_names_array = os.listdir(f"{origin_dir}/shapes")
shuffle(objects_names_array)
# Saving from shuffled array only count of object
objects_names_array = objects_names_array[:count_of_objects]

# Opening the primary image (used in background)
background_img = Image.open(f"{origin_dir}/{background_name}")
colored_background_img = Image.new(mode="RGBA", size=background_img.size).convert("RGB")
color_map_img = Image.new(mode="RGBA", size=background_img.size).convert("RGB")
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
pix_map = color_map_img.load()
pix_background = colored_background_img.load()
used_colores = []

for img_idx, img_name in enumerate(objects_names_array):
    img = Image.open(f"{origin_dir}/shapes/{img_name}").convert("RGBA")
    img_colored = Image.open(f"{origin_dir}/colored_shapes/{img_name.replace('.png', '')}_colored.png").convert("RGBA")

    # Rotate image
    rotation_angel = random.randint(min_rotation_angel, max_rotation_angel)
    img = img.rotate(rotation_angel, expand=True)
    img_colored = img_colored.rotate(rotation_angel, expand=True)
    img_width, img_height = img.size

    # Finding coordinates
    new_x = int(base_x[img_idx] + random.randint(-pixel_error_horizontal, pixel_error_horizontal))
    new_y = int(base_y[img_idx] + random.randint(-pixel_error_vertical, pixel_error_vertical))

    background_img.paste(img, get_center_c(new_x, new_y, img, background_img), mask=img)
    colored_background_img.paste(img_colored, get_center_c(new_x, new_y, img_colored, colored_background_img), mask=img_colored)

    new_colors = []
    for x in range(background_img.size[0]):
        for y in range(background_img.size[1]):
            color_background = pix_background[x, y]
            color_map = pix_map[x, y]

            if color_map == (0, 0, 0):
                pix_map[x, y] = color_background
                if color_background not in new_colors and color_background not in used_colores:
                    new_colors.append(color_background)
            elif color_background in new_colors:
                pix_map[x, y] = (255, 255, 255)

    used_colores += new_colors
    offsets.append(get_center_c(new_x, new_y, img, background_img))
    rotations.append(rotation_angel)
    names.append(img_name)

# Displaying the image
# background_img.show()

for x in range(background_img.size[0]):
    for y in range(background_img.size[1]):
        color_map = pix_map[x, y]
        if color_map == (255, 255, 255):
            pix_map[x, y] = (0, 0, 0)

# Writing data
background_img.save(f"{output_dir}/outputPicture.png")
color_map_img.save(f"{output_dir}/colorMap.png")
# colored_background_img.save(f"{output_dir}/coloredMap.png")

with open(f"{output_dir}/description.txt", 'w') as out:
    for img_idx in range(len(objects_names_array)):
        out.write(f"{offsets[img_idx]};{rotations[img_idx]};{names[img_idx]}\n")
