#!/usr/bin/env python

"""
This program generates 2 images from one, using the (2,2) visual crypto sharing method.
Each pixel in the original image is examined, and become two 2x2 quads in the 2 new images.
If a pixel is white, the two quads will be identical in the two shares.
If a pixel is black, the two quads will be complements of eachother.
This makes it so that the image cannot be decyphered with only one share, but when combined, the two will
form a noisier version of the original image.
"""



import argparse
import os
from PIL import Image
import random
import sys



# These are the possible quads a pixel could be turned into, with the complement of an element
# being the amount of elements - 1 (6 - 1) - the index of the quad, i.e, the inverse of [4] being 5 - 4 = 1
quads = [[1,1,0,0], [1,0,1,0], [1,0,0,1], [0,1,1,0], [0,1,0,1], [0,0,1,1]]
# We then generate the corresponding images from these
quad_imgs = []
for quad in quads:
    quad_img = Image.new('1', (2,2))
    quad_img.putdata(quad)
    quad_imgs.append(quad_img)

# Returns 2 quad_images based on the color(0 or 1), complement or identical
def get_quads(color):
    i = random.randrange(0, len(quad_imgs))
    if color:
        return quad_imgs[i], quad_imgs[i]
    else:
        return quad_imgs[i], quad_imgs[5 - i]



def encrypt_image(infile):
    base = Image.open(infile).convert('1')
    filename = infile[: infile.find('.')]

    # New images will be 4x the size
    new_width = base.width * 2
    new_height = base.height * 2

    img_A = Image.new('1', (new_width, new_height))
    img_B = Image.new('1', (new_width, new_height))

    # pixels = base.getdata() <-- Unfortunately this does not work?
    for y in range(base.height):
        for x in range(base.width):
            paste_y = y * 2
            paste_x = x * 2
            pixel = base.getpixel((x, y))
            A_quad, B_quad = get_quads(pixel)
            img_A.paste(A_quad, (paste_x, paste_y))
            img_B.paste(B_quad, (paste_x, paste_y))

    img_A.save('{}_A.png'.format(filename))
    img_B.save('{}_B.png'.format(filename))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
            help='Image file to encrypt.')

    args = parser.parse_args()

    if args.infile not in os.listdir():
        print('ERROR: {} not a valid file.'.format(args.infile), file=sys.stderr)
        exit()

    encrypt_image(args.infile)


if __name__ == '__main__':
    main()
