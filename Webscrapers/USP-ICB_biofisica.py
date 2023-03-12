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
server_ac = 'https://fisiologia.icb.usp.br/docentes/'


urls = ['https://fisiologia.icb.usp.br/docentes/']


def get_all_links_ac(url, leads):
    state = 'SP'
    country = 'Brazil'
    for url in urls:
        Soup = BeautifulSoup(urllib.request.urlopen(url),'lxml')
        print(url)
        # Soup = BeautifulSoup(page.html, 'html.parser')
        table = Soup.find(attrs={'class':'entry-content article'})
        researchers = table.find_all('a')
        for researcher in researchers:
            name = researcher.text
            print(name)
            f_name, l_name = name.split(' ', 1)
            link = researcher['href'].lstrip().rstrip()
            lead = lead_class.lead('',country,state,link,f_name, l_name, '')
            leads.append(lead)
    return leads

def get_all_info(leads):
    leads_dic=[]
    for lead in leads:
        lead.CEP = '05508-000'
        lead.institution = 'USP-ICB fisiologia biofisica'
        lead.city = 'São Paulo'
        Soup = BeautifulSoup(urllib.request.urlopen(lead.url),'lxml')
        linea = Soup.find(text='Resumo:').text
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
