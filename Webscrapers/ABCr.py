import urllib2
from bs4 import BeautifulSoup
import sys
import io

print('Insert name of the output file ex. ABCr_2019.txt:')
file_out = raw_input()
f = io.open(file_out, 'w+', encoding='UTF-8')
base_url = 'http://www.abcristalografia.org.br'

soup = BeautifulSoup(urllib2.urlopen('http://www.abcristalografia.org.br/socios/lista.php').read(), 'lxml')
clases_socio = soup.findAll('table', attrs={'class':'ListaSocios'})
for clase in clases_socio:
    socios = clase.findAll('tr')
    for x in range(1,len(socios)-1):
        info = socios[x].findAll('td')
        name = info[0].text
        company = info[1].text
        state = info[2].text
        contact = info[3].text.replace('\n','; ')
        email = info[3].a.text
        link = base_url + info[0].a.get('href')
        data = BeautifulSoup(urllib2.urlopen(link).read(), 'lxml')
        # info_formacion = data.findAll('div', attrs={"style":"margin-top: 20px; background-color: #E5E5E5; padding: 10px;"})
        # formacion = (info_formacion[-1].text.split('\n\n\n')[-1] if len(info_formacion) > 0 else 'None')

        f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (name, company, state, email, link, contact))

