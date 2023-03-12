# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import urllib
import lead_class
import re

url = 'http://www.ibt.unam.mx/server/PRG.base?alterno:0,clase:pac,pre:inv'
title_rep = ['Dr. ', 'Dra. ']
#big_regex = re.compile('|'.join(map(re.escape, title_rep)))
reg_phone = re.compile("\d{3}[-\.\s]??\d{5}|\(\d{3}\)\s*\d{5}|\d{3}[-\.\s]??\d{5}")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+$")


serv_url = 'http://www.ibt.unam.mx/'

def get_links_HP(url):
    Soup = BeautifulSoup(urllib.request.urlopen(url))
    tds = Soup.find_all('td')
    l_jefe = get_links_jefe(tds[0].a['href'])
    l_aca = get_links_aca(tds[1].a['href'])
    return [l_jefe, l_aca]

def get_links_jefe(url):
    l_jefes = []
    url = serv_url + url
    site = urllib.request.urlopen(url)
    Soup = BeautifulSoup(site, 'lxml')
    for tag in Soup.find_all('td'):
        link = tag.a['href']
        link = serv_url + 'server/' + link
        l_jefes.append(link)
    
    return l_jefes

def get_links_aca(url):
    l_aca = []
    url = serv_url + url
    site = urllib.request.urlopen(url)
    Soup = BeautifulSoup(site, 'lxml')
    for tag in Soup.find_all('td'):
        link = tag.a['href']
        link = serv_url + 'server/' + link
        l_aca.append(link)
        
    return l_aca
        
def get_info_jefes(url):
    institution = 'UNAM'
    city = 'Mexico City'
    state = 'Mexico (Bundesstaat)'
    CEP = '04510'
    country = 'Mexico'
    site = urllib.request.urlopen(url)
    Soup = BeautifulSoup(site, 'lxml')
    info = Soup.find(attrs={'width':'452'})
    name = info.h3.text
    (title, f_name , l_name) = name.split(' ', 2)
    institute = info.find(attrs={'class':'linea'}).a.text.lstrip().rstrip()
  
    #getting email address    
    emails = re.findall(reg_email,info.tr.text)
    if len(emails) == 1:
        email = emails[0]
        email_s = ''
    elif len(emails) == 0:
        email = ''
        email_s = ''
    elif len(emails) == 2:
        email = emails[0]
        email_s = emails[1]
    else:
        email = emails[0]
        email_s = emails[1]

    #Get the part with info on address
    inf_adress = info.find_all('span')
    #gettin phone number
    if len(inf_adress)<2 :
        phone = 'NaN'
    else:
        phone = inf_adress[2].span.text.lstrip().rstrip()
        
    description = ''
    
    company = " - ".join([institution, "Ibt", institute])

    lead = lead_class.lead(company, country, state, url, f_name, l_name, email)

    lead.title = title
    lead.position = 'Head of Department / Institute'
    lead.description = description
    lead.city = city
    lead.CEP = CEP
    lead.institute = institute
    lead.institution = institution
    lead.email_s = email_s
    lead.phone = phone
    lead.name = name
    
    
    return lead

def get_info_Dr(url):
    institution = 'UNAM'
    city = 'Mexico City'
    state = 'Mexico (Bundesstaat)'
    CEP = '04510'
    country = 'Mexico'   
    site = urllib.request.urlopen(url)
    Soup = BeautifulSoup(site, 'lxml')
    info = Soup.find(attrs={'width':'452'})
    
    name = info.h3.text.lstrip().rstrip()
    #name = big_regex.sub('', name).lstrip().rstrip()
    #name = name.split(' ')
    
    #getting l_name, f_name and title
    if len(name.split(' ')) ==2:
        (f_name, l_name) = name.split(' ',1)
        title = 'NaN'
    elif len(name.split(' ')) >= 3:
        (title, f_name , l_name) = name.split(' ',2)
    else:
        (title, f_name, l_name) = ('NaN', 'NaN', 'NaN')
        
    lineas = info.find_all(attrs={'class':'linea'})
    dep = [k for k in lineas if 'Departamento' in k.text]
    if len(dep) == 1:
        institute = dep[0].a.text
    elif len(dep) == 0:
        institute = ''
    else:
        institute = ''
    #getting emails    
    emails = re.findall(reg_email,info.tr.text)
    if len(emails) == 1:
        email = emails[0]
        email_s = ''
    elif len(emails) == 0:
        email = ''
        email_s = ''
    elif len(emails) == 2:
        email = emails[0]
        email_s = emails[1]
    else:
        email = emails[0]
        email_s = emails[1]
    
    inf_adress = info.find_all('span')
    try:
        phone = inf_adress[2].span.text.lstrip().rstrip()
    except:
        phone = 'NaN'
    
    description = ''
    
    company = " - ".join([institution, "Ibt", institute])

    lead = lead_class.lead(company, country, state, url, f_name, l_name, email)

    lead.title = title
    lead.description = description
    lead.city = city
    lead.CEP = CEP
    lead.institute = institute
    lead.institution = institution
    lead.email_s = email_s
    lead.phone = phone
    lead.name = name
    lead.position = 'Principal Investigator / Lab Director / Group Leader'
    
    return lead
    

def get_all_UNAM_ibt(url):
    d = 0
    s = []
    x = get_links_HP(url)
    print('Links obtenidos')
    for y in x[0]:
        d= d+1
        s.append(get_info_jefes(y).Lead2dict())
        print('jefe numero: ' + str(d))
    for y in x[1]:
        d= d+1
        s.append(get_info_Dr(y).Lead2dict())
        print('academico numero: ' +str(d))
    return s
    