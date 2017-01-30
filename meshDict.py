import initials
import xml.etree.ElementTree as ET
from xml.dom import pulldom

defs = initials.defaults()


def splitString(str):
    str = str.replace(',', '')
    str = str.replace('(', '')
    str = str.replace(')', '')
    words = str.split()
    return words

def prepareXmlMesh():
    file = defs.root + defs.mesh + '/desc2017.xml'
    print 'File path: '+file
    targetFile = open('descriptors.xml','w')
    targetFile.write('<?xml version="1.0"?>\n')
    targetFile.write('<Descriptors>\n')
    doc = pulldom.parse(file)
    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.tagName == 'DescriptorName':
            doc.expandNode(node)
            child = node.toxml()
            #print child
            targetFile.write(child+'\n')
    targetFile.close()
    targetFile.write('</Descriptors>\n')
    print 'Done'


def prepareMesh():
    tree = ET.parse('descriptors.xml')
    root = tree.getroot()
    print root.tag
    final=[]
    for elem in root:
        for e in elem:
            if (e.tag == 'String'):
                #print e.text
                result = splitString(e.text)
                for w in result:
                    #print w
                    final.append(w.lower())
    finalSet = set(final)
    targetFile = open('meshterms.txt', 'w')
    for elem in finalSet:
        #print elem
        targetFile.write(elem+'\n')

def loadMeshDict():
    file = open('meshterms.txt', 'r')
    dict = {}
    for line in file:
        #print line[0]
        key = line[0]
        if key in dict:
            #jest klucz
            value = dict[key]
            value.append(line)
        else:
            #nowy klucz
            dict[key] = [line]
    return dict



prepareXmlMesh()
prepareMesh()
#meshDict = loadMeshDict()
#print meshDict.keys()