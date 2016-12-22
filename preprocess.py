#!/bin/usr/env python
# -*- coding: utf-8 -*-

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def isvalid(line):    
    return all(u'\u4e00' <= char <= u'\u9fff' or char == '，' or char == '。' for char in line)

def filter(poem):
    arr = poem.split('。') 
    for sent in arr:
        lst = sent.split('，') 
        if len(lst) != 2: continue
        if len(lst[0]) != len(lst[1]): continue
        output_data.write(lst[0] + ' ' + lst[1] + '\n')

    output_data.write('\n')

if __name__ == '__main__':
    output_data = file('./data/poems.txt', 'w') 

    poem = '' 
    for index, line in enumerate(file('./data/raw.txt', 'r').readlines()):
        line = line.decode('utf8').strip()
        print index
        if line == '': continue

        title_pattern = u'〖(.*?)〗' 
        res = re.findall(r'' + title_pattern, line)
        if len(res) == 1:
            filter(poem) 
            output_data.write('#' + res[0])
            poem = ''
            continue

        author_pattern = u'作者:' 
        if author_pattern in line:
            res = line[line.index(author_pattern) + len(author_pattern) :]
            output_data.write('#' + res + '\n')
            continue

        if not isvalid(line): 
            continue

        poem += line 
        continue

    filter(poem) 
    output_data.close()
