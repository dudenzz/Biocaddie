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
                ID = jsonTree['dataItem']['ID']
                "AS"
                if ID.startswith("PRJNA"):
                    link = 'https://www.ncbi.nlm.nih.gov/bioproject/' + ID[5:]
                else:
                    raise

                prjna = 1
                response = urllib2.urlopen(link)
                html = response.read()
                oFile = open(defs.root + defs.biohtmls + '/' + file.split('.')[0] + '_bio.html', 'w+')
                oFile.write(html)
                oFile.close()
            except:
                prjna = 0