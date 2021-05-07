import gzip
import itertools
import csv
import collections

import elasticsearch

def parse_concepts(handle):
    reader = csv.reader(handle, delimiter="\t")
    groups = itertools.groupby(reader, lambda row: row[0])
    for id, group in groups:
        id = int(id)
        o = collections.defaultdict(set)
        for row in group:
            type = row[1]
            for concept_id in row[2].split(";"):
                if concept_id == "-":
                    continue
                if type in ("Gene", "Species"):
                    concept_id = int(concept_id)
                o[type].add(concept_id)
        o = {k:list(v) for k,v in o.items()}
        if len(o) == 0:
            continue
        yield id, o

def get_insert_op(id, attrs):
    return {
        "_index": "pubmed",
        "_op_type": "update",
        "_id": id,
        "doc_as_upsert": True,
        "doc": attrs
    }

def insert_ops(path):
    with gzip.open(path, mode="rt") as h:
        for id, attrs in parse_concepts(h):
            yield get_insert_op(id, attrs)

if __name__ == "__main__":
    es = elasticsearch.Elasticsearch(host="elasticsearch-pubmed")
    path = "/data/PubTator/bioconcepts2pubtatorcentral.gz"
    it = insert_ops(path)
    elasticsearch.helpers.bulk(es, it, stats_only=True)
    es.indices.refresh(index="pubmed")
