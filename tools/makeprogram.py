#!/usr/bin/env python
from astropy.table import Table
import pandas as pd
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
days = ['Monday']

t = Table.read('orals1.ipac',format='ipac')
df = t.to_pandas()

head = '<!DOCTYPE html> <html lang="en">\n <head>\n <!-- Required meta tags --> <meta charset="utf-8">\n <meta name="viewport" content="width=device-width, initial-scale=1, shrink-t o-fit=no">\n <title>ADASS XXVIII Schedule</title>\n <!-- Bootstrap CSS -->\n <link rel="stylesheet" type="text/css" href="assets/css/bootstrap.min.css" >\n <!-- Icon -->\n <link rel="stylesheet" type="text/css" href="assets/fonts/line-icons.css">\n <!-- Slicknav -->\n <link rel="stylesheet" type="text/css" href="assets/css/slicknav.css">\n <!-- Nivo Lightbox -->\n <link rel="stylesheet" type="text/css" href="assets/css/nivo-lightbox.css" >\n <!-- Animate -->\n <link rel="stylesheet" type="text/css" href="assets/css/animate.css">\n <!-- Main Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/main.css">\n <!-- Responsive Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/responsive.css">\n </head> <body>'

begin = '<!--#include virtual="schedule-menu.html" -->'
end_sched = '<!--#include virtual="schedule-end.html" -->'
end_html = '<div id="preloader"> <div class="sk-circle"> <div class="sk-circle1 sk-child"></div> <div class="sk-circle2 sk-child"></div> <div class="sk-circle3 sk-child"></div> <div class="sk-circle4 sk-child"></div> <div class="sk-circle5 sk-child"></div> <div class="sk-circle6 sk-child"></div> <div class="sk-circle7 sk-child"></div> <div class="sk-circle8 sk-child"></div> <div class="sk-circle9 sk-child"></div> <div class="sk-circle10 sk-child"></div> <div class="sk-circle11 sk-child"></div> <div class="sk-circle12 sk-child"></div> </div> </div>\n\n <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n <script src="assets/js/jquery-min.js"></script>\n <script src="assets/js/popper.min.js"></script>\n <script src="assets/js/bootstrap.min.js"></script>\n <script src="assets/js/jquery.countdown.min.js"></script>\n <script src="assets/js/jquery.nav.js"></script>\n <script src="assets/js/jquery.easing.min.js"></script>\n <script src="assets/js/wow.js"></script>\n <script src="assets/js/jquery.slicknav.js"></script>\n <script src="assets/js/nivo-lightbox.js"></script>\n <script src="assets/js/main.js"></script>\n </body> </html>'

tabstart='<div class="schedule-tab-content col-md-9 col-lg-9 col-xs-12 clearfix"> <div class="tab-content" id="myTabContent">'

print("%s\n%s\n%s\n" %(head,begin,tabstart))

for theday in days:
  xdf = df[(df['day']==theday)]
  tabopen = '<div class="tab-pane fade show active" id="%s" role="tabpanel" aria-labelledby="%s-tab">\n\n'%(theday,theday)
  accordion_start='<div id="accordion">'
  accordion_end   ='<div><!-- accordion >'

  print(tabopen)
  print(accordion_start)
  for row_index,row in xdf.iterrows():
        talkid        = row['code']
        speaker_first = row['first']
        speaker_last  = row['last']
        title         = row['title']
        time_start    = row['start']
        time_end      = row['end']
        abstract      = speaker_last + ' Abstract here'
        title         = speaker_last + ' Title here'

         

        card = '<div class="card"> \n<div id="heading%s"> <div class="collapsed card-header" data-toggle="collapse" data-target="#collapse%s" aria-expanded="false" aria-controls="collapse%s">\n <table class="table table-borderless p-0 m-0"><tr><td><h5 align="left">%s&ndash;%s</h5></td><td> <h5 align="left">%s %s:&nbsp; %s</h5></td></tr> </table> \n</div> </div>\n\n <div id="collapse%s" class="collapse show" aria-labelledby="heading%s" data-parent="#accordion"> <div class="card-body"> <p>%s</p> </div> </div></div>\n\n' %(talkid,talkid,talkid,time_start,time_end,speaker_first,speaker_last,title,talkid,talkid,abstract)

        print(card)
  print(accordion_end)

print(end_sched)
print(end_html)
