#!/usr/bin/env python

import argparse
import ffmpeg
import os
from PIL import Image
import random


class VideoCreator:
    def __init__(self, args):
        self.infile = args.infile
        self.outfile = args.outfile
        self.outprefix = args.outprefix
        self.fps = args.fps
        self.width = args.width
        self.height = args.height
        self.tmpdir = self.create_tmpdir()
        self.create_images()
        self.create_video()

    def create_tmpdir(self):
        s = 'tmpdir'
        while s in os.listdir():
            # Create random string for tmp dir name
            s = ''.join( [ chr(random.randint(41, 126)) for _ in range(10)  ] )
        s = './' + s
        os.mkdir(s)
        return s

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
        for i, pixel in enumerate(data):
            new_img = Image.new('RGB', (self.width, self.height), pixel)
            number = str(i).zfill(digits)
            filename = self.outprefix + number + '.png'
            new_img.save(self.tmpdir + '/' + filename)

    def create_video(self):
        input_format = self.tmpdir + '/' + self.outprefix + '%0' + str(self.digits) + 'd.png'
        stream = ffmpeg.input(input_format)
        stream = ffmpeg.filter_(stream, 'fps', fps=self.fps, round='up')
        stream = ffmpeg.output(stream, self.outfile)
        ffmpeg.run(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
            help='Image file to convert.')
    parser.add_argument('-o', '--outfile', type=str, default='out.mp4',
            help='Name of output video.')
    parser.add_argument('-p', '--outprefix', type=str, default='image',
            help='Prefix for output images.')
    parser.add_argument('-f', '--fps', type=int, default=30,
            help='Fps for output video.')
    parser.add_argument('-x', '--width', type=int, default=50,
            help='Width of output images.')
    parser.add_argument('-y', '--height', type=int, default=50,
            help='Height of output image.')
    parser.add_argument
    args = parser.parse_args()

    videocreator = VideoCreator(args)


if __name__ == '__main__':
    main()
