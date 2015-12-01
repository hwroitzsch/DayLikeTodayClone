from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#sparql.setQuery("""
#    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#    SELECT ?label
#    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
#""")

sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?name ?birth ?death ?person
    WHERE {
        ?person dbo:birthPlace :Berlin .
        ?person dbo:birthDate ?birth .
        ?person foaf:name ?name .
        ?person dbo:deathDate ?death .
        FILTER (?birth < "1900-01-01"^^xsd:date) .
    }
    ORDER BY ?birth
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)

#for result in results["results"]["bindings"]:
#    print(
#        'NAME:', result['name']['value'], '\n',
#        'BIRTH:', result['birth']['value'], '\n',
#        'DEATH:', result['death']['value'], '\n',
#        'LINK:', result['person']['value'], '\n',
#        end='\n\n'
#    )

