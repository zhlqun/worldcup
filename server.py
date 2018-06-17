#p!/usr/bin/env python
#encoding=utf8

"""
es问答服务，使用flask搭建
"""
#------------------------------------------------------

import os
import sys
import json

from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

#------------------------------------------------------

@app.route('/worldcupDetail', methods=['GET', 'POST'])

def worldcupDetail():
    ret_str = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    
    <html xmlns="http://www.w3.org/1999/xhtml">
    
    <head>
    
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
    
    <meta http-equiv="refresh" content="12; url=http://39.105.49.216:8002/worldcupDetail" />    
    
    <title>群哥撸球直播</title>
    
    </head>
    
    <body>
    
    </body>
    
    </html>
 
    """

    i = 0
    last_score = ""
    for line in open("sina_dynamic/data/worldcupDetail", "r"):
        line = line.strip().split("\t")
        if len(line) != 5:
            continue
        context = line[1].split("\001")
        if line[2] == "-":
            line[2] = last_score
        last_score = line[2]
        if context[0] == "text":
            if line[4] == "1" or line[4] == 1:
                ret_str += """<p><font size="6" color="black">%s | %s | %s %s</font></p>""" % (line[0], context[1], line[3], line[2])
            elif line[4] == "2" or line[4] == 2:
                ret_str += """<p><font size="6" color="blue">%s | %s | %s %s</font></p>""" % (line[0], context[1], line[3], line[2])
            elif line[4] == "4" or line[4] == 4:
                ret_str += """<p><font size="7" color="red">%s | %s | %s %s</font></p>""" % (line[0], context[1], line[3], line[2])
            else:
                ret_str += """<p><font size="7" color="black">%s | %s | %s %s</font></p>""" % (line[0], context[1], line[3], line[2])
        elif context[0] == "url":
            ret_str += """<div><a href=""><img src="%s" tyle="margin: 0 auto;" width="800" height="600" border="0"></a></div>""" % (context[1])
        i += 1
        if i > 400:
            break
    return ret_str

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8002)

