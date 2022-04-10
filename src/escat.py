#!/usr/bin/env python3

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers

obj = elasticsearch.Elasticsearch(hosts=["10.84.146.12"])

it = elasticsearch.helpers.scan(obj, index="pubmed")
for doc in it:
    src = doc["_source"]
    if "Title" in src:
        text = " ".join([
            src.get("Title", "") or "",
            src.get("Abstract", "") or ""
        ]).strip()
        if text:
            print(src["ID"], text.lower(), sep="\t")
