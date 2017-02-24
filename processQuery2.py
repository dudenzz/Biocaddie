import sys
import codecs



def checkFilenames():
    if queryFileName == '':
        print 'No query file provided'
        raise SystemExit
    if searchWhereSeparatorFileName == '':
        print 'No searchWhereSpearator file provided'
        raise SystemExit
    if querySeparatorFileName == '':
        print 'No querySeparator file provided'
        raise SystemExit

def loadSeparators(filename):
    separators=[]
    try:
        ofile = codecs.open(filename, encoding='utf-8')
    except (Exception, IndexError) as e:
        print repr(e) + "\t" + format(
            sys.exc_info()[-1].tb_lineno) + '\n'
        raise SystemExit
    for line in ofile:
        line=line.replace('\n','')
        separators.append(line.replace('\r',''))
    ofile.close()
    return separators

def replaceSeparators (textline,separators,replacement):
    for sep in separators:
        textline=textline.replace(sep,replacement)
    return textline

queryFileName = ''
searchWhereSeparatorFileName = ''
querySeparatorFileName = ''
sws = '#SEARCHWHERE#'
qs = '#QUERY#'

try:
    queryFileName = sys.argv[1]
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

try:
    searchWhereSeparatorFileName = sys.argv[2]
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

try:
    querySeparatorFileName = sys.argv[3]
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

checkFilenames()

searchWhereSeparators = loadSeparators(searchWhereSeparatorFileName)
querySeparators = loadSeparators(querySeparatorFileName)

try:
    ofile = codecs.open(queryFileName,encoding='utf-8')
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'
    raise SystemExit

idx=1
doc='<queries>\n'
for line in ofile:
    #print repr(line)
    searchWhere = ''
    toFind = ''
    toQuery = []
    line = line.replace('\r','')
    line = line.replace('\n', '')
    line=replaceSeparators(line,searchWhereSeparators,sws)
    line = replaceSeparators(line, querySeparators, qs)
    line = line.split(sws)
    if len(line)>1:
        searchWhere = line[1]
    line = line[0].split(qs)
    toFind = line[0]

    for i in range(1,len(line)):
        toQuery.append(line[i])

    doc += '<query>\n'
    doc += '<number>\n' + str(idx) + '\n</number>\n'
    doc += '<toFind>\n' + toFind + '\n</toFind>\n'
    doc += '<toQueryList>\n'
    for obj in toQuery:
        doc += '<toQuery>\n' + obj.replace('\n', '') + '\n</toQuery>\n'
    doc += '</toQueryList>\n'
    doc += '<searchWhere>\n' + searchWhere.replace('\n', '') + '</searchWhere>\n'
    doc += '</query>\n'

    idx += 1
doc +='</queries>\n'
ofile.close()
wfile = open('qeuries.xml','w')
wfile.write(doc.encode('utf-8'))
wfile.close()

print 'Done.'



