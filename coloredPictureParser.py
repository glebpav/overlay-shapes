import pandas as pd
from PIL import Image
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

# defined colors

purple_color = ((163, 73, 164), "purple")
orange_color = ((255, 201, 14), "orange")
brown_color = ((136, 0, 21), "brown")
lime_color = ((181, 230, 29), "lime")
blue_color = ((0, 162, 232), "blue")
cabbage_color = ((255, 127, 39), "cabbage")
green_color = ((34, 177, 76), "green")
yellow_color = ((255, 242, 0), "yellow")
pepper_color = ((255, 174, 201), "pepper")
carrot_color = ((200, 191, 231), "carrot")

# defined settings

output_dir = "output"
output_format = 2

# execution

im = Image.open('output/coloredOutputPicture.png').convert("RGB")  # Can be many different formats.
pix = im.load()

colors = []
colors_palet = {purple_color, orange_color, brown_color, lime_color,
                blue_color, carrot_color, green_color, yellow_color,
                cabbage_color, pepper_color}
output_matrix = np.zeros(im.size)

for x in range(im.size[0]):
    for y in range(im.size[1]):
        colors.append(pix[x, y])
        for color_idx, colors_rgb in enumerate(colors_palet):
            if colors_rgb[0] == pix[x, y]:
                output_matrix[x, y] = color_idx
                break
        else:
            pix[x, y] = (0, 0, 0)

im.save(f"{output_dir}/modified_im.png")

if output_format == 0:
    df = pd.DataFrame(data=output_matrix.astype(int))
    df.to_csv(f"{output_dir}/colorMap.csv", sep=' ', header=False, index=False)
elif output_format == 1:
    with open(f"{output_dir}/colorMap.txt", 'w') as out:
        out.write('{')
        for line in output_matrix:
            out.write(str(line).replace('[', '{').replace(']', '},').replace('.', ',').replace(' ', '').replace('\n', '') + '\n')
        out.write('}')
else:
    pass

with open(f"{output_dir}/colorMapDescription.txt", 'w') as out:
    for color_idx, color in enumerate(colors_palet):
        out.write(f"{color_idx + 1};{color[1]};{color[0]}\n")
