#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 21:57:03 2017

@author: matu
"""

from bs4 import BeautifulSoup
import urllib
import lead_class
import re
from PIL import Image
import pytesseract

url = 'http://www.biomedicas.unam.mx/investigacion/'
title_rep = ['Dr. ', 'Dra. ']
reg_phone = re.compile("\d{3}[-\.\s]??\d{5}|\(\d{3}\)\s*\d{5}|\d{3}[-\.\s]??\d{5}|\d{4}[-\.\s]??\d{4}|\(\d{4}\)\s*\d{4}|\d{4}[-\.\s]??\d{4}|\d{2}[-\.\s]??\(\d{3}\)[-\.\s]??\d{3}[-\.\s]??\d{4}|[Ee]xt[\.\s]+?\d{4,5}?")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+$")
server_img = 'http://www.biomedicas.unam.mx'


def get_links_HP(url):
    c = []
    Soup = BeautifulSoup(urllib.request.urlopen(url),'lxml')
    wrapper = Soup.find_all(attrs={'class':'wpb_wrapper'})
    for link in wrapper:
        try:
            c.append(link.a['href'])
        except:
            print('Wraper equivocado')
    return c[:-1]

def get_links_all(url):
    l_aca = []
    Soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
    members = Soup.find_all(attrs={'class':'member-item '})
    for member in members:
        l_aca.append((member.a['href'], member.text.lstrip(' \n\r\s').rstrip(' \n\r\s')))
    return l_aca

def get_data1(info_area_big, url):
    info_area = info_area_big.find(attrs={'style':'margin-top: -60px;'})
    info = info_area.find_all('p')
    institute, street, phone, email = ('', '', '', '')
    for p in info:
        if p.span.text.lstrip().rstrip() == 'Departamento'  :     
            institute = p.text.lstrip(' \r\s\n').split(' ', 1)[1]
        elif p.span.text.lstrip().rstrip() == 'Ubicación':
            street = p.text.split('\n')[-1].lstrip(' \n\r\s').rstrip(' \r\s\n')
        elif p.span.text.lstrip().rstrip() == 'Teléfono':
            phones = re.findall(reg_phone, p.text)
            phones = ['+52 ' + phone for phone in phones]
            phone = " / ".join(phones)
            phone = re.sub(r'\/ \+52 [Ee]', 'E', phone)
            print(phone)
        elif p.span.text.lstrip().rstrip() == 'Correo electrónico':
            im_url = url + p.img['src']
            img= Image.open(urllib.request.urlopen(im_url))
            email = pytesseract.image_to_string(img)             
    return (institute, street, phone, email )    

def get_data2(info_area_big, url):
    info_area = info_area_big.find(attrs={'style':'margin-top: -60px'})
    info = info_area.find_all('p')
    institute, street, phone, email = ('', '', '', '')
    for p in info:
        if p.span.text.lstrip().rstrip() == 'Departamento'  :     
            institute = p.text.lstrip(' \r\s\n').split(' ', 1)[1]
        elif p.span.text.lstrip().rstrip() == 'Ubicación':
            street = p.text.split('\n')[-1].lstrip(' \n\r\s').rstrip(' \r\s\n')
        elif p.span.text.lstrip().rstrip() == 'Teléfono':
            phones = re.findall(reg_phone, p.text)
            phones = ['+52 ' + phone for phone in phones]
            phone = " / ".join(phones)
            phone = re.sub(r'\/ \+52 [Ee]', 'E', phone)
            print(phone)
        elif p.span.text.lstrip().rstrip() == 'Correo electrónico':
            im_url = url + p.img['src']
            img= Image.open(urllib.request.urlopen(im_url))
            email = pytesseract.image_to_string(img) 
            print(email)
    return (institute, street, phone, email )    

def get_info(url, name):
    print(name)
    institution = 'UNAM - Biomedicine'
    city = 'Mexico City'
    state = 'Mexico (Bundesstaat)'
    CEP = '04510'
    country = 'Mexico'
    Soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
    (f_name, l_name) = name.split(' ', 1)
    
    info_area_big = Soup.find(attrs={'class':'col-md-8'})
    
    if info_area_big.find(attrs={'style':'margin-top: -60px;'}):
        institute, street, phone, email = get_data1(info_area_big, url)
    elif info_area_big.find(attrs={'style':'margin-top: -60px'}):
        institute, street, phone, email = get_data2(info_area_big, url)
    else:
        print(name + ' no tiene informacion')
        return None
        
    description = ''
    
    company = " - ".join([institution, institute])

    lead = lead_class.lead(company, country, state, url, f_name, l_name, email)
    
    lead.title = ''
    lead.description = description
    lead.city = city
    lead.CEP = CEP
    lead.institute = institute
    lead.institution = institution
    lead.email_s = ''
    lead.phone = phone
    lead.name = name
    lead.position = 'Principal Investigator / Lab Director / Group Leader'
    lead.street = street   
    return lead
    
def get_all_UNAM_biomed(urlHP):
    d = 0
    i = 0
    leads = []
    links = []
    urls = get_links_HP(urlHP)
    for url in urls:
        links = get_links_all(url)
        for lin in links:
            lead = get_info(lin[0], lin[1])
            i = i+1
            if lead == None:
                continue
                
            leads.append(lead.Lead2dict())
            d = d + 1

            print('Profesores analizados = ' + str(d) + ' / ' + str(i))
            
    return leads
    