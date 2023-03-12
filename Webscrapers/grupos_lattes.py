from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import lead_class
import re
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)



def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start + stop + 1:]
                finished = 0
    return text


def get_urls(file):
    f = open(file, 'r')
    pesq_file = codecs.open('pesquisadores.txt', 'a', 'utf-8')
    est_file = codecs.open('estudiantes.txt', 'a', 'utf-8')
    browser = webdriver.Safari()
    for i in f:
        browser.get(i)
        browser.implicitly_wait(10)
       # try:
            #element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "idFormVisualizarGrupoPesquisa:j_idt261_data")))
        source = browser.page_source
        Soup = BeautifulSoup(source, 'lxml')
        grp_name = Soup.find(attrs={'style':'position: relative;'}).text.lstrip(' \r\s\n\t').rstrip(' \r\s\n\t')
        print(grp_name)
        pesquisadores_table = Soup.find(attrs={'id':'idFormVisualizarGrupoPesquisa:j_idt261_data'})
        estudiantes_table = Soup.find(attrs={'id':'idFormVisualizarGrupoPesquisa:j_idt278_data'})
        eg_pesquisadores_table = Soup.find(attrs={'id':'idFormVisualizarGrupoPesquisa:j_idt332_data'})
        eg_estudiantes_table = Soup.find(attrs={'id':'idFormVisualizarGrupoPesquisa:j_idt344_data'})



        if not pesquisadores_table :
            print('No hay pesquisadores')
        else:
            pesq_names = pesquisadores_table.find_all('tr')
            for row in pesq_names:
                name = row.td.text.rstrip(' \s\t\r\n').lstrip(' \s\t\r\n')
                print(name)
                pesq_file.write(name + '\t' + grp_name)
                pesq_file.write('\n')
        if not estudiantes_table:
            print('Grupo sin Estudiantes')
        else:
            est_names = estudiantes_table.find_all('tr')
            for row in est_names:
                name = row.td.text.rstrip(' \s\t\r\n').lstrip(' \s\t\r\n')
                print(name)
                est_file.write(name + '\t' + grp_name)
                est_file.write('\n')
        if not eg_pesquisadores_table:
            print('No hay investigadores')
        else:
            pesq_names = eg_pesquisadores_table.find_all('tr')
            for row in pesq_names:
                name = row.td.text.rstrip(' \s\t\r\n').lstrip(' \s\t\r\n')
                print(name)
                pesq_file.write(name + '\t' + grp_name)
                pesq_file.write('\n')
        if not eg_estudiantes_table :
            print('No hay investigadores')
        else:
            est_names = eg_estudiantes_table.find_all('tr')
            for row in est_names:
                name = row.td.text.rstrip(' \s\t\r\n').lstrip(' \s\t\r\n')
                print(name)
                est_file.write(name + '\t' + grp_name)
                est_file.write('\n')
        # finally:
        #     browser.quit()

    est_file.close()
    pesq_file.close()
    browser.quit()



def get_info(url, name, source):
    institution = 'PUC - Chemistry'
    city = 'Santiago'
    state = 'RM'
    CEP = ''
    country = 'Chile'
    Soup = BeautifulSoup(source, 'lxml')
    (l_name, f_name) = name.split(', ', 1)
    home = Soup.find(attrs={'id': 'home'})
    proyects = Soup.find(attrs={'id': 'proyectos'})
    docencia = Soup.find(attrs={'id': 'docencia'})
    try:
        infop = home.find_all('p')
    except:
        infop = docencia.find_all('p')
    for p in infop:
        if len(p.text) == 0:
            continue

        text = StripTags(p.prettify())
        if text.find('Departamento') > 0:  # and re.findall(reg_phone, text) andre.findall(reg_email, text)::
            infos = text.split('\n', )
            institute = [s for s in infos if "Departamento" in s]
            institute = institute[0].lstrip().rstrip().split(' ', 2)[-1]

            # phone = re.findall(reg_phone, text)[0]
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
    l_aca = get_urls(file)
    browser = webdriver.Safari()
    for url in l_aca:
        browser.get(url)
        source = browser.page_source
        tmp = get_info(url, name, source)
        leads.append(tmp)
        leads_dict.append(tmp.Lead2dict())
        tmp2.append(tmp.Lead2dict())
    browser.quit()
    return leads_dict


file = sys.argv[1]
title_rep = ['Dr. ', 'Dra. ']
# big_regex = re.compile('|'.join(map(re.escape, title_rep)))
reg_phone = re.compile(
    "\(\d{2}[-\.\s]??\d{1}\)[-\.\s]??\d{4}[-\.\s]??\d{4}|\d{2}[-\.\s]??\d{1}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{2}[-\.\s]??\d{1}\)[-\.\s]??\d{3}[-\.\s]??\d{4}")
reg_email = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+")
reg_anos = re.compile('20[12][5-9]')
serv_url = 'http://dgp.cnpq.br/dgp/espelhogrupo/'
get_urls(file)
