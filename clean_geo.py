__author__ = 'Asus'

from os import listdir
from initials import defaults
from lxml import etree
import re


defs = defaults()
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
htmlparser = etree.HTMLParser()
for iter, file in enumerate(listdir(defs.root+defs.geohtmls)):
    if iter % 100 == 0:
        print iter
    tree = etree.parse(defs.root+defs.geohtmls + '/' + file,htmlparser)
    root = tree.getroot()
    try:
        ctable = root[1][4][0][0][5][2][1][0][0][0][0][0][0][5][0][0][0]
        oFile = open(defs.root + defs.clean_geo + '/' + file.split('_')[0] + '.txt', 'w+')
        oFile.write(cleanhtml(etree.tostring(ctable)))
        oFile.close()
    except:
        try:
            ctable = root[1]
            oFile = open(defs.root + defs.clean_geo + '/' + 'not_parsed_' + file.split('_')[0] + '.txt', 'w+')
            oFile.write('NA')
            oFile.close()
        except:
            oFile = open(defs.root + defs.clean_geo + '/' + 'NA_' + file.split('_')[0] + '.txt', 'w+')
            oFile.write('NA')
            oFile.close()