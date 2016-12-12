__author__ = 'Artur Cieslewicz'
import json
import os
import xml.etree.ElementTree as ET

import initials

defs = initials.defaults()


def getJsonKeys (jsonArg, tabDelimiter):
    result = ""
    if isinstance(jsonArg, dict):
        tabD = tabDelimiter + '\t'
        for key, value in jsonArg.iteritems():
            result += tabDelimiter + key + '\n'
            if isinstance(value,dict):
                result += getJsonKeys(value, tabD)
            if isinstance(value, list):
                for item in value:
                    result += getJsonKeys(item, tabD)
    return result

def getShortJsonKeys (jsonArg, tabDelimiter):
    result = ""
    if isinstance(jsonArg, dict):
        tabD = tabDelimiter + '\t'
        for key, value in jsonArg.iteritems():
            result += tabDelimiter + key + '\n'
            if isinstance(value,dict):
                result += getJsonKeys(value, tabD)
            if isinstance(value, list):
                result += tabD + '[List_inside]\n'
    return result


jsonStructures = []


for iter, file in enumerate(os.listdir(defs.root + defs.xmldocs)):
    if iter%1000 == 0:
        print iter
    tree = ET.parse(defs.root + defs.xmldocs + '/' + file)
    root = tree.getroot()
    for elem in root:
        if elem.tag == 'METADATA':
            jsonTree = json.loads(elem.text)
            jStructure = getShortJsonKeys(jsonTree,"")
            #jStructure = getJsonKeys(jsonTree,"")
            newPattern = True
            for jSt in jsonStructures:
                if jSt == jStructure:
                    newPattern = False
                    break
            if (newPattern):
                jsonStructures.append(jStructure)

logFile = open('jsonStructures_cia_030216.log','w')
logFile.write('Number of different structure patterns: '+str(len(jsonStructures))+'\n')
idx = 1
for elem in jsonStructures:
    logFile.write(str(idx)+'\n')
    logFile.write(elem+'\n')
    idx +=1
logFile.close()
