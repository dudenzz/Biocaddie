import sqlite3
import enchant
import initials
import xml.etree.ElementTree as ET
defs = initials.defaults()

def loadMeshDict():
    file = open('meshterms.txt', 'r')
    dict = {}
    for line in file:
        #print line[0]
        key = line[0]
        if key in dict:
            #jest klucz
            value = dict[key]
            value.append(line.replace('\n',''))
        else:
            #nowy klucz
            dict[key] = [line.replace('\n','')]
    return dict

def splitString(str):
    try:
        str = str.replace('(', ' ')
    except:
        errFile.write('(string error\n')
        print str
    try:
        str = str.replace(')', ' ')
    except:
        errFile.write(')string error\n')
    try:
        str = str.replace('"', ' ')
    except:
        errFile.write('"string error\n')
    try:
        str = str.replace(']', ' ')
    except:
        errFile.write(']string error\n')
    try:
        str = str.replace('[', ' ')
    except:
        errFile.write('[string error\n')
    try:
        words = str.split()
        finalwords = []
        for w in words:
            app = w.split('_')
            for a in app:
                finalwords.append(a.lower())
        return finalwords
    except:
        errFile.write('[string error - empty string\n')
        return[]

def caclulateScore(finalwords):
    t = 0
    f = 0
    d = enchant.Dict("en_US")
    for w in finalwords:
        if (w != ""):
            try:
                if (d.check(w)):
                    #print w + ' true'
                    t += 1
                else:
                    #f+=1
                    #print w + ' false'
                    key = w[0]
                    if key in meshDict:
                        dm = meshDict[key]
                        #print d
                        meshCheck=0
                        for term in dm:
                            #print term+' =  '+w+'?'
                            if term==w:
                                meshCheck = 1
                                #print term +' = '+w
                                break
                        #print meshCheck
                        if meshCheck==0:
                            f += 1
                        else:
                            t += 1
                    else:
                        f += 1
            except:
                #print 'English check error'
                errFile.write('English check error\n')
    if (t+f==0):
        return -1.0
    ratio = float(t) / float(t + f)
    #print ratio
    return ratio


conn = sqlite3.connect('biocaddie.db')
tableNames = ['arrayexpress','cia','bioproject','clinicaltrials','ctn','cvrg','dataverse',
              'dryad','gemma','geo','mpd','neuromorpho','nursadatasets','openfmri','peptideatlas',
              'phenodisco','physiobank','proteomexchange','yped','pdb']
#common = 'common'

#tableNames = ['arrayexpress']

meshDict = loadMeshDict()
#print meshDict

errFile = open('score_error_log','w')

conn = sqlite3.connect('biocaddie.db')

