#!/usr/bin/env python
"""
rot
Translates a string using a rotated alphabet.
"""

import argparse
import sys
import string

symbols = string.punctuation + string.whitespace + string.digits
alphabet = string.ascii_letters
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
original_table = alphabet + symbols

def rot(n, text):
    n %= 26
    shifted_table = lowercase[n:] + lowercase[:n] + uppercase[n:] + uppercase[:n] + symbols
    translation_table = str.maketrans(original_table, shifted_table)
    result = []
    for word in text:
        result.append(word.translate(translation_table))
    return ' '.join(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int,
            help='Amount of chars to rotate by')
    parser.add_argument('text', type=str, nargs='+',
            help='Text to rotate.')
    args = parser.parse_args()

    print(rot(args.n, args.text))

if __name__ == '__main__':
    main()
