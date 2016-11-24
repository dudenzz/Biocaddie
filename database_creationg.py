__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults


defs = defaults()
working_dir = defs.root + defs.xmlexamples
for file in listdir(working_dir):
    iFile = open(working_dir + file)
    text = iFile.read()
    print text



