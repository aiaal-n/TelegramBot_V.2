# -*- coding: utf-8 -*-
import json
import simplejson
import glob
from openpyxl import Workbook
import io
import re
import os



"""class info(object):
    input = open('injson.txt', 'r',encoding='utf8')
    output = open('output.txt', 'w', encoding='utf8')
    c = input.read(1)
    while len(c) > 0:
        if(c == '"'):
            c = ''


        output.write(c)
        c = input.read(1)

    input.close()
    output.close()"""
class OrganizationInn(object):

    input = open('injson.txt', 'r',encoding='utf-8')
    filename = 'outfile1.json'
    s = input.read()
    l = len(s)

    data1 = []
    i = 0
    integ = ''
    #[int(c) for c in s.split() if c.isdigit()]

    for c in s.split():
        if c.isdigit():
            data1.append({"inn":c})
    simplejson.dump(data1, open(filename, 'w', encoding='utf-8'))
    """for n in s:
        if n.isdigit():
            integ += n
        else:
            integ += ''
    if integ != '' and len(integ) >= 10:
        #integ.append(int(s_int))
        data1.append({"inn":integ})
    simplejson.dump(data1, open(filename, 'w', encoding='utf8'))"""
    #print integ.split()
    """while i < l:
        s_int = ''
        a = s[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '' and len(s_int) >= 10:
            #integ.append(int(s_int))
            data1.append({"inn":int(s_int)})
        simplejson.dump(data1, open(filename, 'w', encoding='utf8'))"""

    input.close()
    #filename.close()
