#! /usr/bin/env python


from __future__ import print_function

import xlrd


p1 = 'ADASS 2018  Submitted Abstracts.xls'  
p2 = 'ADASS 2018  Submitted Abstracts(1).xls'
p3 = 'ADASS 2018  Total Registrant Re.xls'

def open_file(path):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    n = s0.nrows
    for row in range(3,n):
        fname = s0.cell(row,3).value
        lname = s0.cell(row,4).value
        email = s0.cell(row,14).value
        #print   '"',fname,lname,'" <',email,'>'
        print(email)

def xopen(path):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    if ns != 1:
        print("Warning: %s has %d sheets" % (s0,ns))
    nr = s0.nrows
    nc = s0.ncols
    # print("%d x %d in %s" % (nr,nc,path))
    s={}
    for row in range(3,nr):
        name = s0.cell(row,4).value + ", " + s0.cell(row,3).value
        s[name] = s0.row(row)
        
    return s

def report_1(x1,x2,x3):
    for key in x1.keys():
        present = x1[key][22].value
        title   = x1[key][23].value
        r = x3[key]
        focus_demo = r[25].value
        demo_booth = r[26].value
        email      = r[14].value
        if key in x2:
            a2 = "ABS2"
        else:
            a2 = ""
        print(present,key,email,a2,title)

def report_2(x1,x2,x3):
    for key in x1.keys():
        present = x1[key][22].value
        r = x3[key]
        focus_demo = r[25].value
        demo_booth = r[26].value
        print(present,key,'f=%s' % focus_demo,'d=%s' % demo_booth)

 
if __name__ == "__main__":
    x1 = xopen(p1)   # 3,4
    x2 = xopen(p2)   # 3,4
    x3 = xopen(p3)   # 3,4
    report_1(x1,x2,x3)
