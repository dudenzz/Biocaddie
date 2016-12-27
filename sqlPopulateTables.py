import xml.etree.ElementTree as ET
import json
import initials
import sqlite3
import os
import sys
defs = initials.defaults()

def handleExc():
    errstr = repo + "\t" + file + "\t" + repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\t' + str(e) + '\n'
    #print errstr
    exFileName = 'except_log '+repo + '.log'
    exceptionFile = open(exFileName, 'a')
    exceptionFile.write(errstr)
    exceptionFile.close()
    return

def insertIntoDatabase(tableName, argNumber, args):
    sqlQuery = 'INSERT INTO ' + tableName +' VALUES('
    for i in range(0,argNumber):
        sqlQuery+='?'
        if (i!=argNumber-1):
            sqlQuery+=','
    sqlQuery+=')'
    #print sqlQuery
    cur.execute(sqlQuery,args)



#exceptionFile = open('except_log geo_022216.log','w')
#exceptionFile.write("Repo\tPlik\tError\tCodeLine\tJsonClass\n")
#exceptionFile.close()
#errFile = open('error_log','w')
#errFile.write("List of empty files\n")
#errFile.close()

conn = sqlite3.connect('biocaddie.db')
with conn:
    cur = conn.cursor()
    for iter, file in enumerate(os.listdir(defs.root + defs.xmldocs)):
        if iter%1000 == 0:
            print iter
        tree = ET.parse(defs.root + defs.xmldocs + '/' + file)
        root = tree.getroot()
        doc = '<doc>\n\t<docid>' + file.split('.')[0] + '</docid>\n\t<doctitle>'
        for elem in root:
            if elem.tag == 'TITLE':
                title = elem.text

            if elem.tag == 'REPOSITORY':
                try:
                    repo = elem.text.split('_')[0]
                except:
                    repo = elem.text

            if elem.tag == 'METADATA':
                #print title
                #print repo
                cur.execute("INSERT INTO common(filename, title, repository) VALUES(?,?,?)", (file, title, repo))
                lid = cur.lastrowid
                text = ''
                jsonTree = json.loads(elem.text)
                if repo == 'arrayexpress':
                    try:
                        dataItemtitle = jsonTree['dataItem']['title']
                    except:
                        dataItemtitle = ""
                        handleExc()
                    try:
                        dataItemdescription = jsonTree['dataItem']['description']
                    except:
                        dataItemdescription = ""
                        handleExc()
                    try:
                        species = jsonTree['organism']['experiment']['species']
                    except:
                        species = ""
                        handleExc()

                    sqlArgs = (lid, dataItemtitle, dataItemdescription, species)
                    insertIntoDatabase('arrayexpress',len(sqlArgs),sqlArgs)


                if repo == 'cia':
                    try:
                        anatomicalPartname = ''
                        diseasename = ''
                        organismname = ''
                        organismscientificname = ''
                        for part in jsonTree['anatomicalPart']:
                            anatomicalPartname += part['name'] + " "
                        for part in jsonTree['disease']:
                            diseasename += part['name'] + " "
                        for org in jsonTree['organism']:
                            organismname += org['name'] + " "
                            organismscientificname += org['scientificName'] + " "
                    except (Exception, IndexError) as e:
                        handleExc()

                    sqlArgs = (lid, anatomicalPartname, diseasename, organismname, organismscientificname)
                    insertIntoDatabase('cia',len(sqlArgs),sqlArgs)


                if repo == 'bioproject':
                    species = ''
                    strain = ''
                    keywords = ''
                    desc = ''
                    try:
                        for org in jsonTree['organism']['target']:
                            species += org['species'] + ' '
                            strain += org['strain'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kw in jsonTree['dataItem']['keywords']:
                            keywords += kw + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        desc += jsonTree['dataItem']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid, species, strain, keywords, desc)
                    insertIntoDatabase('bioproject', len(sqlArgs), sqlArgs)

                if repo == 'clinicaltrials':
                    gender = ''
                    criteria = ''
                    phase = ''
                    city = ''
                    Locationcountry = ''
                    othercountries = ''
                    studyType = ''
                    StudyGrouptype = ''
                    StudyGroupDes = ''
                    StudyGroupName = ''
                    DiseaseName = ''
                    TreatmentDesc = ''
                    TreatmentAgent = ''
                    TreatmentTitle = ''
                    keyword = ''
                    DatasetDesc = ''


                    try:
                        gender += jsonTree['Study']['recruits']['gender']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        criteria += jsonTree['Study']['recruits']['criteria']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        phase += jsonTree['Study']['phase']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        city += jsonTree['Study']['location']['city']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        Locationcountry += jsonTree['Study']['location']['country']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for country in jsonTree['Study']['location']['othercountries']:
                            othercountries += country + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        studyType += jsonTree['Study']['studyType']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for type in jsonTree['StudyGroup']['type']:
                            StudyGrouptype += type + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for desc in jsonTree['StudyGroup']['description']:
                            StudyGroupDes += desc + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        StudyGroupName += jsonTree['StudyGroup']['name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        DiseaseName += jsonTree['Disease']['name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        TreatmentDesc += jsonTree['Treatment']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        TreatmentAgent += jsonTree['Treatment']['agent']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        TreatmentTitle += jsonTree['Treatment']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['Dataset']['keyword']:
                            keyword += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        DatasetDesc += jsonTree['Dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()

                    sqlArgs = (lid, gender,
                    criteria,
                    phase,
                    city,
                    Locationcountry,
                    othercountries,
                    studyType,
                    StudyGrouptype,
                    StudyGroupDes,
                    StudyGroupName,
                    DiseaseName,
                    TreatmentDesc,
                    TreatmentAgent,
                    TreatmentTitle,
                    keyword,
                    DatasetDesc)
                    insertIntoDatabase('clinicaltrials', len(sqlArgs), sqlArgs)
                if repo == 'ctn':
                    scientificName = ''
                    name = ''
                    description = ''
                    keywords = ''
                    try:
                        for org in jsonTree['organism']:
                            scientificName += org['scientificName'] + ' '
                            name += org['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        description += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['dataset']['keywords']:
                            keywords += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                        scientificName,
                        name,
                        description,
                        keywords
                    )
                    insertIntoDatabase('ctn', len(sqlArgs), sqlArgs)
                if repo == 'cvrg':
                    desc = ''
                    try:
                        desc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                    desc)
                    insertIntoDatabase('cvrg', len(sqlArgs), sqlArgs)
                if repo == 'dataverse':
                    pubdesc = ''
                    datasetdesc = ''
                    try:
                        pubdesc += jsonTree['publication']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        datasetdesc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               pubdesc,
                               datasetdesc)
                    insertIntoDatabase('dataverse', len(sqlArgs), sqlArgs)
                if repo == 'dryad':
                    desc = ''
                    keywords = ''
                    try:
                        desc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['dataset']['keywords']:
                            keywords += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               desc,
                               keywords)
                    insertIntoDatabase('dryad', len(sqlArgs), sqlArgs)
                if repo == 'gemma':
                    commonName = ''
                    title = ''
                    description = ''
                    try:
                        for org in jsonTree['organism']['source']:
                            commonName += org['commonName'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        title += jsonTree['dataItem']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        description += jsonTree['dataItem']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               commonName,
                               title,
                               description)
                    insertIntoDatabase('gemma', len(sqlArgs), sqlArgs)
                if repo == 'geo':
                    title = ''
                    name = ''
                    organism = ''
                    desc = ''
                    htm = ''
                    try:
                        title += jsonTree['dataItem']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        name += jsonTree['dataItem']['source_name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        organism += jsonTree['dataItem']['organism']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        if jsonTree['dataItem']['description'] != 'NA':
                            desc += jsonTree['dataItem']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        iFile = open(defs.root + defs.clean_geo + '/' + file.split('.')[0] + '.txt')
                        #text += '\n'
                        for line in iFile:
                            htm += line
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                                name,
                                organism,
                                desc,
                                htm)
                    insertIntoDatabase('geo', len(sqlArgs), sqlArgs)
                if repo == 'mpd':
                    title = ''
                    desc = ''
                    dataType = ''
                    gender = ''
                    strain = ''
                    scientificName = ''
                    name = ''
                    dimension = ''

                    try:
                        title += jsonTree['dataset']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        desc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        dataType += jsonTree['dataset']['dataType']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        gender += jsonTree['dataset']['gender']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for org in jsonTree['organism']:
                            strain += org['strain'] + ' '
                            scientificName += org['scientificName'] + ' '
                            name+=org['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for dim in jsonTree['dimension']:
                            dimension += dim['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                                title,
                                desc ,
                                dataType ,
                                gender ,
                                strain ,
                                scientificName ,
                                name ,
                                dimension )
                    insertIntoDatabase('mpd', len(sqlArgs), sqlArgs)
                if repo == 'neuromorpho':
                    studyGroup = ''
                    anatomicalPart = ''
                    note = ''
                    name = ''
                    title = ''
                    strain = ''
                    scientificName = ''
                    orgname = ''
                    gender = ''
                    dimension = ''
                    try:
                        studyGroup += jsonTree['studyGroup']['name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for part in jsonTree['anatomicalPart']['name']:
                            anatomicalPart += part + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        note += jsonTree['dataset']['note']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for cel in jsonTree['cell']['name']:
                            name += cel + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        title += jsonTree['treatment']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        strain += jsonTree['organism']['strain']
                        scientificName += jsonTree['organism']['scientificName']
                        orgname += jsonTree['organism']['name']
                        gender += jsonTree['organism']['gender']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for dim in jsonTree['dimension']:
                            dimension += dim['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               studyGroup,
                    anatomicalPart,
                    note,
                    name,
                    title,
                    strain,
                    scientificName,
                    orgname,
                    gender,
                    dimension)
                    insertIntoDatabase('neuromorpho', len(sqlArgs), sqlArgs)
                if repo == 'nursadatasets':
                    title = ''
                    pubdesc = ''
                    keywords = ''
                    datasetdesc = ''
                    datasettitle = ''
                    orgname = ''

                    try:
                        title += jsonTree['dataAcquisition']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        pubdesc += jsonTree['publication']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['dataset']['keywords']:
                            keywords += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        datasetdesc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        datasettitle += jsonTree['dataset']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for org in jsonTree['organism']:
                            orgname += org['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                    pubdesc,
                    keywords,
                    datasetdesc,
                    datasettitle,
                    orgname)
                    insertIntoDatabase('nursadatasets', len(sqlArgs), sqlArgs)
                if repo == 'openfmri':
                    title = ''
                    datasettitle = ''
                    desc = ''

                    try:
                        title += jsonTree['dataAcquisition']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        datasettitle += jsonTree['dataset']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        desc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                               datasettitle,
                               desc)
                    insertIntoDatabase('openfmri', len(sqlArgs), sqlArgs)
                if repo == 'pdb':
                    title = ''
                    desc = ''
                    keywords = ''
                    source = ''
                    host = ''
                    gene = ''

                    try:
                        title += jsonTree['dataItem']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        desc += jsonTree['dataItem']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['dataItem']['keywords']:
                            keywords += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for src in jsonTree['organism']['source']:
                            source += src['scientificName'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for hst in jsonTree['organism']['host']:
                            host += hst['scientificName'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for gen in jsonTree['gene']:
                            gene += gen['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                    desc,
                    keywords,
                    source,
                    host,
                    gene)
                    insertIntoDatabase('pdb', len(sqlArgs), sqlArgs)
                if repo == 'peptideatlas':
                    title = ''
                    desc = ''
                    instrument = ''
                    treatment = ''
                    strain = ''
                    name = ''

                    try:
                        title += jsonTree['dataset']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        desc += jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        instrument += jsonTree['instrument']['name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        treatment += jsonTree['treatment']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for org in jsonTree['organism']:
                            strain += org['strain'] + ' '
                            name += org['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                    desc,
                    instrument,
                    treatment,
                    strain,
                    name)
                    insertIntoDatabase('peptideatlas', len(sqlArgs), sqlArgs)
                if repo == 'phenodisco':
                    MESHterm = ''
                    title = ''
                    inexclude = ''
                    desc = ''
                    gender = ''
                    disease = ''
                    history = ''
                    try:
                        MESHterm += jsonTree['MESHterm']
                        title+=jsonTree['title']
                        inexclude+=jsonTree['inexclude']
                        desc += jsonTree['desc']
                        gender+=jsonTree['gender']
                        disease+=jsonTree['disease']
                        history+=jsonTree['history']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               MESHterm,
                    title ,
                    inexclude,
                    desc ,
                    gender,
                    disease,
                    history)
                    insertIntoDatabase('phenodisco', len(sqlArgs), sqlArgs)

                if repo == 'physiobank':
                    title = ''
                    dataType = ''
                    desc = ''
                    try:
                        title += jsonTree['dataset']['title']
                        dataType+=jsonTree['dataset']['dataType']
                        desc+=jsonTree['dataset']['description']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                               dataType,
                               desc)
                    insertIntoDatabase('physiobank', len(sqlArgs), sqlArgs)
                if repo == 'proteomexchange':
                    instrument = ''
                    title = ''
                    keywords = ''
                    organism = ''
                    try:
                        instrument += jsonTree['instrument']['name']
                        title +=jsonTree['dataset']['title']
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for kwd in jsonTree['keywords']:
                            keywords += kwd + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    try:
                        for org in jsonTree['organism']:
                            organism += org['name'] + ' '
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               instrument,
                               title,
                               keywords,
                               organism)
                    insertIntoDatabase('proteomexchange', len(sqlArgs), sqlArgs)
                if repo == 'yped':
                    title  = ''
                    desc = ''
                    datasettitle = ''
                    name = ''
                    try:
                        title += jsonTree['dataAcquisition']['title']
                        desc += jsonTree['dataset']['description']
                        datasettitle += jsonTree['dataset']['title']
                        name += jsonTree['organism']['name']
                    except (Exception, IndexError) as e:
                        handleExc()
                    sqlArgs = (lid,
                               title,
                               desc,
                               datasettitle,
                               name)
                    insertIntoDatabase('yped', len(sqlArgs), sqlArgs)
                """errFile = open('error_log', 'a')
                if text == "":
                    errFile.write(repo)
                    errFile.write("empty file " + file)

                doc += text + "</body>\n<\doc>"""""
                """oFile = open(defs.root + defs.clean_all + '/' + file.split('.')[0] + '.txt', 'w+')
                oFile.write(doc.encode('utf-8'))
                oFile.close()"""