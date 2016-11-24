__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults
import xml.etree.ElementTree as ET
import json

defs = defaults()
working_dir = defs.root + defs.xmlexamples
for file in listdir(working_dir):
    xmlTree = ET.parse(working_dir + '/' + file).getroot()
    for c in xmlTree:
        if c.tag == 'METADATA':
            jsonTree = json.loads(c.text)
            print jsonTree['dataItem']



