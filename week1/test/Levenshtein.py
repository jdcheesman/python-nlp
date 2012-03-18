#!/usr/bin/env python

import sys


if __name__ == '__main__':
    if len(sys.argv) == 3:
        wordI = sys.argv[1].lower()
        wordJ = sys.argv[2].lower()

        i = 0
        j = 0
        data = [[0 for col in range(len(wordJ)+2)] for row in range(len(wordI)+2)]
        for cI in wordI:
            data[i+2][0] = cI
            data[i+1][1] = i
            i = i+1
        data[i+1][1] = i
        for cJ in wordJ:
            data[0][j+2] = cJ
            data[1][j+1] = j
            j = j+1
        data[1][j+1] = j
        data[0][0] = "&nbsp;"
        data[0][1] = "#"
        data[1][0] = "#"

        for y, row in enumerate(data):
            for x, ele in enumerate(row):
                if (x >= 2 and y >= 2):
                    across = data[x-1][y] + 1
                    down = data[x][y-1] + 1
                    diagonal = data[x-1][y-1]
                    if data[x][0] != data[0][y]:
                        diagonal = diagonal + 2
                    data[x][y] = min([across, down, diagonal])
        print "<html><body><table border=\"1\" cellpadding=\"10\">"
        for row in reversed(data):    
            print "<tr>"
            for ele in row:
                print "<td>%s</td>" % (ele)
            print "</tr>"
        print "</table></body></html>"
    else:
        print "usage: Levenshtein <word one> <word two>"
