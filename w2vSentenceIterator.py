from gensim.models import word2vec
import os
import logging
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = MySentences('M:/biocaddie data/PubMed/sentences')  # a memory-friendly iterator
model = word2vec.Word2Vec(sentences, size=100, window=5, min_count=10, workers=4)
model.wv.save_word2vec_format('M:/biocaddie data/PubMed/VSM/pubmed_size100_window5_min_count10.bin', binary=True)