====================
elasticsearch-pubmed
====================

Loads Pubmed and PubTator entity annotations into an Elasticsearch database running in docker, with automatic weekly updates.

Requirements: docker, docker-compose

Usage
=====

1. Clone & cd into the repo

2. Create a local directory you want Pubmed XML to be saved to

3. Edit config.env to point to that directory

4. Run ./restart.sh

First, Pubmed XML files will be downloaded to your local directory. Then, they will be loaded into Elasticsearch. A daemon will download and index any update XML files (once weekly by default). 

The Elasticsearch service will run at $YOUR_IP:9200.

You can query it; for example, in Python:

.. code-block:: python

    import elasticsearch

    obj = elasticsearch.Elasticsearch(host="localhost")
    hits = obj.search(index="pubmed", 
        body={"query":{"match":{"Title":"caffeine"}}})["hits"]
    for hit in hits:
        print(hit)
