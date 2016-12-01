__author__ = 'Asus'
from initials import defaults
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

def generatePattern(word):
	return "(^|(.*[ _-]))" + word + "(([ _-].*)|$)"
def getConcepts(word):
	pattern = generatePattern(word)
	sparql = SPARQLWrapper("http://boromir.cie.put.poznan.pl:3030/Mesh/sparql")

	#q = """SELECT ?v
	#	{ {?v  <http://www.w3.org/2000/01/rdf-schema#label> ?word } UNION { ?v <http://id.nlm.nih.gov/mesh/vocab#prefLabel> ?word }
	#	FILTER regex(?word, \"""" +  pattern + """\", "i")
	#	}"""

	q = """SELECT ?v
		{ {?v  <http://www.w3.org/2000/01/rdf-schema#label> """ +word+""" } UNION { ?v <http://id.nlm.nih.gov/mesh/vocab#prefLabel> """+word+""" }

		}"""

	sparql.setQuery(q)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	rets = []
	for i in results['results']['bindings']:
		rets.append(i['v']['value'])
	return rets

def getLabels(concept):
	sparql = SPARQLWrapper("http://boromir.cie.put.poznan.pl:3030/Mesh/sparql")
	query = """SELECT ?v {
        {
        	<"""+concept+""">  <http://www.w3.org/2000/01/rdf-schema#label> ?v
        } UNION
        {
        	<"""+concept+""">  <http://id.nlm.nih.gov/mesh/vocab#prefLabel> ?v
        } UNION
        {
        	?tmp ?r <"""+concept+"""> .
          	?tmp <http://www.w3.org/2000/01/rdf-schema#label> ?v
        } UNION
        {
        	?tmp ?r <"""+concept+"""> .
          	?tmp <http://id.nlm.nih.gov/mesh/vocab#prefLabel> ?v
        } UNION
        {
        	<"""+concept+""">  ?r ?tmp .
			?tmp <http://www.w3.org/2000/01/rdf-schema#label> ?v
        } UNION
        {
        	<"""+concept+""">  ?r ?tmp .
			?tmp <http://id.nlm.nih.gov/mesh/vocab#prefLabel> ?v
        }
        }"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	rets = []
	for i in results['results']['bindings']:
		rets.append(i['v']['value'])
	return rets


defs = defaults()
queriesFile = open(defs.root + defs.queries)
expFile = open(defs.root + defs.exp_queries, 'w+')

for i in queriesFile:
	expQuery = i
	print 'Query: ' + i
	for word in i.split(' '):
		if len(i) > 1:
			for c in getConcepts(word):
				print c
				labels = getLabels(c)
				for label in labels:
					expQuery += ' ' + label
	print 'Expanded query:' + expQuery
	expFile.write(expQuery + '\n')

