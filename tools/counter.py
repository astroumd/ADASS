#! /usr/bin/env python


from __future__ import print_function

import xlrd
import sys
 
def open_file(path,col):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    n = s0.nrows
    for row in range(3,n):
        fname = s0.cell(row,3).value
        lname = s0.cell(row,4).value
        cval  = s0.cell(row,col).value
        print(cval)
        

 
if __name__ == "__main__":
    path = "reg/ADASS 2018  Total Registrant Re.xls"
    col = int(sys.argv[1])
    open_file(path,col)
