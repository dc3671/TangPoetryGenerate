#/usr/bin/python2
# -*- coding: utf-8 -*-

from flask import *
import json
import urllib2
from predict import *

app = Flask(__name__)

global first
global second
global third
global fourth

@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')

@app.route('/get_poem', methods=['POST'])
def search():
    global first, second, third, fourth
    data = request.get_json() or request.form
    index = data['index']
    if (index == 1):
        first = data["sentense"].decode('utf8')
        print '第一句：' + first
        (i2, p2, second) = hmm(first, downlist, so_up2down, press_up2down, snum_up2down)
        print '第二句：' + second
        return second
    if (index == 2):
        (i3, p3, third) = hmm(second, uplist, so_down2nextup, press_down2nextup, snum_down2nextup)
        print '第三句：' + third
        return third
    if (index == 3):
        (i4, p4, fourth) = hmm(third, downlist, so_up2down, press_up2down, snum_up2down)
        print '第四句：' + fourth
        return fourth

if __name__ == '__main__':
    print('init...')
    init()
    print('start server...')
    app.run(debug=False, host='127.0.0.1', port=22222)
