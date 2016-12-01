from SPARQLWrapper import SPARQLWrapper, JSON
import sys

def generatePattern(word):
	return ".*" + word + ".*"
def getConcepts(word):
	pattern = generatePattern(word)
	sparql = SPARQLWrapper("http://boromir.cie.put.poznan.pl:3030/Mesh/sparql")
	q = """SELECT ?v 
		{?v  <http://www.w3.org/2000/01/rdf-schema#label> ?word
		 optional( ?v <http://id.nlm.nih.gov/mesh/vocab#prefLabel> ?word )
		FILTER regex(?word, \"""" +  pattern + """\", "i")
		}"""
	print q
	sparql.setQuery(q)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	rets = []
	for i in results['results']['bindings']:
		rets.append(i['v']['value'])
	return rets
	
def getLabels(concept):
	sparql = SPARQLWrapper("http://boromir.cie.put.poznan.pl:3030/Mesh/sparql")
        sparql.setQuery("SELECT * {<"+concept+">  <http://www.w3.org/2000/01/rdf-schema#label> ?v}")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        rets = []
        for i in results['results']['bindings']:
                rets.append(i['v']['value'])
	sparql.setQuery("""
		SELECT ?v
		WHERE
		{
			<"""+concept+""">  ?r ?tmp .
			?tmp <http://www.w3.org/2000/01/rdf-schema#label> ?v
		}""")
	
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for i in results['results']['bindings']:
                rets.append(i['v']['value'])
	
	sparql.setQuery("""
                SELECT ?v
                WHERE
                {
                        ?tmp ?r <"""+concept+"""> .
                        ?tmp <http://www.w3.org/2000/01/rdf-schema#label> ?v
                }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for i in results['results']['bindings']:
                rets.append(i['v']['value'])


        return rets



for c in getConcepts(sys.argv[1]):
	print getLabels(c)
