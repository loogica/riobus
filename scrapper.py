import re
import codecs
import requests

from coopy.base import init_persistent_system
from riobus import RioBus

regex_bus_id = re.compile(r'\&route=(.*)')

riobus = init_persistent_system(RioBus())

if __name__ == "__main__":
    payload = {
        'texto_consulta': 154
    }

    #r = requests.post('http://vadeonibus.com.br/vadeonibus/' +
    #'index.php?d=abrangencia&lang=pt-br',
    #                 data=payload)
    #url = 'http://www.vadeonibus.com.br/vadeonibus/abrangencia_dados.php?ac=con_l&lang=pt-br&consulta=%d'

    index_url = 'http://www.vadeonibus.com.br/vadeonibus/' + \
                'abrangencia_dados.php?ac=con_l&lang=pt-br'
    r = requests.get(index_url)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text)

    urls = [(s['href'], s.string) for s in soup.find_all('a')]

    f = open('lines/content.txt', 'wt')
#    for u in urls:

#        f.write('%s,%u\n' % (u[0], u[1].encode('utf-8')))
#    f.close()

    for u in urls:
        bus_id = regex_bus_id.search(u[0]).group(1)
        bus_name = u[1].encode('utf-8')
        bus_url = u[0]

#        if not bus_id.startswith('154'):
#            continue

        print('Fetching for %s' % (bus_id))

        r = requests.get('http://www.vadeonibus.com.br/vadeonibus/' + bus_url)

        trajeto = BeautifulSoup(r.text)

        ruas = trajeto.table.find_all('tr')
        ff = codecs.open('lines/%s.txt' % (bus_id), 'wt', 'utf-8')

        i = 0

        riobus.init_line(bus_id)

        for r in ruas:
            v = r.find_all('td')
            if len(v) > 1:
                street_name = unicode(r.find_all('td')[1].string.strip())
                city_name = unicode(r.find_all('td')[2].string.strip())
                direction = unicode(r.find_all('td')[0].string.strip())
                ff.write(street_name + ",")
                ff.write,(city_name + ",")
                ff.write(direction + "\n")
                street = riobus.get_or_create_street(street_name,
                                                     city_name,
                                                     direction)
                riobus.add_street(street, bus_id)
                i += 1
        ff.close()

#        import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
        riobus.update_name_and_city(bus_id, bus_name, city_name)

        #break

    riobus.take_snapshot()
    print "end"
