#!/usr/bin/env python

"""
makecomposite.py
Given a folder of png images with filenames consisting of a number + .png, this program
creates a composite image of the images.
The frames will be placed into rows of cells, resized to a size of cellwidth x cellheight,
the amount of cells in a row given by the width argument.
If the amount of frames isnt a multiple of the width, the remaining empty pixels in the last row will simply be black.

"""

import argparse
from math import ceil
import os
from PIL import Image

class CompositeGenerator:
    def __init__(self, args, files, mode='RGB'):
        self.width = args.width
        self.height = ceil(len(files) / self.width)
        self.cellsize = self.cellwidth, self.cellheight = args.cellwidth, args.cellheight
        self.totalsize = self.totalwidth, self.totalheight = self.width * self.cellwidth, self.height * self.cellheight
        self.files = files
        self.mode = mode
        self.outfile = args.outfile
        self.composite = Image.new(self.mode, self.totalsize)

    def create_composite(self):
        for i, filename in enumerate(self.files):
            image = Image.open(filename).convert(self.mode)
            image = image.resize(self.cellsize)
            cellpos = (i % self.width, i // self.width)
            box = (cellpos[0] * self.cellwidth, cellpos[1] * self.cellheight,
                    (cellpos[0] + 1) * self.cellwidth, (cellpos[1] + 1) * self.cellheight)
            self.composite.paste(image, box)

    def save_composite(self):
        if self.outfile:
            filename = self.outfile
        else:
            filename = 'composite_{}x{}.png'.format(self.width, self.height)
        self.composite.save(filename)


def checkfilename(filename):
    if '.png' not in filename:
        return False
    dotindex = filename.find('.')
    try:
        number = int(filename[:dotindex])
    except ValueError:
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int,
            help='Width of composite')
    parser.add_argument('-cw', '--cellwidth', default=1, type=int, nargs='?',
            help='The width to shrink each individual image down to.')
    parser.add_argument('-ch', '--cellheight', default=1, type=int, nargs='?',
            help='The height to shrink each individual image down to.')
    parser.add_argument('outfile', default='', type=str, nargs='?',
            help='Filename of composite image output.')

    args = parser.parse_args()
    files = [filename for filename in os.listdir() if checkfilename(filename)]


    generator = CompositeGenerator(args, files)
    generator.create_composite()
    generator.save_composite()

if __name__ == '__main__':
    main()
