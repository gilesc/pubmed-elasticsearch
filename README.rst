====================
elasticsearch-pubmed
====================

Loads Pubmed into an Elasticsearch database running in docker, with automatic weekly updates.

Requirements: docker, docker-compose

How to run:

1. Clone & cd into the repo
2. Create a local directory you want Pubmed XML to be saved to
2. Edit config.env to point to that directory
3. Run ./restart.sh

First, Pubmed XML files will be downloaded to your local directory. Then, they will be loaded into Elasticsearch. A daemon will download and index any update XML files (once weekly by default). 

The elasticsearch service will run at $YOUR_IP:9200.

TODO
====

- Add the complete list of XML fields
