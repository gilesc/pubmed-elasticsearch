#!/usr/bin/env bash

./wait-for-it.sh -t 0 elasticsearch-pubmed:9200 -- ./daemon.sh
