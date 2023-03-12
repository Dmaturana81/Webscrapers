#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 00:22:40 2017

@author: matu
"""

from JS_scraper import Page
from bs4 import BeautifulSoup
import lead_class
import pandas as pd
import urllib
import re

title_rep = ['Dr. ', 'Dra. ']
reg_phone = re.compile("\d{3}[-\.\s]??\d{5}|\(\d{3}\)\s*\d{5}|\d{3}[-\.\s]??\d{5}|\d{4}[-\.\s]??\d{4}|\(\d{4}\)\s*\d{4}|\d{4}[-\.\s]??\d{4}|\d{2}[-\.\s]??\(\d{3}\)[-\.\s]??\d{3}[-\.\s]??\d{4}|[Ee]xt[\.\s]+?\d{4,5}?")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+$")
server_ac = 'http://www.ifc.unam.mx/'


urls = ['http://www.ifc.unam.mx', 'http://www.ifc.unam.mx/investigacion/basica/bioquimica-biologia-estructural', 'http://www.ifc.unam.mx/investigacion/basica/genetica-molecular',
        'http://www.ifc.unam.mx/investigacion/basica/biologia-celular-y-del-desarrollo', 'http://www.ifc.unam.mx/investigacion/neurociencias/neuropatologia-molecular']


def get_all_links_ac(url, leads):
    state = 'Mexico (Bundesstaat)'
    country = 'Mexico'
    for url in urls:
        page = Page(url)
        print(url)
        Soup = BeautifulSoup(page.html, 'html.parser')
        researchers = Soup.find_all(attrs={'class':'researcherList'})
        for researcher in researchers:
            if len(researcher.a.h2.text.lstrip().rstrip()) > 1:
                name = researcher.a.h2.text.lstrip().rstrip()
                print(name)
            else:
                continue
            f_name, l_name = name.split(' ', 1)
            link = researcher.a['href'].lstrip().rstrip()
            link = server_ac + link
            lead = lead_class.lead('',country,state,link,f_name, l_name, '')
            leads.append(lead)
    return leads

def get_all_info(leads):
    leads_dic=[]
    for lead in leads:
        lead.CEP = '04510'
        lead.institution = 'UNAM - Biomedicine'
        lead.city = 'Mexico City'
        Soup = BeautifulSoup(urllib.request.urlopen(lead.url),'lxml')
        info = Soup.find(attrs={'id':'researcherInfo'})
        lead.institute = info.p.text.lstrip().rstrip()
        ps = info.find_all('p')
        for p in ps:
            if re.findall(reg_email, p.text):
                lead.email = re.findall(reg_email, p.text)[0]
                continue
            elif re.findall(reg_phone, p.text):
                lead.phone = " / ".join(re.findall(reg_phone, p.text))
                continue
            elif len(p.text) > 1:
                lead.street = p.text
                continue
        lead.company = " - ".join([lead.institution, lead.institute])
        leads_dic.append(lead.Lead2dict())
    return leads_dic
