__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults
import xml.etree.ElementTree as ET
import json
import urllib2

defs = defaults()
working_dir = defs.root + defs.xmldocs
for i,file in enumerate(listdir(working_dir)):
    if i%10 == 0:
        print i
    xmlTree = ET.parse(working_dir + '/' + file).getroot()
    for c in xmlTree:
        if c.tag == 'METADATA':
            jsonTree = json.loads(c.text)
            try:
                clinical_trials_acc_link = json['Study']['homepage']
                ct = 1
                response = urllib2.urlopen(clinical_trials_acc_link)
                html = response.read()
                oFile = open(defs.root + defs.clinical_trials_htmls + '/' + file.split('.')[0] + '_geo.html', 'w+')
                oFile.write(html)
                oFile.close()
            except:
                ct = 0



