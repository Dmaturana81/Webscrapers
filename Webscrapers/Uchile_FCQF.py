#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:26:51 2017

@author: matu
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib
import lead_class
import re

url = 'https://quimica.unam.mx/directorio/'
title_rep = ['Dr. ', 'Dra. ']
#big_regex = re.compile('|'.join(map(re.escape, title_rep)))
reg_phone = re.compile("Tel. (\+52 55 \(\d{2,4}\)[-.\s]??\d{4}[-.\s]??\d{4})|Tel. (\+52 55 \d{4}[-.\s]??\d{4})|Tel. (\+52 55 \d{3}[-.\s]??\d{3}[-.\s]??\d{2})|Tel. (\+52 55 \d{2}[-.\s]??\d{2}[-.\s]??\d{2}[-.\s]??\d{2})")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+")
reg_anos = re.compile('20[12][5-9]')
reg_street = re.compile("([Ll]??[a-z]{2,10}[\.\s]??\d{3}[\.\-\s][a-zA-Z\s]+)|(\d{3} [a-zA-Z]+)")
reg_intereses = re.compile('Intereses de Investigación')
serv_url = 'http://www.ifc.unam.mx'

def get_all(url):
    Soup = BeautifulSoup(urllib.request.urlopen(url),'lxml')