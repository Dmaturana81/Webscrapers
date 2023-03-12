import urllib2
from bs4 import BeautifulSoup
import io
import re

fout = io.open('SAIB.txt', 'w', encoding='UTF-8')

for page in range(1,13):
    url = 'http://www.saib.org.ar/consultas/busquedas/detalleResumenesSocios.asp?variableSinUso=&variableSinUso=&intTipoAccion=4&txtLoginSocio=&txtApellido=&txtLocalidad=&selProvincia=0&txtEmail=&selCongreso=31&selSeccion=0&txtTitulo=&selTipoPresentacion=0&txtKeyWords=&button1=BUSCAR&variableSinUso=1&intPaginaActual='+str(page)
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    rows = soup.find_all('tr', attrs={'align':'left'})
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 7:
            print cells[1].text
            continue
        link_abstract1 = re.sub('javascript:popWindow\(\'','http://www.saib.org.ar/consultas/busquedas/',cells[6].a.get('href'))
        link_abstract = re.sub('\',\'previewResumen\'.*;','',link_abstract1)
        #print link_abstract
        abstract = urllib2.urlopen(link_abstract).read()
        sabstract = BeautifulSoup(abstract)
        authors = sabstract.find_all('em')
        if len(authors) < 3:
            names = authors[0].text
            email = authors[1].text
        else :
            names = authors[0].text
            company = authors[1].text
            email = authors[2].text
        resumen = sabstract.p.text
        presenter = cells[5].text.strip(' \s\t\n\r')
        title = cells[1].text.strip(' \s\r\t\n')

        #print '%s\t%s\t%s\t%s\t%s\t%s\n' % (presenter, names, email, company, title, resumen)
        fout.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (presenter, names, email, company, title, resumen))
