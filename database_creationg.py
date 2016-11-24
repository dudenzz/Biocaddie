__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults


defs = defaults()

for file in listdir(defs.root + defs.xmlexamples):
    iFile = open(file)
    text = iFile.read()
    print text