with conn:
    for t in tableNames:
        print t
        if (t=='bioproject'):
            cursor = conn.execute(
                "SELECT bioproject.id, common.title, dataItemkeywords, dataItemdescription FROM common,bioproject WHERE common.id = bioproject.id")
            iter = 0
            for row in cursor:
                #if (iter==100):
                    #break
                if iter % 100 == 0:
                    print iter
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                kwd = splitString(row[2])
                kwdcount = len(kwd)
                desc = splitString(row[3])
                desccount = len(desc)
                titleScore = caclulateScore(title)
                keywordsScore = caclulateScore(kwd)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                            (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1
        if (t=='arrayexpress'):
            cursor = conn.execute(
                "SELECT common.id, common.title, description FROM common,arrayexpress WHERE common.id = arrayexpress.id")
            iter = 0
            for row in cursor:
                #if (iter==100):
                    #break
                if iter % 100 == 0:
                    print iter
                
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                desc = splitString(row[2])
                desccount = len(desc)
                titleScore = caclulateScore(title)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                    (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t == 'cia'):
            cursor = conn.execute(
                "SELECT common.id, common.title FROM common,cia WHERE common.id = cia.id")
            iter = 0
            for row in cursor:

                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                cur.execute(
                    "INSERT INTO itemScore(id,titleScore, titleCount) VALUES(?,?,?)",
                    (id, titleScore, titlecount))
                iter += 1
        if (t=='clinicaltrials'):
            cursor = conn.execute(
                "SELECT common.id, common.title, StudyGroupdescription, Treatmentdescription, Datasetdescription, keyword FROM common,clinicaltrials WHERE common.id = clinicaltrials.id")
            iter = 0
            for row in cursor:

                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                desc = splitString(row[2]+' '+ row[3]+' ' +row[4])
                descScore = caclulateScore(desc)
                kwd = splitString(row[5])
                kwdcount = len(kwd)
                keywordsScore = caclulateScore(kwd)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                    (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1
        if (t=='ctn'):
            cursor = conn.execute("SELECT common.id, common.title, datasetkeywords, datasetdescription FROM common,ctn WHERE common.id = ctn.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                kwd = splitString(row[2])
                kwdcount = len(kwd)
                keywordsScore = caclulateScore(kwd)
                desc = splitString(row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                            (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1
        if (t=='cvrg'):
            cursor = conn.execute(
                "SELECT common.id, common.title, datasetdescription FROM common,cvrg WHERE common.id = cvrg.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                    (id, titleScore, titlecount,  descScore, desccount))
                iter += 1
        if (t=='dataverse'):
            cursor = conn.execute("SELECT common.id, common.title, publicationdescription, datasetdescription FROM common,dataverse WHERE common.id = dataverse.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2]+' '+row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='dryad'):
            cursor = conn.execute("SELECT common.id, common.title, datasetkeywords, datasetdescription FROM common,dryad WHERE common.id = dryad.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                kwd = splitString(row[2])
                kwdcount = len(kwd)
                keywordsScore = caclulateScore(kwd)
                desc = splitString(row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                            (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1
        if (t=='gemma'):
            cursor = conn.execute("SELECT common.id, common.title, dataItemdescription FROM common,gemma WHERE common.id = gemma.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='geo'):
            cursor = conn.execute("SELECT common.id, common.title, dataItemdescription, htmldata FROM common,geo WHERE common.id = geo.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2]+' '+row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='mpd'):
            cursor = conn.execute("SELECT common.id, common.title, datasetdescription FROM common,mpd WHERE common.id = mpd.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='neuromorpho'):
            cursor = conn.execute("SELECT common.id, common.title FROM common,neuromorpho WHERE common.id = neuromorpho.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)


                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount) VALUES(?,?,?)",
                            (id, titleScore, titlecount))
                iter += 1
        if (t=='nursadatasets'):
            cursor = conn.execute("SELECT common.id, common.title, datasetkeywords, datasetdescription FROM common,nursadatasets WHERE common.id = nursadatasets.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                kwd = splitString(row[2])
                kwdcount = len(kwd)
                keywordsScore = caclulateScore(kwd)
                desc = splitString(row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                            (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1
        if (t=='openfmri'):
            cursor = conn.execute("SELECT common.id, common.title, datasetdescription FROM common,openfmri WHERE common.id = openfmri.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='peptideatlas'):
            cursor = conn.execute("SELECT common.id, common.title, datasetdescription, treatmentdescription FROM common,peptideatlas WHERE common.id = peptideatlas.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2]+' '+row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='phenodisco'):
            cursor = conn.execute("SELECT common.id, common.title, inexclude, desc, history FROM common,phenodisco WHERE common.id = phenodisco.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2]+' '+row[3] + ' '+row[4])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='physiobank'):
            cursor = conn.execute("SELECT common.id, common.title, datasetdescription FROM common,physiobank WHERE common.id = physiobank.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='proteomexchange'):
            cursor = conn.execute("SELECT common.id, common.title, keywords FROM common,proteomexchange WHERE common.id = proteomexchange.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                kwd = splitString(row[2])
                kwdcount = len(kwd)
                kwdScore = caclulateScore(kwd)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, kwdScore, kwdcount))
                iter += 1
        if (t=='yped'):
            cursor = conn.execute("SELECT common.id, common.title, datasetdescription FROM common,yped WHERE common.id = yped.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)

                desc = splitString(row[2])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?)",
                            (id, titleScore, titlecount, descScore, desccount))
                iter += 1
        if (t=='pdb'):
            cursor = conn.execute("SELECT common.id, common.title, dataItemkeywords, dataItemdescription FROM common,pdb WHERE common.id = pdb.id")
            iter = 0
            for row in cursor:
                if iter % 100 == 0:
                    print iter
                #if (iter==100):
                    #break
                id = row[0]
                title = splitString(row[1])
                titlecount = len(title)
                titleScore = caclulateScore(title)
                kwd = splitString(row[2])
                kwdcount = len(kwd)
                keywordsScore = caclulateScore(kwd)
                desc = splitString(row[3])
                desccount = len(desc)
                descScore = caclulateScore(desc)
                cur = conn.cursor()
                cur.execute("INSERT INTO itemScore(id,titleScore, titleCount, keywordsScore, keyWordCount, descriptionScore, descriptionCount) VALUES(?,?,?,?,?,?,?)",
                            (id, titleScore, titlecount, keywordsScore, kwdcount, descScore, desccount))
                iter += 1

errFile.close()