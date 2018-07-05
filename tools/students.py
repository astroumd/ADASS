#! /usr/bin/env python


from __future__ import print_function

import xlrd
 
def open_file(path):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    n = s0.nrows
    for row in range(3,n):
        fname = s0.cell(row,3).value
        lname = s0.cell(row,4).value
        student = s0.cell(row,1).value
        print(student)
        

 
if __name__ == "__main__":
    path = "ADASS 2018  Total Registrant Re.xls"
    open_file(path)
