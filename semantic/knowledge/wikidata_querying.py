#!/usr/bin/env python3.6

__author__ = "Pierre-Alexandre Fonta"
__maintainer__ = "Pierre-Alexandre Fonta"

from SPARQLWrapper import SPARQLWrapper, JSON


class QueryingService:

    def __init__(self, endpoint="https://query.wikidata.org/sparql"):
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)

    def fetch(self, query):
        self.sparql.setQuery(query)
        return self.sparql.query().convert()

    def search_entity_contains(self, entity_name, entity_type):
        """Search an entity in Wikidata by its label and upper type."""
        query = """SELECT DISTINCT ?id WHERE {{
            ?id rdfs:label ?entity_name .
            ?id wdt:P31 ?x .  # instance_of
            # FIXME We need to add humans.
            ?x wdt:P279* wd:Q215380 .  # subclass_of band
            ?id wdt:P136 ?genre .
            ?genre ?label ?subgenre_name .
            FILTER(CONTAINS(LCASE(?entity_name), LCASE("{}")))
            FILTER(CONTAINS(LCASE(?subgenre_name), LCASE("{}")))
        }}""".format(entity_name, entity_type)
        response = self.fetch(query)
        bindings = response['results']['bindings']
        return [x['id']['value'].split("/")[-1] for x in bindings]


def main():
    qs = QueryingService()
    ids = qs.search_entity_contains('perfume', 'j-pop')
    print(ids)  # ['Q494703']


if __name__ == "__main__":
    main()
