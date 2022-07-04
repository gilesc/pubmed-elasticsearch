import bottle

import itertools
import sys
import pprint

import elasticsearch
import elasticsearch.helpers
import pandas as pd

app = bottle.Bottle()

def fetch():
    obj = elasticsearch.Elasticsearch("http://localhost:9200/")
    o = []
    q = obj.search(
            {
                "query": {"match_phrase": {"Journal.Title": "Aging Cell"}}, 
                "sort": {"Date": {"order": "desc"}},
                "size": 100,
            }, index="pubmed")
    for doc in q["hits"]["hits"]:
        src = doc["_source"]
        o.append((src["ID"], src["Date"], src["Author"][-1], src["Title"])) #, src["Citations"]))
    o = pd.DataFrame(o, columns=["ID", "Date", "FirstAuthor", "Title"])
    return o

@app.route("/")
def index():
    df = fetch()
    return "hello world"

if __name__ == "__main__":
    app.run(host="localhost", port=9090)
