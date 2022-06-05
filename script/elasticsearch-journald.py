#!/usr/bin/env python3

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers

obj = elasticsearch.Elasticsearch("http://localhost:9200/")
q = obj.search(
        {
            "query": {"match_phrase": {"Journal.Title": "Aging Cell"}}, 
            "sort": {"Date": {"order": "desc"}},
            "size": 100,
        }, index="pubmed")
for doc in q["hits"]["hits"]:
    src = doc["_source"]
    print(src["ID"], src["Date"], src["Author"][-1], src["Title"], src["Citations"], sep="\t")
