import sqlite3

sqlQueries = {
    'arrayexpress':'SELECT description FROM arrayexpress WHERE arrayexpress.id = ?',
    'bioproject':'SELECT dataItemkeywords, dataItemdescription FROM bioproject WHERE bioproject.id=?',
    'cia':'',
    'clinicaltrials':'SELECT keyword, StudyGroupdescription, Treatmentdescription, Datasetdescription FROM clinicaltrials WHERE clinicaltrials.id=?',
    'ctn':'SELECT datasetkeywords, datasetdescription FROM ctn WHERE ctn.id=?',
    'cvrg':'SELECT datasetdescription FROM cvrg WHERE cvrg.id=?',
    'dataverse':'SELECT publicationdescription, datasetdescription FROM dataverse WHERE dataverse.id=?',
    'dryad':'SELECT datasetkeywords, datasetdescription FROM dryad WHERE dryad.id=?',
    'gemma':'SELECT dataItemdescription FROM gemma WHERE gemma.id=?',
    'geo':'SELECT dataItemdescription, htmldata FROM geo WHERE geo.id=?',
    'mpd':'SELECT datasetdescription FROM mpd WHERE mpd.id=?',
    'neuromorpho':'',
    'nursadatasets':'SELECT datasetkeywords, datasetdescription FROM nursadatasets WHERE nursadatasets.id=?',
    'openfmri':'SELECT datasetdescription FROM openfmri WHERE openfmri.id=?',
    'peptideatlas':'SELECT datasetdescription, treatmentdescription FROM peptideatlas WHERE peptideatlas.id=?',
    'phenodisco':'SELECT inexclude, desc, history FROM phenodisco WHERE phenodisco.id=?',
    'physiobank':'SELECT datasetdescription FROM physiobank WHERE physiobank.id=?',
    'proteomexchange':'SELECT keywords FROM proteomexchange WHERE proteomexchange.id=?',
    'yped':'SELECT datasetdescription FROM yped WHERE yped.id=?',
    'pdb':'SELECT dataItemkeywords, dataItemdescription FROM pdb WHERE pdb.id=?'
}

conn = sqlite3.connect('biocaddie.db')

li=0

cursor = conn.execute('SELECT common.id,filename,title,repository,hasTitle,hasKeywords,hasDescription FROM common,partialscore where common.id=partialscore.id')

oFile = open('biocaddieTerrier.xml','w')

for row in cursor:

    #if li>200:
        #break

    id = row[0]

    docno = row[1].replace('.xml','')
    title = row[2]
    repo = row[3]
    hasTitle = row[4]
    hasKeywords = row[5]
    hasDescription = row[6]

    keywords = ''
    description = ''

    cur = conn.cursor()
    if sqlQueries[repo]!='':
        cur.execute(sqlQueries[repo],(str(id),))
        if hasKeywords==0:
            for r1 in cur:
                for r2 in r1:
                    description += r2

        else:
            for r1 in cur:
                keywords = r1[0]
                for idx in range(1,len(r1)):
                    description += r1[idx]
    else:
        keywords=''
        description=''


    doc = '<DOC>\n'
    doc+='<DOCNO>'+docno+'</DOCNO>\n'
    if hasTitle==1:
        doc+='<TITLE>'+title+'</TITLE>\n'
    else:
        doc += '<TITLE>#TODO</TITLE>\n'
    if hasKeywords==1:
        doc+='<KEYWORDS>'+keywords+'</KEYWORDS>\n'
    else:
        doc += '<KEYWORDS>#TODO</KEYWORDS>\n'
    if hasDescription==1:
        doc += '<DESCRIPTION>' + description + '</DESCRIPTION>\n'
    else:
        doc += '<DESCRIPTION>#TODO</DESCRIPTION>\n'
    doc+='</DOC>\n'

    #print doc
    oFile.write(doc.encode('utf-8'))

    if li % 100 == 0:
        print li
    li += 1

oFile.close()
