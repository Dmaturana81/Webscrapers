# encoding: utf-8
from google import search
from random import randint
import re
import mechanize 
import time
import io
import urllib2
#from bs4 import BeautifulSoup
import cookielib
import sys
import shutil
import Levenshtein
import os, errno
import warnings
warnings.filterwarnings('ignore')

d_uni = {}
u =  io.open("universidades.txt", 'r', encoding='UTF-8' )
for line in u:
   (key, val) = line.split("\t")
   d_uni[key.lower()] = val.lower().rstrip("\n\r\ ")
idsincluidos = {}
fname2 = sys.argv[2]
#fout = io.open(fname2, 'a', encoding='UTF-8')
with io.open(sys.argv[2], 'r', encoding='UTF-8') as fout:
    for line in fout:
        idlattes = line.split("\t")[0]
        idsincluidos[idlattes]=1
fout.close()
fout = io.open(fname2, 'a', encoding='UTF-8')
fname1 = sys.argv[1]
fin = io.open(fname1, 'r', encoding='UTF-8')

def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text


def get_emails_google(search_list, intento):
    intento = int(intento) + 1
    name_split = search_list[0].split(' ')
    name_split.append(search_list[-1])
    search_str = "+".join(name_split)
    print "\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++"+""
    print "+ Results:"+""
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"+""
    print "searching for " + search_str
    d = {}
    page_counter_web = 0

    br = mechanize.Browser() ##
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 

    try:
        while page_counter_web < 50 :
            time.sleep(randint(60,120))

            #br.open('http://www.google.com.br/')
            #br.select_form(nr=0)
            #br.form['q'] = search_str.encode('UTF-8') ##

            #br.form['start'] = page_counter_web ##
            results_web = 'http://www.google.com/search?q='+search_str.encode('UTF-8')+'&lr=&ie=UTF-8&start=' + repr(page_counter_web) + '&sa=N'
            #request_web = urllib2.Request(results_web)
            #request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
            #opener_web = urllib2.build_opener()
            text = br.open(results_web).read() #opener_web.open(request_web).read()
            emails_web = (re.findall('([\d\w\.\-\<\>]+@[\<\>\d\w\.\-]+\.br)',StripTags(text)))
            for email_web in emails_web:
                if d.has_key(email_web):
                    d[email_web] += 1
                    for substring in sys.argv[1:]:
                        if substring in email_web:
                            d[email_web] += 4
                else:
                    d[email_web] = 1
            page_counter_web = page_counter_web +10

	

    except IOError as e:
        print " Intento: "+str(intento)+"; I/O error({0}): {1}".format(e.errno, e.strerror)
        time.sleep(intento * 1800)
        return get_emails_google(search_list, intento)



    if len(d) > 0:
        email_find = sorted(d, key=d.get, reverse=True)[0]
        print "mail encontrado: "+email_find
        return email_find #sorted(d, key=d.get, reverse=True)[0]
    else:
        if len(search_list) == 3:
            intento = 0
            get_emails_google(search_list[1:], intento)
        else:
            print "Definitivamente Sin Resultados !!!!"
            return 'none'
            

for line in fin:
    (idlattes, name, firstname, lastname, email, company, institute, address, rest) = line.split("\t",8)
    if company.lower() in d_uni:
        abrev = d_uni[company.lower()] + ".br"
    else:
        abrev = company
    
    if idlattes in idsincluidos:
        print 'IdLattes: %s de profesor %s, ya esta incluido en el archivo' % (idlattes, name)
        continue
    else:
        if email == 'None' or email == 'ERROR':
            print 'Buscando email para %s , %s' % (idlattes, name)
            google_search = [name, firstname+" "+lastname.lower(), abrev.replace(' ','+')]
            email = get_emails_google(google_search, 0)
            fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'
% (idlattes, name.capitalize(), firstname.capitalize(), lastname.capitalize(), email, company, institute, address, rest))
        else:
            print 'Email ya obtenido previamente %s , %s , %s' % (idlattes, name, email)
            fout.write('%s' % (line))
            continue
        


