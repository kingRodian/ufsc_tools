#!/usr/bin/env python

import argparse
import os
from PIL import Image
import random



class Exploder:
    def __init__(self, args):
        self.infile = args.infile
        self.outprefix = args.outprefix
        self.width = args.width
        self.height = args.height
        # This is for random pixel noise
        self.rand_population = [0, 1, 2, 3]
        self.rand_weights = [90, 7, 2, 1]

    def create_tmpdir(self):
        s = 'tmpdir'
        while s in os.listdir():
            # Create random string for tmp dir name
            s = ''.join( [ chr(random.randint(41, 126)) for _ in range(10)  ] )
        s = './' + s
        os.mkdir(s)
        self.tmpdir = s

    def clamp(self, value):
        return max(min(value, 255), 0)

    def create_noise(self, img):
        # This should really be rewritten, very slow
        rand_num = random.choices(self.rand_population, self.rand_weights)[0]
        for _ in range(rand_num):
            pos = tuple((random.randrange(0, img.width), random.randrange(0, img.height)))
            op = random.randint(0, 1) # Add or subtract
            factor = random.random()
            if op == 0:
                factor += 1
            else:
                factor -= 1;
            color = img.getpixel((0,0))
            new_color = tuple((self.clamp(int(color[i] * factor)) for i in range(3)))
            img.putpixel(pos, new_color)


    def create_images(self):
        try:
            img = Image.open(self.infile)
        except IOError:
            print('Could not open file: {}'.format(infile))
            exit()
        img = img.convert('RGB')
        data = list(img.getdata())
        digits = len(str(len(data)))
        self.digits = digits
        pix_num = self.width * self.height
        for i, pixel in enumerate(data):
            new_img = Image.new('RGB', (self.width, self.height), pixel)
            self.create_noise(new_img)
            number = str(i).zfill(digits)
            filename = self.outprefix + number + '.png'
            new_img.save(self.tmpdir + '/' + filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
            help='Image file to convert.')
    parser.add_argument('-p', '--outprefix', type=str, default='image',
            help='Prefix for output images.')
    parser.add_argument('-x', '--width', type=int, default=50,
            help='Width of output images.')
    parser.add_argument('-y', '--height', type=int, default=50,
            help='Height of output image.')
    parser.add_argument
    args = parser.parse_args()

    exploder = Exploder(args)
    exploder.create_tmpdir()
    exploder.create_images()


if __name__ == '__main__':
    main()
