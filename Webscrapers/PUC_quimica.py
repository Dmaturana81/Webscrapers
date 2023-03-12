#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:12:25 2017

@author: matu
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import lead_class
import re

url = 'http://quimica.uc.cl/es/facultad/academicos?start='
title_rep = ['Dr. ', 'Dra. ']
#big_regex = re.compile('|'.join(map(re.escape, title_rep)))
reg_phone = re.compile("\(\d{2}[-\.\s]??\d{1}\)[-\.\s]??\d{4}[-\.\s]??\d{4}|\d{2}[-\.\s]??\d{1}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{2}[-\.\s]??\d{1}\)[-\.\s]??\d{3}[-\.\s]??\d{4}")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+")
reg_anos = re.compile('20[12][5-9]')
serv_url = 'http://quimica.uc.cl/'

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

def get_urls(url):
    l_aca = []
    index = list(range(0,61,10))
    for i in index:
        print(i)
        Soup = BeautifulSoup(urllib.request.urlopen(url + str(i)),'lxml')
        rows_td = Soup.find_all('td')
        for row in rows_td:
            l_aca.append((serv_url + row.a['href'], row.text.lstrip('\t\n\r\s').rstrip('\t\n\r\s')))   
    return l_aca

def get_info(url, name, source):
    institution = 'PUC - Chemistry'
    city = 'Santiago'
    state = 'RM'
    CEP = ''
    country = 'Chile'
    Soup = BeautifulSoup(source, 'lxml')
    (l_name, f_name) = name.split(', ', 1)
    home = Soup.find(attrs={'id':'home'})
    proyects = Soup.find(attrs={'id':'proyectos'})
    docencia = Soup.find(attrs={'id':'docencia'})
    try:
        infop = home.find_all('p')
    except:
        infop = docencia.find_all('p')
    for p in infop:
        if len(p.text) == 0:
            continue
        
        text = StripTags(p.prettify())
        if text.find('Departamento') > 0:# and re.findall(reg_phone, text) andre.findall(reg_email, text)::
            infos = text.split('\n',)
            institute = [s for s in infos if "Departamento" in s]
            institute = institute[0].lstrip().rstrip().split(' ',2)[-1]

            #phone = re.findall(reg_phone, text)[0]
           # email = re.findall(reg_email, text)[0]
        if re.findall(reg_phone, text):
            phone = re.findall(reg_phone, text)[0]

        if re.findall(reg_email, text):
            email = re.findall(reg_email, text)[0]

    try:
        institute
    except NameError:
        institute = ''
    try:
        email
    except NameError:
        email = ''
    try:
        phone
    except NameError:
        phone = ''
    print(institute)
    company = " - ".join([institution, institute])
    try:
        projectos = proyects.find_all('p')
        actual_projects = []
        for proyecto in projectos:
            if len(re.findall(reg_anos, proyecto.text)):
                actual_projects.append(proyecto.text.lstrip('\s\n\r\t').rstrip('\s\n\r\t'))
        description = '\n'.join(actual_projects)       
    except:
        description = ''
        
    lead = lead_class.lead(company, country, state, serv_url + url, f_name, l_name, email)
    
    lead.title = ''
    lead.description = description
    lead.city = city
    lead.CEP = CEP
    lead.institute = institute
    lead.institution = institution
    lead.email_s = ''
    lead.phone = phone
    lead.name = name
    lead.position = ''
    lead.street = ''  
    lead.description = description
    return lead

def get_all(url):
    leads = [] 
    leads_dict = []
    l_aca = get_urls(url) 
    browser = webdriver.Safari()
    for url, name in l_aca:
        browser.get(url)
        source = browser.page_source
        tmp = get_info(url, name, source)
        leads.append(tmp)
        leads_dict.append(tmp.Lead2dict())
        tmp2.append(tmp.Lead2dict())
    browser.quit()
    return leads_dict