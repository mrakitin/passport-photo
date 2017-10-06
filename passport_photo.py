"""
Passport photo preparation tool. Requires a processed photo named "photo.jpg" of size 600x600 px.

Useful links:
- https://travel.state.gov/content/passports/en/passports/photos.html: photo cropping tool to create 600x600 px input image.
- https://www.xnview.com: correct levels, etc.
- https://stackoverflow.com/a/10649311/4143531: paste image into another image.
- https://stackoverflow.com/a/9204506/4143531: possible usage of scikit-image
"""

import numpy as np
from PIL import Image

data = np.ones((1800, 1200), dtype=np.uint32) * 255  # white canvas of vertical orientation 6x4"
photo = Image.open("photo.jpg")

photo_dim = photo.size  # (600, 600)
required_dim = (600, 600)
assert photo_dim == required_dim, 'Photo dimensions should be {}'.format(required_dim)

start_left = 300
start_top = 200

tick_len = 30
tick_color = 200  # gray

offset = 5

start_tops = [start_top, 2 * start_top + photo_dim[0]]

for start_top in start_tops:
    data[start_top - tick_len - offset: start_top - offset,
    start_left] = tick_color
    data[start_top - tick_len - offset: start_top - offset,
    start_left + photo_dim[1]] = tick_color
    data[(start_top + photo_dim[0]) + offset: (start_top + photo_dim[0]) + offset + tick_len,
    start_left] = tick_color
    data[(start_top + photo_dim[0]) + offset: (start_top + photo_dim[0]) + offset + tick_len,
    start_left + photo_dim[1]] = tick_color

    data[start_top,
    start_left - tick_len - offset:start_left - offset] = tick_color
    data[start_top + photo_dim[0],
    start_left - tick_len - offset:start_left - offset] = tick_color
    data[start_top,
    (start_left + photo_dim[1] + offset): (start_left + photo_dim[1] + offset) + tick_len] = tick_color
    data[start_top + photo_dim[0],
    (start_left + photo_dim[1] + offset): (start_left + photo_dim[1] + offset) + tick_len] = tick_color

# Get bits per point:
# mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'I;16': 16, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}

image = Image.fromarray(data)
image = image.convert('RGB')
for s in start_tops:
    image.paste(photo, (start_left, s))
image.save('result.jpg')
