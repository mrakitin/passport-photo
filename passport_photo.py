"""
Passport photo preparation tool. Requires a processed photo named "photo.jpg" of size 600x600 px.

Useful links:
- https://travel.state.gov/content/passports/en/passports/photos.html: photo cropping tool to create 600x600 px input image.
- https://www.xnview.com: correct levels, etc.
- https://stackoverflow.com/a/10649311/4143531: paste image into another image.
- https://stackoverflow.com/a/19303889/4143531: quality considerations.
- https://stackoverflow.com/a/9204506/4143531: possible usage of scikit-image.
"""
import os

import numpy as np
from PIL import Image


def passport_photo(input_name='photo.jpg', output_name=None, background_color=255, canvas_size=(1800, 1200),
                   start_left=300, start_top=200, tick_len=30, tick_color=0, offset=5,
                   output_format='RGB', dpi=(300, 300), subsampling=0, quality=100):
    """The function creates a vertical 6x4" image file with two photos in it from the provided file with tick guides
    to allow easier cutting of the printed photo.

    :param input_name: the name of the input image file (should be of size 600x600 px).
    :param output_image: the name of output image file.
    :param background_color: the code of the background color (0=black, 255=white).
    :param canvas_size: the size of canvas (in pixels); (1800, 1200) - canvas of vertical orientation 6x4".
    :param start_left: the horizontal position on the canvas to place the photo at (in pixels).
    :param start_top: the vertical position on the canvas to place the photo at  (in pixels).
    :param tick_len: the length of the ticks (in pixels).
    :param tick_color: the color of the ticks (0=black, 255=white).
    :param offset: the offset of the ticks from the corner of the inserted photo (in pixels).
    :param output_format: the output format (RGB for JPEG).
    :param dpi: the DPI of the resulted image.
    :param subsampling: enable or disable subsampling (to change the quality of the resulted image).
    :param quality: JPEG quality.
    :return: the output name of the file.
    """

    if not os.path.isfile(input_name):
        raise FileNotFoundError('The file "{}" cannot be found'.format(input_name))

    if not output_name:
        name, ext = os.path.splitext(input_name)
        output_name = '{}_6x4in{}'.format(name, ext)

    data = np.ones(canvas_size, dtype=np.uint32) * background_color
    photo = Image.open(input_name)

    photo_dim = photo.size
    required_dim = (600, 600)
    assert photo_dim == required_dim, 'Photo dimensions should be {}'.format(required_dim)

    start_tops = [start_top, 2 * start_top + photo_dim[0]]  # to produce 2 vertically arranged photos

    for start_top in start_tops:
        # Vertical ticks:
        data[start_top - tick_len - offset: start_top - offset,
        start_left] = tick_color
        data[start_top - tick_len - offset: start_top - offset,
        start_left + photo_dim[1]] = tick_color
        data[(start_top + photo_dim[0]) + offset: (start_top + photo_dim[0]) + offset + tick_len,
        start_left] = tick_color
        data[(start_top + photo_dim[0]) + offset: (start_top + photo_dim[0]) + offset + tick_len,
        start_left + photo_dim[1]] = tick_color

        # Horizontal ticks:
        data[start_top,
        start_left - tick_len - offset:start_left - offset] = tick_color
        data[start_top + photo_dim[0],
        start_left - tick_len - offset:start_left - offset] = tick_color
        data[start_top,
        (start_left + photo_dim[1] + offset): (start_left + photo_dim[1] + offset) + tick_len] = tick_color
        data[start_top + photo_dim[0],
        (start_left + photo_dim[1] + offset): (start_left + photo_dim[1] + offset) + tick_len] = tick_color

    image = Image.fromarray(data)
    # image = image.convert(output_format)
    image = image.convert(output_format)
    for s in start_tops:
        image.paste(photo, (start_left, s))
    image.save(output_name, dpi=dpi, subsampling=subsampling, quality=quality)

    return output_name


if __name__ == '__main__':
    passport_photo(input_name='photo.jpg')
