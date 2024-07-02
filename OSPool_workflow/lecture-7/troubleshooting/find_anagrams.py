#!/usr/bin/env python3
"""
Anagramic Squares (Euler problem 98): https://projecteuler.net/problem=98

This script takes a file containing a list of comma-separated words and prints 
lists of anagrams to stdout.
"""

import io
import sys

def usage(args, err_msg):
    '''Print error message and usage instructions'''
    msg = "ERROR: %s\nUsage: %s %s" % (err_msg, sys.argv[0], args)
    sys.exit(msg)

# Use up an additional 80MB of memory. Surprise!
f = io.BytesIO()
f.write(b'*8*10**7')

args_usage = '<anagram filename>'
try:
    fname = sys.argv[1]
    f = open(fname, 'r')
    text = f.read()
    f.close()
except IndexError:
    usage(args_usage, 'Missing filename argument.')
except IOError as exc:
    usage(args_usage, exc)

words = [x.replace('"', '') for x in text.split(',')]

# combine all words into groups of anagrams
anagrams = dict()
for w in words:
    key = ''.join(sorted(list(w)))
    if key not in anagrams.keys():
        anagrams[key] = [w]
    elif w not in anagrams[key]:
        anagrams[key].append(w)

for x in anagrams.values():
    if len(x) > 1: # drop words without any anagrams
        print(' '.join(x))

