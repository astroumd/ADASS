#! /usr/bin/env python
#
#   ADASS 2018 sample processing of the 3 XLS spreadsheets
#   1) you need python3 (or expect UTF-8 issues)
#   2) you need xlrd (should come with python3)

from __future__ import print_function

import xlrd
import sys
import io
import datetime

# names of the 3 sheets we got from C&VS (notice the 31 character limit of the basename)
_p1 = 'ADASS 2018  Submitted Abstracts.xls'  
_p2 = 'ADASS 2018  2nd Submitted Abstr.xls'
_p3 = 'ADASS 2018  Total Registrant Re.xls'
_p4 = 'IVOA Registration (Responses).xlsx'

_header1 = '<html> <body>\n'
_footer1 = '</body> </html>\n'

_header2 = """\\documentclass{report}\n
              \\usepackage{a4wide}\n
              \\begin{document}\n
           """

_footer2 = '\\end{document}\n'



class adass(object):
    def __init__(self, dirname, debug=False):
        """ Given a directory it will read in a set of spreadsheets that define the participants
            This is for ADASS 2018
        """
        # filenames
        self.p1 = dirname + '/' + _p1
        self.p2 = dirname + '/' + _p2
        self.p3 = dirname + '/' + _p3
        self.p4 = dirname + '/' + _p4        
        # sheets
        (self.x1,self.r1) = self.xopen(self.p1, debug)
        (self.x2,self.r2) = self.xopen(self.p2, debug)
        (self.x3,self.r3) = self.xopen(self.p3, debug)
        (self.x4,self.r4) = self.yopen(self.p4, debug)
        # prepare some lists
        self.lnames1=[]
        self.keys1  =[]
        self.titles = dict()
        for key in self.x1.keys():                       # loop over all "Lname, Fname"
            ln = key[:key.find(',')]
            self.lnames1.append(ln)     # make a list of all "Lname"
            self.titles[ln] = self.x1[key][23].value # makeprogram needs hash of last name and title
            self.keys1.append(key)                       # and list of "Lname, Fname"
        

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
            if name in s and debug:
                print("Warning: duplicate entry for %s" % name)
            s[name] = s0.row(row)

        if debug:
            print("Accepted %d entries" % len(s))
        return (s,row_values)

    def yopen(self, path, debug=False):
        """
        Return IVOA names
        
        path     file
        debug    print more
        
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
        row_values = s0.row_values(0)
        col_name = 1
        s={}
        for row in range(2,nr):     # first 3 rows are administrative
            name = s0.cell(row,col_name).value 
            if name in s and debug:
                print("Warning: duplicate entry for %s" % name)
            s[name] = s0.row(row)

        if debug:
            print("IVOA Accepted %d entries" % len(s))
        return (s,row_values)

    def expand_name(self,k):
        """ for a given (nick)name "k" find the full name we use in the hash
        """
        if k == '#':                                    # comment
            return None
        if k in self.x1.keys():                         # full match
            return k
        if self.lnames1.count(k) == 1:                  # match via last name
            return self.keys1[self.lnames1.index(k)]
        # one last try, min. match if 'k' is in lnames[]
        # for names in lnames:
        print("# %s" % k)
        return None
        
    def tab2list(self, filename, use_code=False):
        """ filename with "NAMES; Code"   - return the [names]
            if <NAMES> is <FNAME LNAME>, it adds them as <LNAME,FNAME>
        """
        o1 = io.open(filename, encoding="utf-8").readlines()
        o2 = []  # names
        o3 = []  # codes, should be required by now (I,O,B,F,T,P)
        o4 = []  # times, if appropriate (for I,O,B,F,T)
        nz = 0
        for i in range(len(o1)):
            s  = o1[i].strip() 
            w  = s.split(';')  # Split returns a list.
            nw = len(w)
            if nw == 0:    continue     # skip blank lines
            if w[0][0] =='#': continue  # skip comment lines
            if nw == 1:
                nz = nz + 1
                name = w[0].strip()
                code = 'Z%d' % nz
                time = 'N/A'
            elif nw == 2:
                name = w[0].strip()
                code = w[1].strip()
                time = 'TBD'
            elif nw == 3:
                name = w[0].strip()
                code = w[1].strip()
                time = w[2].strip()
            else:
                continue;

            ic = name.find(',')
            if ic < 0:
                names = name.split()
                if len(names) == 2:
                    name = names[1] + ', ' + names[0]
            o2.append(name)
            o3.append(code)
            o4.append(time)
        if use_code:
            return (o2,o3,o4)
        return o2
    
    # switch to makeprogram.py instead
    #def tab2list2(self, filename):
    #    o1 = io.open(filename, encoding="utf-8").readlines()
    #    for i in range(len(o1)):
    #        s  = o1[i].strip() 
    #        w  = s.split(';')  # Split returns a list.
    #        nw = len(w)
    #        if nw == 0:    continue     # skip blank lines
    #        if w[0][0] =='#': 
    #           ws = w[0].split()
    #           if w[1][0] == 'S': # starting a new session
    #              session_num = w[1][1:]
    #              newsession = True
    #           continue # for now skip other comments
    #
    #        # trim the tabs
    #        for w in range(len(w)):
    #            w[i] = w[i].strip()
            

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

    def report_0a(self):
        """ print the 'Lastname,  Firstname        Institution'
        """
        keys = list(self.x3.keys())
        keys.sort()
        index = self.r3.index('Univ/Affiliation')
        for key in keys:
            print(key,self.x3[key][index].value)

    def report_1(self, abstract=False, cat = False):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present   = self.x1[key][22].value
            title1    = self.x1[key][23].value
            abstract1 = self.x1[key][24].value
            theme1    = self.x1[key][20].value
            theme1a   = self.x1[key][21].value
            r = self.x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            email      = r[14+self.off].value
            theme = theme1[:theme1.find(')')]
                
            if abstract: print(" ")
            
            if present == 'Talk/Focus Demo':
                if focus_demo == '1' and demo_booth == '1':
                    ptype = "F+B"
                elif focus_demo == '1':
                    ptype = "F"                    
                elif demo_booth == '1':
                    ptype = "B"                    
                else:
                    ptype = "O"                    
            elif present == 'Poster':
                ptype = "P"
            else:
                ptype = "X"
                
            if cat:
                print("%s    ; %s%s." % (key,ptype,theme))
            else:
                if True:
                    print(ptype,key,email,title1)
                else:
                    print(ptype,key,email)
                    print("  TITLE:",title1)

            if abstract:
                print("    ABS:",abstract1)
                print("    T:",theme1)
                print("   TO:",theme1a)
            if key in self.x2:
                present2  = self.x2[key][22].value
                title2    = self.x2[key][23].value
                abstract2 = self.x2[key][23].value
                print("  ABS2",key,title2)
                if abstract: print("    ABS:",abstract2)

    def report_1a(self, tabname = None):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present   = self.x1[key][22].value
            title1    = self.x1[key][23].value
            abstract1 = self.x1[key][24].value
            theme1    = self.x1[key][20].value
            theme1a   = self.x1[key][21].value
            r = self.x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            email      = r[14+self.off].value
            theme = theme1[:theme1.find(')')]
                
            if abstract: print(" ")
            
            if present == 'Talk/Focus Demo':
                if focus_demo == '1' and demo_booth == '1':
                    ptype = "F+B"
                elif focus_demo == '1':
                    ptype = "F"                    
                elif demo_booth == '1':
                    ptype = "B"                    
                else:
                    ptype = "O"                    
            elif present == 'Poster':
                ptype = "P"
            else:
                ptype = "X"
                
            if cat:
                print("%s    ; %s%s." % (key,ptype,theme))
            else:
                print(ptype,key,email,title1)

            if abstract:
                print("    ABS:",abstract1)
                print("    T:",theme1)
                print("   TO:",theme1a)
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
        n=0
        for k in o1:
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                if count:
                    print(n,key,present,title1)
                else:
                    print(key,'-',title1)

    def report_3a(self,o1,o2,o3, count=False, dirname='www/abstracts', index=True):
        """ report a selection of presenters based on list of names
            o1 = names
            o2 = codes
            o3 = times
        """
        n=0
        for (k,c,t) in zip(o1,o2,o3):
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                if count:
                    print(n,key,present,title1)
                else:
                    fn = dirname + '/' + c + '.html'
                    fp = open(fn,'w')
                    fp.write(_header1)
                    msg = '<b>%s: %s</b>\n' % (c, key)   ; fp.write(msg)
                    msg = '<br>\n'                       ; fp.write(msg)
                    if True:
                        a1 = self.x1[key][9].value
                        b1 = self.x1[key][10].value;
                        if len(b1) > 0: b1 = '(' + b1 + ')'
                        a2 = self.x1[key][11].value
                        b2 = self.x1[key][12].value;
                        if len(b2) > 0: b2 = '(' + b2 + ')'
                        a3 = self.x1[key][13].value
                        b3 = self.x1[key][14].value;
                        if len(b3) > 0: b3 = '(' + b3 + ')'
                        a4 = self.x1[key][15].value
                        b4 = self.x1[key][16].value;
                        if len(b4) > 0: b4 = '(' + b4 + ')'
                        a5 = self.x1[key][17].value
                        b5 = self.x1[key][18].value;
                        if len(b5) > 0: b5 = '(' + b5 + ')'
                        a6 = self.x1[key][19].value
                        msg = '%s %s <br> %s %s <br>  %s %s<br>  %s %s<br>  %s %s<br>  %s' % (a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6);  fp.write(msg)
                        msg = '<br><br>\n'                       ; fp.write(msg)                                                                
                    if c[0] != 'P':
                        msg = '<b>Time: %s</b>\n' % t        ; fp.write(msg)
                        msg = '<br>\n'                       ; fp.write(msg)                                        
                    msg = '<i>%s</i>\n' % title1         ; fp.write(msg)
                    msg = '<br><br>\n'                       ; fp.write(msg)                                        
                    msg = '%s\n' % abstract1             ; fp.write(msg)
                    fp.write(_footer1)
                    fp.close()
                    if index:
                        msg = '<A HREF=%s.html>%s </A> <b>%s</b> :  %s<br>' % (c,key,c,title1)
                        print(msg)
                    
    def report_3b(self,o1,o2,o3, count=False, dirname='www/abstracts'):
        """ report a selection of presenters based on list of names - latex version of report_3a
            o1 = names
            o2 = codes
            o3 = times
        """
        def latex(text):
            """ attempt to turn text into latex
            """
            text = text.replace('_','\_')
            text = text.replace('&','\&')
            text = text.replace('#','\#')
            text = text.replace('^','\^')
            
            return text
        fn = dirname + '/' + 'abstracts.tex'
        fp = open(fn,'w')
        fp.write(_header2)
        fp.write('Generated %s\\newline\n\n' % datetime.datetime.now().isoformat())
        
        n=0
        for (k,c,t) in zip(o1,o2,o3):
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                email     = self.x1[key][6].value
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                if count:
                    print(n,key,present,title1)
                else:
                    msg = '\\subsection*{%s: %s}\n' % (c, title1); fp.write(msg)
                    msg = '\\bigskip\n'                          ; fp.write(msg)
                    if True:
                        a1 = self.x1[key][9].value
                        b1 = self.x1[key][10].value;
                        if len(b1) > 0: b1 = '(' + b1 + ')'
                        a2 = self.x1[key][11].value
                        b2 = self.x1[key][12].value;
                        if len(b2) > 0: b2 = '(' + b2 + ')'
                        a3 = self.x1[key][13].value
                        b3 = self.x1[key][14].value;
                        if len(b3) > 0: b3 = '(' + b3 + ')'
                        a4 = self.x1[key][15].value
                        b4 = self.x1[key][16].value;
                        if len(b4) > 0: b4 = '(' + b4 + ')'
                        a5 = self.x1[key][17].value
                        b5 = self.x1[key][18].value;
                        if len(b5) > 0: b5 = '(' + b5 + ')'
                        a6 = self.x1[key][19].value
                        msg = '%s %s \\newline %s %s \\newline  %s %s\\newline  %s %s\\newline %s %s\\newline  %s' % (a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6);
                        fp.write(latex(msg))
                        msg = '\\newline\\newline\n'                       ;
                        fp.write(latex(msg))                                                                
                    if c[0] != 'P':
                        msg = '{\\bf Time:} %s\\newline\n' % t        ; fp.write(latex(msg))
                        msg = '\\newline\n'                           ; fp.write(latex(msg))
                    # msg = '{\\it %s}\\newline\n' % title1             ; fp.write(latex(msg))
                    msg = '{\\it %s}\\newline\n' % email              ; fp.write(latex(msg))                    
                    msg = '\\newline\\newline\n'                      ; fp.write(latex(msg))
                    msg = '%s\\newline\n\\newpage\n' % abstract1      ; fp.write(latex(msg))
        fp.write(_footer2)
        fp.close()
                    
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

    def report_5(self):
        """ report IVOA names"""

        keys = list(self.x4.keys())
        # keys.sort()
        for key in keys:
            r = self.x4[key]
            name = r[1].value
            print(name)

    def report_6(self,o1, col=0):
        """ report a column
        """
        n=0
        for k in o1:
            if k in self.x3.keys():
                txtcol= self.x3[k][col].value
                msg = '%-33s %s' % (k,txtcol)
                print(msg)
            else:
                print('#', k)
                
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
    
    a = adass('reg')
    
    if len(sys.argv) == 3:                  # specific colum from registration
        o1 = a.tab2list(sys.argv[1])
        col = int(sys.argv[2])
        a.report_6(o1,col)
    elif len(sys.argv) == 2:                # titles 
        o1 = a.tab2list(sys.argv[1])
        a.report_3(o1,False)
    else:                                   # all , one or two liner
        a.report_1(False)                 
