#!/usr/bin/env python
# -*- coding: latin-1 -*-

import initials
import xml.etree.ElementTree as ET
from xml.dom import pulldom
import sys


defs = initials.defaults()


def parseDesc(targetFile):
    file = defs.root + defs.mesh + '/desc2017.xml'
    print 'File path: '+file
    doc = pulldom.parse(file)
    idx=0
    for event, node in doc:
        if idx%1000==0:
            print idx
        res=''
        if event == pulldom.START_ELEMENT and node.tagName == 'DescriptorRecord':
            doc.expandNode(node)
            child = node.toxml()

            root = ET.fromstring(child.encode('utf-8'))

            DescriptorName = root.find('DescriptorName')
            name = DescriptorName.find('String').text

            res+='<meshterm>\n'
            res +='<name>'+name+'</name>\n'
            ConceptList = root.find('ConceptList')
            res +='<synonymlist>\n'
            for Concept in ConceptList.findall('Concept'):
                TermList = Concept.find('TermList')
                for Term in TermList.findall('Term'):
                    syn = Term.find('String').text
                    if syn != name:
                        res +='<synonym>' + syn + '</synonym>\n'

            res +='</synonymlist>\n'
            res +='</meshterm>\n'
            targetFile.write(res.encode('utf-8'))
        idx +=1
        #if idx==1000:
            #break

    print 'desc2017 finished'


def parseSuppl(targetFile):
    file = defs.root + defs.mesh + '/supp2017.xml'
    print 'File path: '+file
    doc = pulldom.parse(file)
    idx=0
    for event, node in doc:
        if idx%1000==0:
            print idx
        res=''
        if event == pulldom.START_ELEMENT and node.tagName == 'SupplementalRecord':
            doc.expandNode(node)
            child = node.toxml()

            root = ET.fromstring(child.encode('utf-8'))

            DescriptorName = root.find('SupplementalRecordName')
            name = DescriptorName.find('String').text

            res+='<meshterm>\n'
            res +='<name>'+name+'</name>\n'
            ConceptList = root.find('ConceptList')
            res +='<synonymlist>\n'
            for Concept in ConceptList.findall('Concept'):
                TermList = Concept.find('TermList')
                for Term in TermList.findall('Term'):
                    syn = Term.find('String').text

                    if syn!=name:
                        res +='<synonym>' + syn + '</synonym>\n'

            res +='</synonymlist>\n'
            res +='</meshterm>\n'
            targetFile.write(res.encode('utf-8'))
        idx +=1
        #if idx==100:
            #break

    print 'suppl2017 finished'

def parsePa(targetFile):
    file = defs.root + defs.mesh + '/pa2017.xml'
    print 'File path: '+file
    doc = pulldom.parse(file)
    idx=0
    for event, node in doc:
        if idx%1000==0:
            print idx
        res=''
        if event == pulldom.START_ELEMENT and node.tagName == 'PharmacologicalAction':
            doc.expandNode(node)
            child = node.toxml()

            root = ET.fromstring(child.encode('utf-8'))

            DescriptorReferredTo = root.find('DescriptorReferredTo')
            DescriptorName = DescriptorReferredTo.find('DescriptorName')
            name = DescriptorName.find('String').text

            res+='<meshterm>\n'
            res +='<name>'+name+'</name>\n'
            PharmacologicalActionSubstanceList = root.find('PharmacologicalActionSubstanceList')
            res +='<synonymlist>\n'
            for Substance in PharmacologicalActionSubstanceList.findall('Substance'):
                RecordName = Substance.find('RecordName')
                syn = RecordName.find('String').text
                if syn!=name:
                    res +='<synonym>' + syn + '</synonym>\n'

            res +='</synonymlist>\n'
            res +='</meshterm>\n'
            targetFile.write(res.encode('utf-8'))
        idx +=1
        #if idx==100:
            #break

    print 'pa2017 finished'

def parseQual(targetFile):
    file = defs.root + defs.mesh + '/qual2017.xml'
    print 'File path: '+file
    doc = pulldom.parse(file)
    idx=0
    for event, node in doc:
        if idx%1000==0:
            print idx
        res=''
        if event == pulldom.START_ELEMENT and node.tagName == 'QualifierRecord':
            doc.expandNode(node)
            child = node.toxml()

            root = ET.fromstring(child.encode('utf-8'))

            DescriptorName = root.find('QualifierName')
            name = DescriptorName.find('String').text

            res+='<meshterm>\n'
            res +='<name>'+name+'</name>\n'
            ConceptList = root.find('ConceptList')
            res +='<synonymlist>\n'
            for Concept in ConceptList.findall('Concept'):
                TermList = Concept.find('TermList')
                for Term in TermList.findall('Term'):
                    syn = Term.find('String').text
                    if syn != name:
                        res +='<synonym>' + syn + '</synonym>\n'

            res +='</synonymlist>\n'
            res +='</meshterm>\n'
            targetFile.write(res.encode('utf-8'))
        idx +=1
        #if idx==100:
            #break

    print 'qual2017 finished'




if len(sys.argv)>1:
    filename = sys.argv[1]
else:
    filename='meshSynonyms.xml'

targetFile = open(filename,'w')
targetFile.write('<?xml version="1.0"?>\n'.encode('utf-8'))
targetFile.write('<synonyms>\n'.encode('utf-8'))
parseDesc(targetFile)
parseSuppl(targetFile)
parsePa(targetFile)
parseQual(targetFile)
targetFile.write('</synonyms>\n'.encode('utf-8'))
targetFile.close()

