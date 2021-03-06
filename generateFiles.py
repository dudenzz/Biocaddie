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
                            try:
                                text = jsonTree['dataItem']['description']
                            except:
                                text = jsonTree['dataItem']['title']
                        if repoid == 2:
                            try:
                                text = jsonTree['dataItem']['description'] + " "
                            except:
                                ok = 1
                            try:
                                for spec in jsonTree['organism']['target']:
                                    text += spec['species']
                            except:
                                ok = 1
                        if repoid == 3:
                            for part in jsonTree['anatomicalPart']:
                                text += part['name'] + " "
                            for part in jsonTree['disease']:
                                text += part['name'] + " "
                            for org in jsonTree['organism']:
                                text+=  org['name'] + " " + org['scientificName']
                        if repoid == 4:
                            try:
                                text = jsonTree['Study']['recruits']['criteria']  + " "  + jsonTree['Dataset']['description']
                            except:
                                ok = 1
                            try:
                                text += jsonTree['Treatment']['agent'] + " " + jsonTree['Treatment']['title'] + " " + jsonTree['Dataset']['briefTitle']  + " "
                            except:
                                ok = 1
                            try:
                                text += " " + jsonTree['Disease']['name']
                            except:
                                ok = 1
                            try:
                                for desc in jsonTree['StudyGroup']['description']:
                                    text += " " + desc
                            except:
                                ok = 1
                            try:
                                for keyword in jsonTree['Dataset']['keyword']:
                                    text += " " + keyword
                            except:
                                try:
                                    for keyword in jsonTree['Dataset']['keywords']:
                                        text += " " + keyword
                                except:
                                    text += ' no_kws'
                        if repoid == 5:
                            text = jsonTree['dataset']['description']
                            for keyword in jsonTree['dataset']['keywords']:
                                text += " "  + keyword
                        if repoid == 6:
                            text = jsonTree['dataItem']['description']
                        if repoid == 7:
                                try:
                                    text = jsonTree['dataset']['description']
                                except:
                                    text = jsonTree['dataset']['title']
                        if repoid == 8:
                            try:
                                text = jsonTree['dataset']['description']
                            except:
                                ok = 1
                            try:
                                for keyword in jsonTree['dataset']['keywords']:
                                    text += " " + keyword
                            except:
                                ok = 1
                        if repoid == 9:
                            try:
                                text += jsonTree['organism']['source']['commonName']
                            except:
                                ok = 1
                            try:
                                text += jsonTree['dataItem']['description']
                            except:
                                ok = 1
                        if repoid == 10:
                            try:
                                iFile = open(defs.root + defs.clean_geo + '/' + file.split('.')[0] + '.txt')
                                for line in iFile:
                                    text += line
                            except:
                                text = 'NA'
                        if repoid == 11:
                            try:
                                text = jsonTree['dataset']['note']
                            except:
                                ok = 1
                        if repoid == 12:
                            try:
                                text = jsonTree['dataItem']['description']
                            except:
                                ok = 1
                        if repoid == 13:
                            text = 'NA'
                        if repoid == 14:
                            for me in jsonTree['materialEntity']:
                                try:
                                    text += " " + me['name']
                                except:
                                    try:
                                        text += " " + me['formula']
                                    except:
                                        ok = 1
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
                    errFile = open('error_log','w+')
                    if text == "":
                        errFile.write(repo)
                        errFile.write("empty file " + file)

                    doc += text + "</body>\n + <\doc>"
                    oFile = open(defs.root + defs.clean_all + '/' + file.split('.')[0] + '.txt', 'w+')
                    oFile.write(doc.encode('utf-8'))
                    oFile.close()
            break