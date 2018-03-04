#!/usr/bin/env python


import argparse
from collections import Counter
from math import ceil
import os
from PIL import Image
from PIL import ImageChops
import re

class Combinator:
    def __init__(self, args, files):
        self.files = files
        self.significant_digits = len(str(len(files)))
        self.mode = args.mode
        self.determine_chop()
        self.outfile = args.outfile
        self.image = None

    def create_combination(self):
        for filename in self.files:
            newimage = Image.open(filename).convert('RGB')
            if self.image == None:
                self.image = newimage
                continue
            self.image = self.chop(self.image, newimage)

    def determine_chop(self):
        if self.mode == 'add':
            self.chop = ImageChops.add
        elif self.mode == 'blend':
            self.chop = lambda i1, i2: ImageChops.blend(i1, i2, 255)
        elif self.mode == 'darker':
            self.chop = ImageChops.darker
        elif self.mode == 'difference':
            self.chop = ImageChops.difference
        elif self.mode == 'lighter':
            self.chop = ImageChops.lighter
        elif self.mode == 'multiply':
            self.chop = ImageChops.multiply
        elif self.mode == 'screen':
            self.chop = ImageChops.screen
        elif self.mode == 'subtract':
            self.chop = ImageChops.subtract

    def save_combination(self):
        if self.outfile:
            filename = self.outfile
        else:
            filename = 'combination_{}.png'.format(self.mode)
        self.image.save(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regex', default='(image\d+\.png)', type=str, nargs='?',
            help='Regex for determining which files to take as input.')
    parser.add_argument('outfile', default='', type=str, nargs='?',
            help='Filename of combination image output.')
    parser.add_argument('-m', '--mode', default='difference', type=str, nargs='?',
            help='Channel operation to perform on images.')

    args = parser.parse_args()
    file_expr = re.compile(args.regex)
    files = [filename for filename in os.listdir() if file_expr.search(filename)]


    generator = Combinator(args, files)
    generator.create_combination()
    generator.save_combination()

if __name__ == '__main__':
    main()
