"""
Passport photo preparation tool. Requires a processed photo named "photo.jpg" of size 600x600 px.

Useful links:
- https://travel.state.gov/content/passports/en/passports/photos.html: photo cropping tool to create 600x600 px input image.
- https://www.xnview.com: correct levels, etc.
- https://stackoverflow.com/a/10649311/4143531: paste image into another image.
- https://stackoverflow.com/a/19303889/4143531: quality considerations.
- https://stackoverflow.com/a/9204506/4143531: possible usage of scikit-image.
"""
import argparse
import os

import numpy as np
from PIL import Image


def passport_photo(input_name, output_name=None, background_color=255, canvas_size=(1800 * 1.5, 1200 * 1.5),
                   start_left=10, start_top=10, tick_color=0, tick_len=30, offset=5,
                   output_format='JPEG', dpi=(300, 300), subsampling=0, quality=100):
    """The function creates a vertical 6x4" image file with two photos in it from the provided file with tick guides
    to allow easier cutting of the printed photo.

    :param input_name: the name of the input image file (should be of size 600x600 px).
    :param output_image: the name of output image file.
    :param background_color: the code of the background color (0=black, 255=white).
    :param canvas_size: the size of canvas (in pixels); (1800, 1200) - canvas of vertical orientation 6x4".
    :param start_left: the horizontal position on the canvas to place the photo at (in pixels).
    :param start_top: the vertical position on the canvas to place the photo at  (in pixels).
    :param tick_color: the color of the ticks (0=black, 255=white).
    :param tick_len: the length of the ticks (in pixels).
    :param offset: the offset of the ticks from the corners of the inserted photo (in pixels).
    :param output_format: the output format (e.g., JPEG).
    :param dpi: the DPI of the resulted image.
    :param subsampling: enable or disable subsampling (to change the quality of the resulted image).
    :param quality: image quality.
    :return: the output name of the file.
    """

    if not input_name:
        raise ValueError('Provide input file name')

    if not os.path.isfile(input_name):
        raise FileNotFoundError('The file "{}" cannot be found'.format(input_name))

    if not output_name:
        output_name = '{}_6x4in{}'.format(*os.path.splitext(os.path.basename(input_name)))

    format_codes = {
        'JPEG': 'RGB',
    }

    data = np.ones(canvas_size, dtype=np.uint32) * background_color
    photo = Image.open(input_name)

    photo_dim = photo.size
    required_dim = (600, 600)
    assert photo_dim == required_dim, 'Photo dimensions should be {}'.format(required_dim)

    start_tops = [start_top, 2 * start_top + photo_dim[0]]  # to produce 2 vertically arranged photos

    start_lefts = [start_left, 2 * start_left + photo_dim[1]]

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
    image = image.convert(format_codes[output_format])
    for start_left in start_lefts:
        for s in start_tops:
            image.paste(photo, (start_left, s))
    image.save(output_name, dpi=dpi, format=output_format, subsampling=subsampling, quality=quality)

    return output_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Passport photo preparation tool')

    # I/O options:
    parser.add_argument('-i', '--input-name', dest='input_name', default=None,
                        help='the name of the input image file (should be of size 600x600 px)')
    parser.add_argument('-o', '--output-name', dest='output_name', default=None, help='the name of output image file')

    # Colors/sizes:
    parser.add_argument('-b', '--background-color', dest='background_color', default=255,
                        help='the code of the background color (0=black, 255=white)')
    parser.add_argument('-s', '--canvas-size', dest='canvas_size', default=(int(1800 * 1.1), int(1200 * 1.1)),
                        help='the size of canvas (in pixels); (1800, 1200) - canvas of vertical orientation 6x4"')

    parser.add_argument('-l', '--start-left', dest='start_left', default=40,
                        help='the horizontal position on the canvas to place the photo at (in pixels)')

    parser.add_argument('-t', '--start-top', dest='start_top', default=150,
                        help='the vertical position on the canvas to place the photo at  (in pixels)')

    parser.add_argument('-c', '--tick-color', dest='tick_color', default=255,
                        help='the color of the ticks (0=black, 255=white)')
    parser.add_argument('--tick-len', dest='tick_len', default=30, help='the length of the ticks (in pixels)')
    parser.add_argument('--offset', dest='offset', default=50,
                        help='the offset of the ticks from the corners of the inserted photo (in pixels)')

    # Format/quality options:
    parser.add_argument('--output-format', dest='output_format', default='JPEG', help='the output format (e.g., JPEG)')
    parser.add_argument('--dpi', dest='dpi', default=(300, 300), help='the DPI of the resulted image')
    parser.add_argument('--quality', dest='quality', default=100, help='JPEG image quality')
    parser.add_argument('--subsampling', dest='subsampling', default=0,
                        help='enable or disable subsampling (to change the quality of the resulted image)')

    args = parser.parse_args()

    kwargs = vars(args)

    if not args.input_name:
        parser.error('Provide input file name')

    output_name = passport_photo(**kwargs)
    print('{} has been created'.format(output_name))
