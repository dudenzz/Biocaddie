__author__ = 'Jakub Dutkiewicz'

from os import listdir
from initials import defaults


defaults()

for file in listdir(defaults.root + defaults.xmlexamples):
    print file



