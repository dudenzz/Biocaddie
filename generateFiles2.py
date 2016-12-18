__author__ = 'Artur Cieslewicz'
import xml.etree.ElementTree as ET
import json
import initials
import os
import sys
defs = initials.defaults()

def handleExc():
    errstr = repo + "\t" + file + "\t" + repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\t' + str(e) + '\n'
    #print errstr
    exceptionFile = open('except_log yped_030716.log', 'a')
    exceptionFile.write(errstr)
    exceptionFile.close()
    return


exceptionFile = open('except_log yped_030716.log','w')
exceptionFile.write("Repo\tPlik\tError\tCodeLine\tJsonClass\n")
exceptionFile.close()
errFile = open('error_log','w')
errFile.write("List of empty files\n")
errFile.close()

for iter, file in enumerate(os.listdir(defs.root + defs.xmldocs)):
    if iter%1000 == 0:
        print iter
    tree = ET.parse(defs.root + defs.xmldocs + '/' + file)
    root = tree.getroot()
    doc = '<doc>\n\t<docid>' + file.split('.')[0] + '</docid>\n\t<doctitle>'
    for elem in root:
        if elem.tag == 'TITLE':
            try:
                doc += elem.text + '</doctitle>\n\t <body>'
            except:
                doc += '</doctitle> + \n\t <body>'
        if elem.tag == 'REPOSITORY':
            try:
                repo = elem.text.split('_')[0]
            except:
                repo = elem.text
        if elem.tag == 'METADATA':
            text = ''
            jsonTree = json.loads(elem.text)
            if repo == 'arrayexpress':
                try:
                    text += jsonTree['dataItem']['title'] + '\n'
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['description'] + '\n'
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['organism']['experiment']['species'] + '\n'
                except (Exception, IndexError) as e:
                    handleExc()

            if repo == 'cia':
                try:
                    for part in jsonTree['anatomicalPart']:
                        text += part['name'] + " "
                    for part in jsonTree['disease']:
                        text += part['name'] + " "
                    for org in jsonTree['organism']:
                        text += org['name'] + " " + org['scientificName']
                except (Exception, IndexError) as e:
                    handleExc()

            if repo == 'bioproject':
                try:
                    for org in jsonTree['organism']['target']:
                        text += org['species'] + ' '
                        text += org['strain'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kw in jsonTree['dataItem']['keywords']:
                        text += kw + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['description']
                except (Exception, IndexError) as e:
                    handleExc()

            if repo == 'clinicaltrials':
                try:
                    text += jsonTree['Study']['recruits']['gender'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Study']['recruits']['criteria'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Study']['phase'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Study']['location']['city'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Study']['location']['country'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for country in jsonTree['Study']['location']['othercountries']:
                        text += country + ''
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Study']['studyType'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for type in jsonTree['StudyGroup']['type']:
                        text += type + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for desc in jsonTree['StudyGroup']['description']:
                        text += desc + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Disease']['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Disease']['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Treatment']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Treatment']['agent'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Treatment']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['Dataset']['keyword']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['Dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'ctn':
                try:
                    for org in jsonTree['organism']:
                        text += org['scientificName'] + ' ' + org['name']
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['dataset']['keywords']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'cvrg':
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'dataverse':
                try:
                    text += jsonTree['publication']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'dryad':
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['dataset']['keywords']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'gemma':
                try:
                    for org in jsonTree['organism']['source']:
                        text += org['commonName'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'geo':
                try:
                    text += jsonTree['dataItem']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['source_name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['organism'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    if jsonTree['dataItem']['description'] != 'NA':
                        text += jsonTree['dataItem']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'mpd':
                try:
                    text += jsonTree['dataset']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['dataType'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['gender'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for org in jsonTree['organism']:
                        text += org['strain'] + ' ' + org['scientificName'] + ' ' + org['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for dim in jsonTree['dimension']:
                        text += dim['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'neuromorpho':
                try:
                    text += jsonTree['studyGroup']['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for part in jsonTree['anatomicalPart']['name']:
                        text += part + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['note'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for cel in jsonTree['cell']['name']:
                        text += cel + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['treatment']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['organism']['strain'] + ' ' + jsonTree['organism']['scientificName'] + ' ' +jsonTree['organism']['name'] + ' '+jsonTree['organism']['gender'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for dim in jsonTree['dimension']:
                        text += dim['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'nursadatasets':
                try:
                    text += jsonTree['dataAcquisition']['title'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['publication']['description'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['dataset']['keywords']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['title'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for org in jsonTree['organism']:
                        text += org['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'openfmri':
                try:
                    text += jsonTree['dataAcquisition']['title'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['title'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] +' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'pdb':
                try:
                    text += jsonTree['dataItem']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataItem']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['dataItem']['keywords']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for src in jsonTree['organism']['source']:
                        text += src['scientificName'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for hst in jsonTree['organism']['host']:
                        text += hst['scientificName'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for gen in jsonTree['gene']:
                        text += gen['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'peptideatlas':
                try:
                    text += jsonTree['dataset']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['instrument']['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    text += jsonTree['treatment']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for org in jsonTree['organism']:
                        text += org['strain'] + ' ' + org['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'phenodisco':
                try:
                    text += jsonTree['MESHterm'] + ' ' + jsonTree['title'] + ' ' + jsonTree['inexclude'] + ' ' + jsonTree['desc'] + ' ' + jsonTree['gender'] + ' ' + jsonTree['disease'] + ' ' + jsonTree['history'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'physiobank':
                try:
                    text += jsonTree['dataset']['title'] + ' ' + jsonTree['dataset']['dataType'] + ' ' + jsonTree['dataset']['description'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'proteomexchange':
                try:
                    text += jsonTree['instrument']['name'] + ' ' + jsonTree['dataset']['title'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for kwd in jsonTree['keywords']:
                        text += kwd + ' '
                except (Exception, IndexError) as e:
                    handleExc()
                try:
                    for org in jsonTree['organism']:
                        text += org['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()
            if repo == 'yped':
                try:
                    text += jsonTree['dataAcquisition']['title'] + ' ' + jsonTree['dataset']['description'] + ' ' + jsonTree['dataset']['title'] + ' ' + jsonTree['organism']['name'] + ' '
                except (Exception, IndexError) as e:
                    handleExc()

            errFile = open('error_log', 'a')
            if text == "":
                errFile.write(repo)
                errFile.write("empty file " + file)

            doc += text + "</body>\n<\doc>"
            oFile = open(defs.root + defs.clean_all + '/' + file.split('.')[0] + '.txt', 'w+')
            oFile.write(doc.encode('utf-8'))
            oFile.close()