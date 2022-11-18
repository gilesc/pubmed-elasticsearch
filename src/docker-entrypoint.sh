#!/usr/bin/env bash

#sleep 60
#./daemon.sh
./wait-for-it.sh -t 0 elasticsearch-pubmed:9200 -- ./daemon.sh
