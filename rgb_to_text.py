#!/usr/bin/env python


import argparse
from PIL import Image


def convert(args):
    prefix = args.infile[: args.infile.find('.')]
    if not args.outfile:
        args.outfile = prefix + '.dat'

    img = Image.open(args.infile).convert('RGB')
    with open(args.outfile, 'w') as f:
        #f.write('# {}\n'.format(args.infile))
        for RGB in list(img.getdata()):
            f.write('{} {} {}\n'.format(RGB[0], RGB[1], RGB[2]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
                        help='Image file to convert.')
    parser.add_argument('outfile', type=str, default='', nargs='?',
                        help='Text file to write to.')
    args = parser.parse_args()
    convert(args)


if __name__ == '__main__':
    main()
