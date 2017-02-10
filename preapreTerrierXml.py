import sqlite3

sqlQueries = ['SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,description FROM common,partialscore, arrayexpress where common.id=partialscore.id and common.id=arrayexpress.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,dataItemkeywords, dataItemdescription FROM common,partialscore, bioproject where common.id=partialscore.id and common.id=bioproject.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription FROM common,partialscore, cia where common.id=partialscore.id and common.id=cia.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,keyword, StudyGroupdescription, Treatmentdescription, Datasetdescription FROM common,partialscore, clinicaltrials where common.id=partialscore.id and common.id=clinicaltrials.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetkeywords, datasetdescription FROM common,partialscore, ctn where common.id=partialscore.id and common.id=ctn.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription FROM common,partialscore, cvrg where common.id=partialscore.id and common.id=cvrg.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,publicationdescription, datasetdescription FROM common,partialscore, dataverse where common.id=partialscore.id and common.id=dataverse.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetkeywords, datasetdescription FROM common,partialscore, dryad where common.id=partialscore.id and common.id=dryad.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,dataItemdescription FROM common,partialscore, gemma where common.id=partialscore.id and common.id=gemma.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,dataItemdescription, htmldata FROM common,partialscore, geo where common.id=partialscore.id and common.id=geo.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription FROM common,partialscore, mpd where common.id=partialscore.id and common.id=mpd.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription FROM common,partialscore, neuromorpho where common.id=partialscore.id and common.id=neuromorpho.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetkeywords, datasetdescription FROM common,partialscore, nursadatasets where common.id=partialscore.id and common.id=nursadatasets.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription FROM common,partialscore, openfmri where common.id=partialscore.id and common.id=openfmri.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription, treatmentdescription FROM common,partialscore, peptideatlas where common.id=partialscore.id and common.id=peptideatlas.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,inexclude, desc, history FROM common,partialscore, phenodisco where common.id=partialscore.id and common.id=phenodisco.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription FROM common,partialscore, physiobank where common.id=partialscore.id and common.id=physiobank.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,keywords FROM common,partialscore, proteomexchange where common.id=partialscore.id and common.id=proteomexchange.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,datasetdescription FROM common,partialscore, yped where common.id=partialscore.id and common.id=yped.id',
'SELECT common.id,filename,common.title,repository,hasTitle,hasKeywords,hasDescription,dataItemkeywords, dataItemdescription FROM common,partialscore, pdb where common.id=partialscore.id and common.id=pdb.id']

conn = sqlite3.connect('biocaddie.db')

li=0
size=794992
oFile = open('biocaddieTerrier.xml','w')

for query in sqlQueries:
    #print query
    cursor = conn.execute(query)
    for row in cursor:
        #if li>0:
            #break
        id = row[0]
        docno = row[1].replace('.xml', '')
        title = row[2]
        repo = row[3]
        hasTitle = row[4]
        hasKeywords = row[5]
        hasDescription = row[6]

        keywords = ''
        description = ''
        rowLen = len(row)
        if rowLen>7:
            if hasKeywords == 0:
                for idx in range(7,rowLen):
                    description += row[idx]+'\n'
            else:
                keywords = row[7]
                if rowLen>8:
                    for idx in range(8,rowLen):
                        description += row[idx] + '\n'
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

        if li % 10000 == 0:
            progres = int((float(li)/float(size))*100.0)
            print str(progres)+'%'
            #print li
        li += 1

oFile.close()
