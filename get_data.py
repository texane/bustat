#!/usr/bin/env python


import random
import re
import urllib
import urllib2


ypages_re = re.compile('<strong id="SEL-nbresultat">(\d+)</strong>')
insee_re = re.compile('<td class="tab-chiffre">(.+)</td>')
annu_re = re.compile('<span class="nb_res">(\d+)</span>')


proxy = urllib2.ProxyHandler({'http': 'proxy.esrf.fr:3128'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)


def postal_db_init(path):
    # www.data.gouv.fr/en/datasets/base-officielle-des-codes-postaux
    # format: INSEE_code;name;postal_code;label
    try: f = open(path, 'r')
    except: return
    postal_db = {}
    while True:
        l = f.readline()
        if len(l) == 0: break
        v = l.split(';')
        if len(v) != 4: continue
        postal_db[v[1].lower()] = (v[0], v[2])
    return postal_db


def postal_db_query(postal_db, name):
    if name in postal_db:
        return (postal_db[name][0], postal_db[name][1])
    return None


def postal_db_randkeys(postal_db, n = None):
    if n == None: n = len(postal_db)
    if n > len(postal_db): n = len(postal_db)
    random.seed()
    return random.sample(postal_db.keys(), n)


def ypages_query(postal_id, postal_name, what):
    # query activity for given city
    # what the activity
    q = 'http://www.pagesjaunes.fr/annuaire/'
    q += postal_name + '-' + str(postal_id[0:2])
    q += '/' + what
    try:
        u = urllib2.urlopen(q)
        r = u.read()
        u.close()
    except:
        r = None
    if r == None: return 0
    m = ypages_re.search(r)
    if m == None: return 0
    return int(m.groups()[0])


def annu_query(postal_id, what):
    # query activity for given city
    # what the activity
    url = 'http://www.annu.com'
    try:
        data = urllib.urlencode({'q' : what + ' ' + str(postal_id) })
        u = urllib2.urlopen(urllib2.Request(url, data))
        r = u.read()
        u.close()
    except:
        r = None
    if r == None: return 0
    m = annu_re.findall(r)
    if m == None: return 0
    if len(m) == 0: return 0
    return int(m[-1])


def insee_query(insee_id):
    q = 'http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/'
    q += 'populations-legales/commune.asp?annee=2012&'
    q += 'depcom=' + str(insee_id)
    try:
        u = urllib2.urlopen(q)
        r = u.read()
        u.close()
    except:
        r = None
    if r == None: return 0
    m = insee_re.findall(r)
    if m == None: return 0
    return int(m[-1].replace('\xa0', ''))


def main():
    postal_db = postal_db_init('./postal_db.csv')

    print('# city people bakers butchers')

    cities = postal_db_randkeys(postal_db, 100)
    cities.append('grenoble')
    cities.append('nice')
    cities.append('rennes')
    cities.append('lorient')
    for i in range(1, 21):
        c = 'paris '
        if i < 10: c += '0'
        c += str(i)
        cities.append(c)

    for c in cities:
        ids = postal_db_query(postal_db, c)
        if ids == None: continue
        (insee_id, postal_id) = (ids[0], ids[1])
        people = insee_query(insee_id)
        bakers = annu_query(postal_id, 'boulangerie')
        butchers = annu_query(postal_id, 'boucherie')
        if (people == 0) or (bakers == 0) or (butchers == 0): continue
        s = "'" + c + "'"
        s += ' ' + str(people)
        s += ' ' + str(bakers)
        s += ' ' + str(butchers)
        print(s)

    return


main()
