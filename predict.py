#!/bin/usr/env python
# -*- coding: utf-8 -*-

import sys
import re
from math import log
reload(sys)
sys.setdefaultencoding('utf-8')

so_up2down = {}
press_up2down = {}
snum_up2down = {}

so_down2nextup = {}
press_down2nextup = {}
snum_down2nextup = {}

poemlist = []
uplist = []
downlist = []
sentence2poem = []

class poem():
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

def loadfreq(filename, so, press, snum):
    for line in open(filename + '.so'):
        line = line.decode('utf8').strip()
        if line == '':
            continue

        arr = line.split(' ')
        s = arr[0]
        o = arr[1]
        cnt = arr[2]

        if s not in so:
            so[s] = {}
        so[s][o] = int(cnt)

    for line in open(filename + '.press'):
        line = line.decode('utf8').strip()
        if line == '':
            continue

        arr = line.split(' ')
        pres = arr[0]
        s = arr[1]
        cnt = arr[2]

        if pres not in press:
            press[pres] = {}
        press[pres][s] = int(cnt)

    for line in open(filename + '.status'):
        line = line.decode('utf8').strip()
        if line == '':
            continue

        arr = line.split(' ')
        s = arr[0]
        cnt = arr[1]

        snum[s] = int(cnt)

def loadpoems(filename):
    title = ''
    author = ''
    content = ''
    for line in open(filename):
        line = line.decode('utf8').strip()
        if line == '': continue
        if '#' in line:
            if title != '':
                x = poem(title, author, content)
                poemlist.append(x)
            arr = line.split('#')
            title = arr[1]
            author = arr[2]
            content = ''
            continue

        content += line + '\n'
        uplist.append(line.split(' ')[0])
        downlist.append(line.split(' ')[1])
        sentence2poem.append(len(poemlist))

    if title != '':
        x = poem(title, author, content)
        poemlist.append(x)


def hmm(obser, candidates, so, press, snum):
    obser = 'B' + obser
    maxi = 0
    maxp = float("-inf")
    for i in range(len(candidates)):
        candidate = 'B' + candidates[i]
        p = 0
        if len(candidate) != len(obser): continue

        for j in range(1, len(candidate)):
            s = candidate[j]
            o = obser[j]
            pres = candidate[j - 1]

            if s in so and o in so[s]:
                p += log(so[s][o] * 1.0 / snum[s])
            else:
                p += float("-inf")

            if pres in press and s in press[pres]:
                p += log(press[pres][s] * 1.0 / snum[pres])
            else:
                p += float("-inf")

        if maxp < p:
            maxi = i
            maxp = p


    return maxi, maxp, candidates[maxi]

def init():
    loadfreq('./data/up2down', so_up2down, press_up2down, snum_up2down)
    loadfreq('./data/down2nextup', so_down2nextup, press_down2nextup, snum_down2nextup)
    loadpoems('./data/poems.txt')

if __name__ == '__main__':
    first = sys.argv[1].decode('utf8')
    i1 = -1
    for i in range(len(uplist)):
        if uplist[i] == first or downlist[i] == first:
            i1 = i
            break

    print '第一句：' + first
    (i2, p2, second) = hmm(first, downlist, so_up2down, press_up2down, snum_up2down)
    print '第二句：' + second
    (i3, p3, third) = hmm(second, uplist, so_down2nextup, press_down2nextup, snum_down2nextup)
    print '第三句：' + third
    (i4, p4, fourth) = hmm(third, downlist, so_up2down, press_up2down, snum_up2down)
    print '第四句：' + fourth
