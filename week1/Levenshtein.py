#!/usr/bin/env python

import sys


if __name__ == '__main__':
    if len(sys.argv) == 3:
        for word in sys.argv[1:]:
            print word
            
    else:
        print "usage: Levenshtein <word one> <word two>"
