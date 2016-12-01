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
for file in listdir(defs.root+defs.geohtmls):
    tree = etree.parse(defs.root+defs.geohtmls + '/' + file,htmlparser)
    root = tree.getroot()
    ctable = root[1][4][0][0][5][2][1][0][0][0][0][0][5][0][0][0]
    print cleanhtml(ctable)

