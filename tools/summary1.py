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

def xopen(path, debug=False):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    if ns != 1:
        print("Warning: %s has %d sheets" % (s0,ns))
    nr = s0.nrows
    nc = s0.ncols
    if debug:
        print("%d x %d in %s" % (nr,nc,path))
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
        if present == 'Talk/Focus Demo':
            if focus_demo == '1' and demo_booth == '1':
                print("F+B",key,email,title)
            elif focus_demo == '1':
                print("F",key,email,title)            
            elif demo_booth == '1':
                print("B",key,email,title)                        
            else:
                print("O",key,email,title)
        else:
            print("P",key,email,title)
        if key in x2:
            present2 = x2[key][22].value
            title2   = x2[key][23].value
            print("  ABS2",present2,key,title2)            
            


def report_2(x1,x2,x3):
    for key in x1.keys():
        present = x1[key][22].value
        r = x3[key]
        focus_demo = r[25].value
        demo_booth = r[26].value
        print(present,key,'f=%s' % focus_demo,'d=%s' % demo_booth)

 
if __name__ == "__main__":
    debug = False
    x1 = xopen(p1, debug)
    x2 = xopen(p2, debug)
    x3 = xopen(p3, debug)

    report_1(x1,x2,x3)
