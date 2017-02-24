import sys
import codecs


def showDict(freqDict):
    for w in freqDict:
        perc = (float(freqDict[w]) / float(count)) * 100.0
        print repr(w), perc

filename = ''
try:
    filename = sys.argv[1]
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'

if filename == '':
    print 'No query file provided'
    raise SystemExit
#print filename
try:
    ofile = codecs.open(filename,encoding='utf-8')
except (Exception, IndexError) as e:
    print repr(e) + "\t" + format(
        sys.exc_info()[-1].tb_lineno) + '\n'


freqDict = {}
count = 0
queries = []
newqueries = []
for line in ofile:

    line = line.split()
    queries.append(line)
    for w in line:
        if w in freqDict:
            freqDict[w] += 1
        else:
            freqDict[w] = 1
        count +=1

#print queries

ofile.close()
wname = 'processedQueries.txt'
wfile = open(wname,'w')
for q in queries:
   #print q
   temp = []
   for w in q:
       perc = (float(freqDict[w])/float(count))*100.0
       #print w, perc
       if perc <= 1.75:
           temp.append(w)
   newqueries.append(temp)

for q in newqueries:
    #print q
    line=''
    for w in q:
       line+=w+' '
    line+='\n'
    wfile.write(line.encode('utf-8'))

wfile.close()
#showDict(freqDict)
print 'Saved as '+wname


