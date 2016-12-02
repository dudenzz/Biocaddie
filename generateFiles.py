__author__ = 'Jakub Dutkiewicz'
import xml.etree.ElementTree as ET
import json
import initials
import os
defs = initials.defaults()

for iter, file in enumerate(os.listdir(defs.root + defs.xmldocs)):
    if iter%1000 == 0:
        print iter
    tree = ET.parse(defs.root + defs.xmldocs + '/' + file)
    root = tree.getroot()
    doc = '<doc>\n\t<docid>' + file.split('.')[0] + '</docid>\n\t<doctitle>'
    for elem in root:
        if elem.tag == 'TITLE':
            try:
                doc += elem.text + '</doctitle> + \n\t <body>'
            except:
                doc += '</doctitle> + \n\t <body>'
        if elem.tag == 'REPOSITORY':
            try:
                repo = elem.text.split('_')[0]
            except:
                repo = elem.text
            repoid = 0
            if repo == 'arrayexpress':
                repoid = 1
            if repo == 'bioproject':
                repoid = 2
            if repo == 'cia':
                repoid = 3
            if repo == 'clinicaltrials':
                repoid = 4
            if repo == 'ctn':
                repoid = 5
            if repo == 'cvrg':
                repoid = 6
            if repo == 'dataverse':
                repoid = 7
            if repo == 'dryad':
                repoid = 8
            if repo == 'gemma':
                repoid = 9
            if repo == 'geo':
                repoid = 10
            if repo == 'neuromorpho':
                repoid = 11
            if repo == 'nursadatasets':
                repoid = 12
            if repo == 'openfmri':
                repoid = 13
            if repo == 'pdb':
                repoid = 14
            if repo == 'peptideatlas':
                repoid = 15
            if repo == 'phenodisco':
                repoid = 16
            if repo == 'physiobank':
                repoid = 17
            if repo == 'yped':
                repoid = 18
            if repo == 'proteomexchange':
                repoid = 19
            if repo == 0:
                print repo
                raise
            for i_elem in root:
                if i_elem.tag == 'METADATA':
                    text = ''
                    jsonTree = json.loads(i_elem.text)
                    try:
                        if repoid == 1:
                            text = jsonTree['dataItem']['description']
                        if repoid == 2:
                            text = jsonTree['dataItem']['description'] + " " + jsonTree['organism']['target']['species']
                        if repoid == 3:
                            text = jsonTree['anatomicalPart']['name'] + " " + jsonTree['disease']['name'] + " " + jsonTree['organism']['name'] + " " + jsonTree['organism']['scientificName']
                        if repoid == 4:
                            text = jsonTree['studyGroup']['criteria'] + " " + jsonTree['disease']['name'] + " " + jsonTree['treatment']['agent'] + " " + jsonTree['treatment']['title'] + " " + jsonTree['Dataset']['briefTitle']  + " " + jsonTree['Dataset']['description']
                            for desc in sonTree['StudyGroup']['description']:
                                text += " " + desc
                            for keyword in " "+ jsonTree['Dataset']['keywords']:
                                text += " " + keyword
                        if repoid == 5:
                            text = jsonTree['dataset']['description']
                            for keyword in jsonTree['dataset']['keywords']:
                                text += " "  + keyword
                        if repoid == 6:
                            text = jsonTree['dataItem']['description']
                        if repoid == 7:
                            text = jsonTree['dataItem']['description']
                        if repoid == 8:
                            text = jsonTree['dataset']['description']
                            for keyword in jsonTree['dataset']['keywords']:
                                text += " " + keyword
                        if repoid == 9:
                            text = jsonTree['organism']['source']['commonName'] + jsonTree['dataItem']['description']
                        if repoid == 10:
                            try:
                                iFile = open(defs.root + defs.clean_geo + '/' + file.split('.')[0] + '.txt')
                                for line in iFile:
                                    text += line
                            except:
                                text = 'NA'
                        if repoid == 11:
                            text = jsonTree['dataset']['note']
                        if repoid == 12:
                            text = jsonTree['dataItem']['description']
                        if repoid == 13:
                            text = 'NA'
                        if repoid == 14:
                            for me in jsonTree['materialEntity']:
                                text += " " + me['text']
                        if repoid == 15:
                            text = jsonTree['treatment']['description']
                        if repoid == 16:
                            text = jsonTree['MESHterm'] + " " + jsonTree['phen'] + " " + jsonTree['phenID'] + " " + jsonTree['desc']
                        if repoid == 17:
                            text = jsonTree['dataset']['description']
                        if repoid == 18:
                            text = jsonTree['dataset']['description']
                        if repoid == 19:
                            for keyword in jsonTree['keywords']:
                                text += " " + keyword
                    except:
                        print file
                        raise
                    if text == "":
                        print repo
                        print "empty file" + file
                        raise
                    doc += text + "</body>\n + <\doc>"
                    oFile = open(defs.root + defs.clean_all + '/' + file.split('.') + '.txt')
            break