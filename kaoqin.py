#!/usr/bin/python

import os
import re
import codecs
import time
 
os.system('cat /proc/net/arp > /tmp/arplist')

ipmac = {}
macname = {}
ipname = {}
maclogintime = {}
maclogouttime = {}
nameonlinestatus = {}
namefirstlogintime= {}
namelastlogouttime= {}

ff = open("/root/maclist.txt","r")
fflines = ff.readlines()
for ffline in fflines:
    ffmatchObj = re.match( r'.*list maclist \'(.*\:.*\:.*\:.*\:.*\:\w+)\'.*(#\w+).*', ffline, re.M|re.I)
    if ffmatchObj:
       macname[ffmatchObj.group(1).lower()] = ffmatchObj.group(2).lower()
       #print "ffmatchObj.group(1) : ", ffmatchObj.group(1)
       #print "ffmatchObj.group(2) : ", ffmatchObj.group(2)
ff.close()


f = open("/tmp/arplist","r")  
lines = f.readlines()
for line in lines:
    matchObj = re.match( r'(192\.168\.\d+.\d+)\s.*\s(0x\d)\s+(.*\:.*\:.*\:.*\:.*\:\w+)\s.*', line, re.M|re.I)
    if matchObj:
       ipmac[matchObj.group(1).lower()] = matchObj.group(3).lower()  
       #print "matchObj.group(1) : ", matchObj.group(1)
       #maconline[matchObj.group(3).lower()] = matchObj.group(2).lower()
       print "maconline key: ", matchObj.group(3) 
       print "maconline value: ", matchObj.group(2) 
f.close()

all_the_text=""
f4 = open('/www/bandwidthd/index.html','r')
for i in f4.readlines():
    all_the_text=all_the_text+i.strip()
f4.close()
 
         
for (k,v) in ipmac.items():
     if v in macname:
          ipname[k] = macname[v]
          print 'list'
          print k
          print macname[v]
          all_the_text=all_the_text.replace(k, macname[v], 100); 
          
fff = codecs.open('/www/bandwidthd/ipname.html','w','utf-8')
fff.write(all_the_text)
fff.close();

os.system(' logread | grep RSN > /tmp/loglogin')

flog = open("/tmp/loglogin","r")
floglines = flog.readlines()
for flogline in floglines:
    flogmatchObj = re.match( r'(.*)daemon.*STA\s(.*\:.*\:.*\:.*\:.*\:\w+)\sWPA', flogline, re.M|re.I)
    if flogmatchObj:
       if flogmatchObj.group(2).lower() not in maclogintime:
          maclogintime[flogmatchObj.group(2).lower()] = flogmatchObj.group(1)
          #print "flogmatchObj.group(1) : ", flogmatchObj.group(1)
          #print "flogmatchObj.group(2) : ", flogmatchObj.group(2)
flog.close()




if os.path.exists('/tmp/qiandaobiao'):
   if os.path.getsize('/tmp/qiandaobiao') > 0:
      f5 = open('/tmp/qiandaobiao','r')
      f5lines = f5.readlines()
      for f5line in f5lines:
          f5matchObj = re.match( r'(.*)at(#\w+)', f5line, re.M|re.I)
          if f5matchObj:
             namefirstlogintime[f5matchObj.group(2).lower()] = f5matchObj.group(1)
             #print "f5matchObj.group(1) : ", f5matchObj.group(1)
             #print "f5matchObj.group(2) : ", f5matchObj.group(2)
      f5.close()


for (k,v) in maclogintime.items():
     if k in macname:
          if macname[k] in namefirstlogintime:
             print "Exists",macname[k]
          else:
             namefirstlogintime[macname[k]] = v
              
fo = open('/tmp/qiandaobiao', "wb")
for (k,v) in namefirstlogintime.items():
     str = v+'at'+k
     fo.write(str)
     fo.write("\n")
fo.close

os.system(' logread | grep AP-STA-DISCONNECTED > /tmp/loglogout')
flogout = open("/tmp/loglogout","r")
flogoutlines = flogout.readlines()
for flogoutline in flogoutlines:
    flogoutmatchObj = re.match( r'(.*)daemon.*AP-STA-DISCONNECTED\s(.*\:.*\:.*\:.*\:.*\:\w+)', flogoutline, re.M|re.I)
    if flogoutmatchObj:
       maclogouttime[flogoutmatchObj.group(2).lower()] = flogoutmatchObj.group(1)
       print "maclogouttime: ", flogoutmatchObj.group(1)
       #print "flogoutmatchObj.group(2) : ", flogoutmatchObj.group(2)
flogout.close()

if os.path.exists('/tmp/likaibiao'):
   if os.path.getsize('/tmp/likaibiao') > 0:
      f6 = open('/tmp/likaibiao','r')
      f6lines = f6.readlines()
      for f6line in f6lines:
          f6matchObj = re.match( r'(.*)at(#\w+)', f6line, re.M|re.I)
          if f6matchObj:
             namelastlogouttime[f6matchObj.group(2).lower()] = f6matchObj.group(1)
             #print "f6matchObj.group(1) : ", f6matchObj.group(1)
             #print "f6matchObj.group(2) : ", f6matchObj.group(2)
      f6.close()

for (k,v) in maclogouttime.items():
     if k in macname:
          namelastlogouttime[macname[k]] = v
        
flo = open('/tmp/likaibiao', "wb")
for (k,v) in namelastlogouttime.items():
     str = v+'at'+k
     flo.write(str)
     flo.write("\n")
flo.close    
    
              
fwo = open('/tmp/bandwidthd/qdb.html', "wb")
fwo.write("<html><title>Exciting Network Login/Logout Information</title><body><h4>Exciting Network Login/Logout Information</h4><table border=1>")
str = '<tr><td>'+ 'Name' + '</td><td>' + 'The Earlierest Login Time' + '</td><td>The Last Logout Time </td></tr>'
fwo.write(str) 
for (k,v) in namefirstlogintime.items():
     print v
     b = time.mktime(time.strptime(v,"%a %b %d %H:%M:%S %Y "))
     c = time.strftime("%Y%m%d %H:%M:%S",time.localtime(b))
     if k not in namelastlogouttime:
        str = '<tr><td>'+k + '</td><td>' + c + ' </td><td> online </td></tr>'
     else:
        d = time.mktime(time.strptime(namelastlogouttime[k],"%a %b %d %H:%M:%S %Y "))
        e = time.strftime("%Y%m%d %H:%M:%S",time.localtime(d))
        str = '<tr><td>'+k + '</td><td>' + c + ' </td><td>' + e +' </td></tr>' 
     fwo.write(str)     
fwo.write("</table></body><br></html>")
fwo.close





