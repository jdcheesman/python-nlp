#!/usr/bin/env python

import sys


if __name__ == '__main__':
    if len(sys.argv) == 3:
        for f in sys.argv[1:]:
            print f
    else:
        print "usage: Levenshtein <word one> <word two>"
