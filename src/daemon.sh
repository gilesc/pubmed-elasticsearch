#!/usr/bin/env bash

while true; do
    cd /data
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/
    echo "Starting to upsert Pubmed..."
    python /script/update_pubmed.py
    echo "Update complete; sleeping for ${REBUILD_DELAY} seconds ..."
    sleep ${REBUILD_DELAY:-604800}
done
