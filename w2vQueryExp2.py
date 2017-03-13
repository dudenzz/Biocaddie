import gensim
import codecs

def clean(line):
    line = line.replace("'s", "")
    line = line.replace('`s', '')
    #line = line.decode("utf-8").replace('\u2019s','').encode("utf-8")
    special=u'\u2019s'
    line=line.replace(special,'')
    #line = line.replace('\u2019s', '')
    #line = line.replace('\n','')
    #line = line.replace('\r', '')
    return line

vsmPath='M:/biocaddie data/PubMed/VSM/pubmed_size100_window5_min_count10.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(vsmPath, binary=True)
filename='M:/terrier/terrier-core-4.2/var/topics2b.txt'
file = codecs.open(filename, encoding='utf-8')
result=''
idx=1
#pubmed
w2vTreshold=0.9
#biocad
#highTreshold = 0.8
#lowTreshold=0.7
for line in file:
    line=line.lower()
    words = line.split()
    words.remove(words[0])
    #print words
    qexp=[]

    for w in words:
        w2v = model.most_similar(w, topn=1)
        for w2 in w2v:
            score = float(w2[1])
            #pubmed
            if score>=w2vTreshold:
                wrd=clean(w2[0])
                if not wrd in line:
                    qexp.append(wrd)
            #biocad
            #if score>=lowTreshold and score<=highTreshold:
                #wrd=clean(w[0])
                #if not wrd in line:
                    #qexp.append(wrd)
    print qexp
    result += str(idx) + ' '
    for w in words:
        #result += w + '^5 '
        result += w+'^150 '
    for w in qexp:
        result += w+' '
    result += '\n'
    idx+=1

file.close()
targetFile = open(filename.replace('.txt','_expand.txt'),'w')
targetFile.write(result.encode('utf-8'))
targetFile.close()
