#!/usr/bin/env bash

export TMPDIR=/data/tmp 

while true; do
    cd /data
    mkdir -p PubMed
    cd PubMed
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/

    #cd /data
    #mkdir -p OA
    #cd OA
    #wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/

    cd /data
    mkdir -p PubTator
    cd PubTator
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/bioconcepts2pubtatorcentral.gz

    echo "Updating PubMed core..."
    python /script/update_pubmed.py

    echo "Updating PubTator concepts..."
    python /script/update_pubtator.py

    echo "Update complete; sleeping for ${REBUILD_DELAY} seconds ..."

    sleep ${REBUILD_DELAY:-604800}
done
