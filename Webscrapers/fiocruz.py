
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

#def lattes2txt(listaMiembros):
#    identificador = 0
#    profmem = []
#    f = io.open(fname, 'w', encoding='utf8')
#    
#    for prof in listaMiembros:
#        profmem.append(Membro(identificador, prof,'','2010','2014','','',cachepath ))
#        identificador = identificador + 1
#    
#    for x in profmem:
#        x.carregarDadosCVLattes()
#        idsc.union(x.listaIDLattesColaboradoresUnica)
#        names = re.findall(r"[a-zA-Z\-]+", x.nomeEmCitacoesBibliograficas)
#        #print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo)
#        try:
#            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (x.idLattes, x.nomeCompleto, x.nomeCompleto.split(' ')[0], names[0], x.enderecoProfissional.split(',')[0], x.enderecoProfissional.split(',')[1], x.enderecoProfissional, x.textoResumo))
#        except IndexError:
#            f.write(u'%s\t\n' % (x.idLattes))
#            continue
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

webpage ='http://www.fiocruz.br/ioc/cgi/cgilua.exe/sys/start.htm?sid=71'

idsm = []
idsc = set([])

webp=webpage
page = urllib2.urlopen(webp)
soup = BeautifulSoup(page)
refs = soup.findAll('a', href=True, target='_blank')
for link in refs:
    lattes = link.get('href') if link.get('href').find('cnpq') >= 0 else 'nones'
    print lattes
    if lattes.find('buscatextual') >= 0 :
        latid=re.search(r"=([A-Z0-9]+)",lattes).group(1)
    elif lattes.find('lattes') >= 0 :
        latid=lattes[-16:]
    else:
        print ' ###### link no tiene direccion Lattes Correcta ######'
        continue

    idsm.append(latid) if latid not in idsm else next

lattes2txt(idsm)
























