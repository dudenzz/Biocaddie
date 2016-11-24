__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults
import xml.etree.ElementTree as ET
import json
import urllib2

defs = defaults()
working_dir = defs.root + defs.xmlexamples
for file in listdir(working_dir):
    xmlTree = ET.parse(working_dir + '/' + file).getroot()
    for c in xmlTree:
        if c.tag == 'METADATA':
            jsonTree = json.loads(c.text)
            try:
                geo_acc_link = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + jsonTree['dataItem']['geo_accession']
                geoaccess = 1
                response = urllib2.urlopen(geo_acc_link)
                html = response.read()
                oFile = open(defs.root + defs.geohtmls + '/' + file.split('.')[0] + '_geo.html', 'w+')
                oFile.write(html)
                oFile.close()
            except:
                geoaccess = 0



