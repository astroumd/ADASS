#! /usr/bin/env python


import xlrd
 
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
        print email
        

 
if __name__ == "__main__":
    path = "ADASS 2018  Total Registrant Re.xls"
    open_file(path)
