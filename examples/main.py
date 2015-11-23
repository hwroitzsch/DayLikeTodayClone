import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request

# HTTP URL is constructed accordingly with JSON query results format in mind.

def sparqlQuery(query, baseURL, format="application/json"):
    params = {
        "default-graph": "",
        "should-sponge": "soft",
        "query": query,
        "debug": "on",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }
    querypart = urlencode(params)
    binary_query = querypart.encode('utf8')
    request = Request(baseURL, binary_query)
    response = urlopen(request).read()
    return json.loads(response)

# Setting Data Source Name (DSN)
data_source_name = "http://dbpedia.org/sparql"

# Virtuoso pragmas for instructing SPARQL engine to perform an HTTP GET
# using the IRI in FROM clause as Data Source URL

query = """DEFINE get:soft "replace" SELECT DISTINCT * FROM <%s> WHERE {?s ?p ?o}""" %data_source_name

query_people_born_before_1900 = """
SELECT ?name ?birth ?death ?person
WHERE {
?person dbo:birthPlace :Berlin .
?person dbo:birthDate ?birth .
?person foaf:name ?name .
?person dbo:deathDate ?death .
FILTER (?birth < "1900-01-01"^^xsd:date) .
}
ORDER BY ?name
"""

data = sparqlQuery(query, "http://localhost:8890/sparql/")

print("Retrieved data:\n" + json.dumps(data, sort_keys=True, indent=4))
