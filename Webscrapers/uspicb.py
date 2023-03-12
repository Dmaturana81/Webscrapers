

import time
import io
import urllib2
from bs4 import BeautifulSoup
import sys
import shutil
import Levenshtein
import os, errno
import warnings
warnings.filterwarnings('ignore')

sys.path.append('scriptLattes')
sys.path.append('scriptLattes/producoesBibliograficas/')
sys.path.append('scriptLattes/producoesTecnicas/')
sys.path.append('scriptLattes/producoesArtisticas/')
sys.path.append('scriptLattes/producoesUnitarias/')
sys.path.append('scriptLattes/orientacoes/')
sys.path.append('scriptLattes/eventos/')
sys.path.append('scriptLattes/charts/')
sys.path.append('scriptLattes/internacionalizacao/')
sys.path.append('scriptLattes/qualis/')
sys.path.append('scriptLattes/patentesRegistros/')

from membro import *

def lattes2txt(listaMiembros):
    identificador = 0
    profmem = []
    f = io.open(fname, 'w', encoding='utf8')
    
    for prof in listaMiembros:
        profmem.append(Membro(identificador, prof,'','2010','2014','','',cachepath ))
        identificador = identificador + 1
    
    for x in profmem:
        x.carregarDadosCVLattes()
        x.filtrarItemsPorPeriodo()
        idsc.union(x.listaIDLattesColaboradoresUnica)
        names = re.findall(r"[a-zA-Z\-]+", x.nomeEmCitacoesBibliograficas)
        #print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo)
        #        try:
        #            Institution
        #            Institute
        #            Street
        try:
            Fone = re.findall(r"Telefone: ([0-9\(\) ]{8,13})", x.enderecoProfissional)[0]
        except:
            Fone = "None"
        
        try:
            City = re.findall(r"\-[\w ]+, [A-Z]{2}[ ,]", x.enderecoProfissional)[0].split(',')[0].strip(' -')
        except:
            City = u'None'
        
        try:
            State = re.findall(r" [A-Z]{2}[ ,]", x.enderecoProfissional)[0].strip()
        #            Country
        except:
            State = 'None'
        
        try:
            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo, City, State, Fone))
        except IndexError:
            f.write(u'%s\t\n' % (x.idLattes))
            continue

cachepath = '/Users/dmaturana/Downloads/lattes/cvs'

fname = sys.argv[1]

webpage = "http://www.bioqmed.ufrj.br/docentes/?pg="

idsm = []
idsc = set([])


for x in range(1,7) :
    webp=webpage + str(x)
    page = urllib2.urlopen(webp)
    soup = BeautifulSoup(page)
    todo = soup.find_all("div","item grid_6")
    for doc in todo:
        cname = doc.h2.text
        name = cname.split(' ')[0]
        address = doc.p.a.get('href')
        soup2 = BeautifulSoup(urllib2.urlopen(address))
        info = soup2.find('div','info')
        desc = info.p.text
        lattes = info.a.get('href').strip()
        if lattes.find('buscatextual') >= 0 :
            latid=re.search(r"=([A-Z0-9]+)",lattes).group(1)
        elif lattes.find('lattes') >= 0 :
            latid=lattes[-16:]
        else:
            print ' ###### Profesor %s no tiene id Lattes Correcto ######' % (cname)
            continue
        idsm.append(latid) if latid not in idsm else next

lattes2txt(idsm)

#for prof in idsm:
#    profmem.append(Membro(identificador, prof,'','2010','2014','','',cachepath ))
#    identificador = identificador + 1
#    
#for x in profmem:
#    x.carregarDadosCVLattes()
#    idsc.union(x.listaIDLattesColaboradoresUnica)
#    names = re.findall(r"[a-zA-Z\-]+", x.nomeEmCitacoesBibliograficas)
#    print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo)
#    f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo))
#    


        
        
#        
#        try:
#            lsoup = BeautifulSoup(urllib2.urlopen(lattes))
#            #name = lsoup.find_all('div', 'layout-cell layout-cell-12 data-cell')[0].find_all('div','layout-cell layout-cell-9')[1].text.split(',')[1]
#            lname = lsoup.find_all('div', 'layout-cell layout-cell-12 data-cell')[0].find_all('div','layout-cell layout-cell-9')[1].text.split(';')[0].split(',')[0].strip()
#            place = lsoup.find_all('div', 'layout-cell layout-cell-12 data-cell')[1].find_all('div', 'layout-cell-pad-5')[1].next.split(',')
#            univ = place[0]
#            latid = lsoup.find('div', 'layout-cell-pad-main').li.text[-16:]
#
#            try:
#                center = place[1]
#            except IndexError:
#                center = 'null'
#            
#            print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (latid, cname, name, lname, univ, center, address, lattes, desc)
#            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (latid, cname, name, lname, univ, center, address, lattes, desc))
#        except IndexError:
#            f.write('%s\t \t \t%s\t%s\t \t \t%s\n' % (cname, address, lattes, desc))
#            print 'ERROR con %s, se esperara 30 segundos y recomenzar' % cname
#            time.sleep(30)
#            
#
#
