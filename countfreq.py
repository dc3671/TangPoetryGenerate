#!/bin/usr/env python
# -*- coding: utf-8 -*-

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def count(obser, status, so, press, snum):
    if len(obser) != len(status): return

    for i in range(1, len(obser)):
        o = obser[i]
        s = status[i]
        pres = status[i - 1]

        if s not in so:
            so[s] = {}
        so[s].setdefault(o, 0)
        so[s][o] += 1

        if pres not in press:
            press[pres] = {}
        press[pres].setdefault(s, 0)
        press[pres][s] += 1

        snum.setdefault(s, 0)
        snum[s] += 1

    snum['B'] += 1


def save(filename, so, press, snum):
    data = open(filename + '.so', 'w')
    for s in so:
        for o in so[s]:
            data.write(s + ' ' + o + ' ' + str(so[s][o]) + '\n')
    data.close()

    data = open(filename + '.press', 'w')
    for pres in press:
        for s in press[pres]:
            data.write(pres + ' ' + s + ' ' + str(press[pres][s]) + '\n' )
    data.close()

    data = open(filename + '.status', 'w')
    for s in snum:
        data.write(s + ' ' + str(snum[s]) + '\n')
    data.close()

if __name__ == '__main__':
    # up to get down
    so_up2down = {}
    press_up2down = {}
    snum_up2down = {}
    snum_up2down['B'] = 0


    # down to get up
    so_down2nextup = {}
    press_down2nextup = {}
    snum_down2nextup = {}
    snum_down2nextup['B'] = 0

    preline = ''
    for index, line in enumerate(file('./data/poems.txt', 'r').readlines()):
        line = line.decode('utf8').strip()
        print index

        # blank line
        if line == '' or '#' in line:
            preline = line
            continue
        arr = line.split(' ')
        # up to get down
        count('B' + arr[0], 'B' + arr[1], so_up2down, press_up2down, snum_up2down)

        # blank line
        if preline == '' or '#' in preline:
            preline = line
            continue
        # down to get up
        count('B' + preline.split(' ')[1], 'B' + line.split(' ')[0], so_down2nextup, press_down2nextup, snum_down2nextup)

        preline = line

    save('./data/up2down', so_up2down, press_up2down, snum_up2down)
    save('./data/down2nextup', so_down2nextup, press_down2nextup, snum_down2nextup)

