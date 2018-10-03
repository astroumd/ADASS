#! /usr/bin/env python
#
#   ADASS 2018 sample processing of the 3 XLS spreadsheets
#   1) you need python3
#   2) you need xlrd (should come with python3)

from __future__ import print_function

import xlrd
import sys


_p1 = 'ADASS 2018  Submitted Abstracts.xls'  
_p2 = 'ADASS 2018  Submitted Abstracts(1).xls'
_p3 = 'ADASS 2018  Total Registrant Re.xls'


class adass(object):
    def __init__(self, dirname, debug=False):
        """ Given a directory it will read in a set of spreadsheets that define the participants
            This is for ADASS 2018
        """
        # filenames
        self.p1 = dirname + '/' + _p1
        self.p2 = dirname + '/' + _p2
        self.p3 = dirname + '/' + _p3
        # sheets
        (self.x1,self.r1) = self.xopen(self.p1, debug)
        (self.x2,self.r2) = self.xopen(self.p2, debug)
        (self.x3,self.r3) = self.xopen(self.p3, debug)

    def xopen(self, path, debug=False, status = True):
        """
        path     file
        debug    print more
        status   if true, only accept 'New' in "Reg Status"
        """

        book = xlrd.open_workbook(path)
        ns = book.nsheets
        s0 = book.sheet_by_index(0)
        if ns != 1:
            print("Warning: %s has %d sheets" % (s0,ns))
        nr = s0.nrows
        nc = s0.ncols
        if debug:
            print("%d x %d in %s" % (nr,nc,path))
        # find which columns store the first and last name, we key on that
        row_values = s0.row_values(2)
        col_ln = row_values.index('Last Name')
        col_fn = row_values.index('First Name')
        # C&VS had a few revisions....
        if row_values[0] == 'Reg Status':     # (added 
            if row_values[2] == 'Modified':   # (added oct 1)
                self.off = 2
            else:
                self.off = 1
        else:
            self.off = 0
        status = status and (row_values[0] == 'Reg Status')
        s={}
        for row in range(3,nr):     # first 3 rows are administrative
            if status:
                if s0.cell(row,0).value != 'New':
                    continue
            name = s0.cell(row,col_ln).value + ", " + s0.cell(row,col_fn).value
            s[name] = s0.row(row)

        if debug:
            print("Accepted %d entries" % len(s))
        return (s,row_values)

    def print_col(self, col):
        """ print a given columns. expert mode
        """
        keys = list(self.x3.keys())
        keys.sort()
        for key in keys:
            r = self.x3[key]
            print(r[col+self.off].value)

    def report_0(self):
        """ print just the 'Lastname, Firstname' key
        """
        keys = list(self.x3.keys())
        keys.sort()
        for key in keys:
            print(key)

    def report_1(self, abstract=False):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present   = self.x1[key][22].value
            title1    = self.x1[key][23].value
            abstract1 = self.x1[key][24].value
            r = self.x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            email      = r[14+self.off].value
            if abstract: print(" ")
            if present == 'Talk/Focus Demo':
                if focus_demo == '1' and demo_booth == '1':
                    print("F+B",key,email,title1)
                elif focus_demo == '1':
                    print("F",key,email,title1)            
                elif demo_booth == '1':
                    print("B",key,email,title1)                        
                else:
                    print("O",key,email,title1)
            elif present == 'Poster':
                print("P",key,email,title1)
            else:
                print("X",key,email,title1)
            if abstract: print("    ABS:",abstract1)
            if key in self.x2:
                present2  = self.x2[key][22].value
                title2    = self.x2[key][23].value
                abstract2 = self.x2[key][23].value
                print("  ABS2",key,title2)
                if abstract: print("    ABS:",abstract2)

    def report_2(self,x1,x2,x3):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present = x1[key][22+self.off].value
            r = x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            print(present,key,'f=%s' % focus_demo,'d=%s' % demo_booth)

    def report_3(self,o1, count=False):
        """ report a selection of presenters based on list of names
        """
        # prepare list of last names
        lnames=[]
        keys  =[]
        for key in self.x1.keys():
            lnames.append(key[:key.find(',')])
            keys.append(key)
        #print(lnames)
        #print(keys)
        #
        n=0
        for k in o1:
            if k == '#': continue
            found = False
            if k in self.x1.keys():
                # full match
                found = True
                key = k
            else:
                # try a partial match based on last name
                if lnames.count(k) == 1: 
                    key = keys[lnames.index(k)]
                    found = True                    
                else:
                    # one last try, min. match if 'k' is in lnames[]
                    # for names in lnames:
                    print("# %s" % k)
            if found:
                n         = n + 1
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                if count:
                    print(n,key,present,title1)
                else:
                    print(key,'-',title1)

    def report_4(self, full = False, name=None):
        """ report emails only"""

        keys = list(self.x3.keys())
        keys.sort()
        if name != None:  full = True
        for key in keys:
            r = self.x3[key]
            email = r[14+self.off].value
            if full:
                msg = '"%s" <%s>' % (key,email)
                if name == None:
                    print(msg)
                else:
                    if msg.upper().find(name.upper()) > 0:
                        print(msg)
            else:
                print(email)

    def report_demo(self):
        """ report who wants demo table
        """
        for key in self.x3.keys():
            r = self.x3[key]
            focus_demo  = r[25+self.off].value
            comm_booth  = r[26+self.off].value
            astro_booth = r[27+self.off].value            
            if focus_demo != "":
                print(key,' FOCUS')
            if comm_booth != "":
                print(key,' COMMERCIAL')
            if astro_booth != "":
                print(key,' ASTRO')

 
if __name__ == "__main__":

    import io
    
    debug = True
    a = adass('reg', debug)
    
    if len(sys.argv) == 2:
        f1 = sys.argv[1]
        o1 = io.open(f1, encoding="utf-8").readlines()
        for i in range(len(o1)):
            o1[i] = o1[i].strip()
        a.report_3(o1)
    else:
        a.report_1(False)
