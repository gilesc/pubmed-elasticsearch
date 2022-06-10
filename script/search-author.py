#!/usr/bin/env python3

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers

obj = elasticsearch.Elasticsearch("http://localhost:9200/")

query = "Van Remmen H"

q = obj.search(
        body={
            "query": {"match_phrase": {"Author": query}}, 
            "sort": {"Date": {"order": "desc"}},
            "size": 100,
        }, 
        index="pubmed")

for doc in q["hits"]["hits"]:
    src = doc["_source"]
    print(src["ID"], src["Date"], src["Author"][0], src["Author"][-1], sep="\t")
    print("", src["Author"], sep="\t")
    print("", src["Title"], sep="\t")
