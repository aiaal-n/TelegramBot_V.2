# -*- coding: utf-8 -*-
import json
import simplejson
import glob
from openpyxl import Workbook
import io
import re
import os
data = []
class Organization(object):

    chat_id = None

    def __init__(self, chat_id):
        self.chat_id = chat_id

choise = False
"""class excel(object):
    wb = Workbook()
    dest_filename = 'empty_book.xlsx'
    ws1 = wb.active
    ws1.title = "еуыые"
    for row in range(1, 5):
        ws1.append(range(10))
        ws1['A1:B1'] = 'You should see three logos below'
    wb.save("sample.xlsx")"""
#Добавление инн огранизаций
class OrganizationInfo(object):
    filename = 'outfile1.json'
    global choise
    global data
    #global data
    print("Добавить пользователей по инн? введите y/n")
    ls = input()
    if(ls == "y"):
        #choise = True
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
        input.close()
    if(ls == "n"):
        #choise = False
        with open(filename, 'r') as f:
             data = json.load(f)

    """if(choise == True):
        for i in range(1):
            print("inn:")
            inn = input()
            print("name")
            name = input()

            #data = [inn, name]

            data = json.load(open(filename))
            data.append({'inn':inn, 'name':name})

            simplejson.dump(data, open(filename, 'w', encoding='utf8')).encode('utf8')"""
    with open(filename, 'r') as f:
         data = json.load(f)

    #data = json.load(open(filename))

    """input = open('injson.txt', 'r',encoding='utf8')
    output = open('outfile.json', 'w', encoding='utf8')
    find = False
    find1 = False



    c = input.read(1)
    while len(c) > 0:
        if(c == '"'):
            c = ''
        if(c == '14'):
            print("yes")
        output.write(c)
        c = input.read(1)

    input.close()
    output.close()
class OrganizationInn(object):
    input = open('injson.txt', 'r',encoding='utf8')
    filename = 'outfile1.json'
    s = input.read()
    l = len(s)
    integ = []
    data1 = []
    i = 0
    while i < l:
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
            integ.append(int(s_int))
    #output.write(str(integ))
            data1.append({"inn":int(s_int)})
        simplejson.dump(data1, open(filename, 'w', encoding='utf8'))

    input.close()
    #output.close()"""
