import sqlite3

def addSqlData (sqlData,key,v):
    if key in sqlData:
        # jest klucz
        value = sqlData[key]
        value.append(v)
    else:
        # nowy klucz
        sqlData[key] = [v]

conn = sqlite3.connect('biocaddie.db')
iter=0
sqlData = {}
with conn:
    # TITLE
    print 'Get title score'
    iter = 0
    cursor = conn.execute(
        'SELECT common.id FROM itemscore,common WHERE itemscore.id = common.id AND (titlecount<3 OR titlescore<=0 OR titlecount IS NULL)')
    for row in cursor:
        key = row[0]
        v = 0
        addSqlData(sqlData,key,v)
        if iter % 1000 == 0:
            print iter
        iter += 1
    cursor = conn.execute(
        'select common.id from itemscore,common where itemscore.id = common.id and not(titlecount<3 or titlescore<=0 or titlecount is null)')
    for row in cursor:
        key = row[0]
        v = 1
        addSqlData(sqlData, key, v)
        if iter % 1000 == 0:
            print iter
        iter += 1

    # DESCRIPTION
    print 'Get description score'
    iter = 0
    cursor = conn.execute(
        'select common.id from itemscore,common where itemscore.id = common.id and (descriptioncount<3 or descriptionscore<=0 or descriptioncount is null)')
    for row in cursor:
        key = row[0]
        v = 0
        addSqlData(sqlData, key, v)
        if iter % 1000 == 0:
            print iter
        iter += 1
    cursor = conn.execute(
        'select common.id from itemscore,common where itemscore.id = common.id and not(descriptioncount<3 or descriptionscore<=0 or descriptioncount is null)')
    for row in cursor:
        key = row[0]
        v = 1
        addSqlData(sqlData, key, v)
        if iter % 1000 == 0:
            print iter
        iter += 1


    # KEYWORDS
    print 'Get description score'
    iter = 0
    cursor = conn.execute(
        'select common.id from itemscore,common where itemscore.id = common.id and (keywordcount<=0 or keywordcount is null)')
    for row in cursor:
        key = row[0]
        v = 0
        addSqlData(sqlData, key, v)
        if iter % 1000 == 0:
            print iter
        iter += 1
    cursor = conn.execute(
        'select common.id from itemscore,common where itemscore.id = common.id and not(keywordcount<=0 or keywordcount is null)')
    for row in cursor:
        key = row[0]
        v = 1
        addSqlData(sqlData, key, v)
        if iter % 1000 == 0:
            print iter
        iter += 1
    #print sqlData

    #INSERT INTO DATABASE
    print 'Inserting scores into database'
    iter=0
    for key in sqlData:
        id = int(key)
        data = sqlData[key]
        hasTitle = data[0]
        hasDescription = data[1]
        hasKeywords = data[2]
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO partialscore (id,hasTitle,hasDescription,hasKeywords) VALUES(?,?,?,?)",(id,hasTitle,hasDescription,hasKeywords))
        if iter % 1000 == 0:
            print iter
        iter += 1