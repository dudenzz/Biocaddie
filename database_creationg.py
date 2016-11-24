__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults
import xml.etree.ElementTree as ET

defs = defaults()
working_dir = defs.root + defs.xmlexamples
for file in listdir(working_dir):
    iFile = open(working_dir + '/' +  file)
    text = iFile.read()
    xmlTree = ET.parse(text).getroot()
    for c in xmlTree:
        if c.tag == 'METADATA':
            print c



