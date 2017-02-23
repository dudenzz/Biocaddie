# -*- coding: utf-8 -*-
import sys
import codecs

def getToFind(queryString):
    res=queryString.split(' on ')
    if len(res)>1:
        return res
    res=queryString.split(' related to ')
    if len(res) > 1:
        return res
    res = queryString.split(' that mention ')
    if len(res) > 1:
        return res

def getSearchWhere(queryString):
    res = queryString.split(' across ')
    return res

def getToQuery(queryString):

    t1=[]
    t2=[]
    t3=[]
    t0 = queryString.split(' in relation to ')
    for obj in t0:
       t1 += obj.split(' in ')
    for obj in t1:
        t2+= obj.split(' related to ')
    for obj in t2:
        t3+=obj.split(' and ')
    return t3



filename = ''
try:
    filename = sys.argv[1]
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

if filename == '':
    print 'No query file provided'
    raise SystemExit
print filename
try:
    ofile = codecs.open(filename,encoding='utf-8')
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

#queryList=[]
idx=1
doc='<queries>\n'
for line in ofile:

    #print idx
    #queryList.append(line)
    toQuery = []
    temp=getToFind(line)
    #toFind=temp[0]
    toFind=temp[0].replace('Find ','')
    toFind=toFind.replace('Search for ','')

    #print'toFind:'
    #print repr(toFind)


    if len(temp)>2: #related to 2 times
        end = len(temp)-1
        for i in range(1,end):
            toQuery.append(temp[i])
        temp=getSearchWhere(temp[end])
        if len(temp)>1:
            searchWhere = temp[1]
        else:
            searchWhere = ''
    else:
        temp = getSearchWhere(temp[1])
        if len(temp) > 1:
            searchWhere = temp[1]
        else:
            searchWhere = ''
    #print'searchWhere'
    #print repr(searchWhere)


    temp = getToQuery(temp[0])
    for obj in temp:
        toQuery.append(obj)
    #print'toQuery'
    #print repr(toQuery)

    doc += '<query>\n'
    doc += '<number>\n' + str(idx) + '\n</number>\n'
    doc += '<toFind>\n' + toFind + '\n</toFind>\n'
    doc += '<toQueryList>\n'
    for obj in toQuery:
        doc += '<toQuery>\n'+obj.replace('\n','')+'\n</toQuery>\n'
    doc += '</toQueryList>\n'
    doc += '<searchWhere>\n' +searchWhere.replace('\n','') + '</searchWhere>\n'
    doc +='</query>\n'


    idx+=1

doc +='</queries>\n'
ofile.close()
wfile = open('qeuries.xml','w')
wfile.write(doc.encode('utf-8'))
wfile.close()

print 'Done.'
