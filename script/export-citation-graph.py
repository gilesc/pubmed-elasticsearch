#!/usr/bin/env python3

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers

obj = elasticsearch.Elasticsearch("http://localhost:9200/")

it = elasticsearch.helpers.scan(obj, 
        index="pubmed",
        query={"query": {"match_all": {}}}
)

for doc in it:
    src = doc["_source"]
    source_id = src["ID"]
    for target_id in src.get("Citations", []):
        print(source_id, target_id, sep="\t")
