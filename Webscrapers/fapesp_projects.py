import urllib2
from bs4 import BeautifulSoup
import sys
import io

f = io.open('/Users/matu/workspace/tmp.txt', 'w', encoding ='UTF-8')
urlin = sys.argv[1]
pages = sys.argv[2]

for y in range(1,int(pages)):

    url = urlin + str(y)
    print url
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    Projects = soup.findAll('div', attrs={'class':'record'})



    for x in Projects:
        ref = x.a.get('href')
        title = x.a.text
        tds = x.findAll('td')
        url_ref = 'http://www.bv.fapesp.br/' + ref
        url_prof = 'http://www.bv.fapesp.br/' + tds[1].a.get('href')
        prof = x.find('a' , attrs={'itemprop':'author'}).text.lstrip(' \n\r\s\t').rstrip(' \r\s\t\n')
        lattes = x.find('a', attrs={'class':'plataforma_lattes'}).get('onclick').split(',',1)[0].replace('window.open(\"','').replace('\'','')
        company = x.find('td', attrs={'itemprop':'sourceOrganization'}).text.rstrip(' \n\r\t\s').lstrip(' \r\n\t\s')
        description = x.find('div', attrs={'class':'description'}).text.replace('Abstract','').lstrip(' \n\r\s\t').rstrip(' \r\s\t\n')
        fechas = tds[-1].text.split('-')
        inicio = fechas[0].lstrip(' \r\t\s\n').rstrip(' \r\s\t\n')
        try:
            fin = fechas[1].lstrip(' \r\t\s\n').rstrip(' \r\s\t\n')
        except:
            fin = 'None'
        cols_list = []
        colab_tag = x.findAll('a', attrs={'itemprop':'contributor'})
        if len(colab_tag) == 0:
            colab_url = ' '
            colab = ' '
            colab_lattes = ' '
            cols_list.append(" ".join([colab, colab_url, colab_lattes]))
        else:
            cols_link = x.findAll('span', attrs={'style':'display:none;'})
            col_n = 0
#        print cols_link
            for col in colab_tag:
                colab_url = 'http://www.bv.fapesp.br/' + col.get('href')
                colab = col.text.rstrip(' \r\t\s\n').lstrip(' \r\t\s\n')
                colab_lattes = cols_link[col_n].a.get('onclick').split(',',1)[0].replace('window.open(\'\"','').replace('\'','')
                col_n += 1
                cols_list.append(" ".join([colab, colab_url, colab_lattes]))

        colaboradores = "; ".join(cols_list)


        f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (title, url_ref, prof, url_prof, lattes, company, description, inicio, fin, colaboradores))
