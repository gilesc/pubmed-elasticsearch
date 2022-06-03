#!/usr/bin/env python3

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers

obj = elasticsearch.Elasticsearch("http://localhost:9200/")

it = elasticsearch.helpers.scan(obj, 
        index="pubmed",
        query={"query": {"match_phrase": {"Journal.Title": "Aging Cell"}}},
)
for doc in it:
    src = doc["_source"]
    if "Title" in src:
        text = " ".join([
            src.get("Title", "") or "",
            src.get("Abstract", "") or ""
        ]).strip()
        if text:
            pprint.pprint(src)
