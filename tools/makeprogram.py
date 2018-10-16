#!/usr/bin/env python
from astropy.table import Table
import pandas as pd
import codecs
from html.entities import codepoint2name


class Program(object):

  def __init__(self,infile):
    self._file = infile
    #self._t = Table.read(infile,format='ipac',encoding='utf-8')
    self._t = Table.read(infile,format='ipac')
    self._df = self._t.to_pandas()
    self.a = None
    codecs.register_error('html_replace', self.html_replace)

  def _getadass(self):
    from adass2018 import adass
    self.a = adass("reg")

  def maketitle(self):
    if self.a == None:
       self._getadass()
    titles = []
    for c in self._t["last"]:
       #print(c)
       z = self.a.titles.get(c,"TBD")
       titles.append(z)
    self._t['title'] = titles

  def write(self,file):
    self._t.write(file,overwrite=True,format='ipac')
     

  def tohtml(self,days):
    colors = {"C": "lightblue", "L": "yellow", "F":"#ddd", "I":"orange", "Q":"lightgreen"}

    head = '<!DOCTYPE html> <html lang="en">\n <head>\n <!-- Required meta tags --> \n <meta name="viewport" content="width=device-width, initial-scale=1, shrink-t o-fit=no">\n <title>ADASS XXVIII Program</title>\n <!-- Bootstrap CSS -->\n <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css" >\n <!-- Icon -->\n <link rel="stylesheet" type="text/css" href="assets/fonts/line-icons.css">\n <!-- Slicknav -->\n <link rel="stylesheet" type="text/css" href="assets/css/slicknav.css">\n <!-- Nivo Lightbox -->\n <link rel="stylesheet" type="text/css" href="assets/css/nivo-lightbox.css" >\n <!-- Animate -->\n <link rel="stylesheet" type="text/css" href="assets/css/animate.css">\n <!-- Main Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/main.css">\n <!-- Responsive Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/responsive.css">\n   <!-- Custom styles for this template -->\n <link href="css/modern-business.css" rel="stylesheet">\n </head> <body>'

    begin = '<!--#include virtual="includes/nav.inc"-->\n<!--#include virtual="schedule-menu.html" -->'
    end_sched = '<!--#include virtual="schedule-end.html" -->'
    end_html = '<div id="preloader"> <div class="sk-circle"> <div class="sk-circle1 sk-child"></div> <div class="sk-circle2 sk-child"></div> <div class="sk-circle3 sk-child"></div> <div class="sk-circle4 sk-child"></div> <div class="sk-circle5 sk-child"></div> <div class="sk-circle6 sk-child"></div> <div class="sk-circle7 sk-child"></div> <div class="sk-circle8 sk-child"></div> <div class="sk-circle9 sk-child"></div> <div class="sk-circle10 sk-child"></div> <div class="sk-circle11 sk-child"></div> <div class="sk-circle12 sk-child"></div> </div> </div>\n\n <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n <script src="assets/js/jquery-min.js"></script>\n <script src="assets/js/popper.min.js"></script>\n <script src="assets/js/bootstrap.min.js"></script>\n <script src="assets/js/jquery.countdown.min.js"></script>\n <script src="assets/js/jquery.nav.js"></script>\n <script src="assets/js/jquery.easing.min.js"></script>\n <script src="assets/js/wow.js"></script>\n <script src="assets/js/jquery.slicknav.js"></script>\n <script src="assets/js/nivo-lightbox.js"></script>\n <script src="assets/js/main.js"></script>\n </body> </html>'

    tabstart='<div class="schedule-tab-content col-md-9 col-lg-9 col-xs-12 clearfix"> <div class="tab-content" id="myTabContent">'

    print("%s\n%s\n%s\n" %(head,begin,tabstart))

    for theday in days:
      xdf = self._df[(self._df['day']==theday)]
      if theday == "Sunday":
         active="active"
      else:
         active=""
      tabopen = '<div class="tab-pane fade show %s" id="%s" role="tabpanel" aria-labelledby="%s-tab">\n\n'%(active,theday,theday)
      accordion_start='<div id="accordion">'
      accordion_end   ='</div><!-- accordion -->\n</div><!-- end %s -->' %(theday)

      print(tabopen)
      print(accordion_start)
      for row_index,row in xdf.iterrows():
            talkid        = row['code']
            speaker_first = self.encode_for_html(row['first']).decode('utf-8').replace("&amp;","&");
            speaker_last  = self.encode_for_html(row['last']).decode('utf-8').replace("&amp;","&");
            title         = row['title']
            time_start    = row['start']
            time_end      = row['end']
            abstract      = row['last'] + ' Abstract here'

            if talkid[0] == "C" or talkid[0] == "L" or talkid[0] == "Q":
                card = '<div class="card"> \n<div id="heading%s"> <div class="card-header" style="background-color:%s;">\n <table class="table table-borderless p-0 m-0"><tr><td><h5 align="left">%s&ndash;%s</h5></td><td> <h5 align="left">%s %s</h5></td></tr> </table> \n</div></div></div>\n\n' %(talkid,colors[talkid[0]],time_start,time_end,speaker_first,speaker_last)

            else:
                c = colors.get(talkid[0],"#ffffff")
                card = '<div class="card"> \n<div id="heading%s"> <div class="collapsed card-header" style="background-color:%s;" data-toggle="collapse" data-target="#collapse%s" aria-expanded="false" aria-controls="collapse%s">\n <table class="table table-borderless p-0 m-0"><tr><td><h5 class="text-left">%s&ndash;%s</h5></td><td> <h5 class="text-left">%s %s &nbsp; <i>%s</i></h5></td></tr> </table> \n</div> </div>\n\n <div id="collapse%s" class="collapse" aria-labelledby="heading%s" data-parent="#accordion"> <div class="card-body"> <p>%s</p> </div> </div></div>\n\n' %(talkid,c,talkid,talkid,time_start,time_end,speaker_first,speaker_last,title,talkid,talkid,abstract)

            print(card)
      print(accordion_end)

    print(end_sched)
    print(end_html)

  ###########################################################
  # utf-8 to html encoding
  # @See https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s24.html
  def html_replace(self,exc):
      if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
          s = [ u'&amp;%s;' % codepoint2name[ord(c)]
                for c in exc.object[exc.start:exc.end] ]
          return ''.join(s), exc.end
      else:
          raise TypeError("can't handle %s" % exc.__name__) 

  def encode_for_html(self,unicode_data, encoding='ascii'):
      return unicode_data.encode(encoding, 'html_replace')
  ###########################################################


if __name__ == "__main__":
    _days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    
    if True:
        p = Program('orals2.ipac')
        p.maketitle()
        p.write('program.ipac')
    p = Program('program.ipac')
    p.tohtml(_days)
